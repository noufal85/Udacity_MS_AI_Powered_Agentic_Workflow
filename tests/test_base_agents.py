import importlib
import os
import signal
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
PHASE_1 = ROOT / "phase_1"
sys.path.insert(0, str(PHASE_1))

base_agents = importlib.import_module("workflow_agents.base_agents")


def chat_response(text):
    return SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content=text))]
    )


def embedding_response(values):
    return SimpleNamespace(data=[SimpleNamespace(embedding=values)])


class FakeClient:
    def __init__(self, chat_outputs=None, embeddings=None):
        self.chat_calls = []
        self.embedding_calls = []
        self._chat_outputs = iter(chat_outputs or [])
        self._embeddings = embeddings or {}
        self.chat = SimpleNamespace(
            completions=SimpleNamespace(create=self._create_chat)
        )
        self.embeddings = SimpleNamespace(create=self._create_embedding)

    def _create_chat(self, **kwargs):
        self.chat_calls.append(kwargs)
        return chat_response(next(self._chat_outputs))

    def _create_embedding(self, **kwargs):
        self.embedding_calls.append(kwargs)
        return embedding_response(self._embeddings[kwargs["input"]])


class BaseAgentTests(unittest.TestCase):
    def test_chat_model_can_be_overridden_for_live_execution(self):
        client = FakeClient(chat_outputs=["OK"])
        with patch.dict(os.environ, {"OPENAI_CHAT_MODEL": "gpt-4.1-mini"}):
            with patch.object(base_agents, "OpenAI", return_value=client):
                base_agents.DirectPromptAgent("key").respond("Reply OK")
        self.assertEqual(client.chat_calls[0]["model"], "gpt-4.1-mini")

    def test_rag_uses_configured_endpoint_for_embeddings(self):
        client = FakeClient(embeddings={"sample": [1.0, 0.0]})
        with patch.dict(os.environ, {"OPENAI_BASE_URL": "https://api.openai.com/v1"}):
            with patch.object(base_agents, "OpenAI", return_value=client) as factory:
                base_agents.RAGKnowledgePromptAgent("key", "researcher").get_embedding("sample")
        self.assertEqual(factory.call_args.kwargs["base_url"], "https://api.openai.com/v1")

    def test_rag_chunking_finishes_after_the_final_chunk(self):
        agent = base_agents.RAGKnowledgePromptAgent(
            "key", "researcher", chunk_size=10, chunk_overlap=2
        )

        def timeout_handler(signum, frame):
            raise TimeoutError("chunking did not advance past the final chunk")

        previous_handler = signal.signal(signal.SIGALRM, timeout_handler)
        original_directory = Path.cwd()
        try:
            with tempfile.TemporaryDirectory() as temp_directory:
                os.chdir(temp_directory)
                signal.alarm(1)
                chunks = agent.chunk_text("abcdefghijkl")
                signal.alarm(0)
        finally:
            signal.alarm(0)
            os.chdir(original_directory)
            signal.signal(signal.SIGALRM, previous_handler)

        self.assertEqual(chunks[-1]["text"], "ijkl")

    def test_direct_prompt_agent_sends_only_user_prompt(self):
        client = FakeClient(chat_outputs=["Paris"])
        with patch.object(base_agents, "OpenAI", return_value=client):
            result = base_agents.DirectPromptAgent("key").respond("Capital?")

        self.assertEqual(result, "Paris")
        self.assertEqual(client.chat_calls[0]["model"], "gpt-3.5-turbo")
        self.assertEqual(
            client.chat_calls[0]["messages"],
            [{"role": "user", "content": "Capital?"}],
        )

    def test_augmented_agent_applies_persona_and_resets_context(self):
        client = FakeClient(chat_outputs=["Dear students, Paris."])
        with patch.object(base_agents, "OpenAI", return_value=client):
            agent = base_agents.AugmentedPromptAgent("key", "a professor")
            result = agent.respond("Capital?")

        self.assertEqual(result, "Dear students, Paris.")
        system = client.chat_calls[0]["messages"][0]
        self.assertEqual(system["role"], "system")
        self.assertIn("a professor", system["content"])
        self.assertIn("Forget all previous context", system["content"])

    def test_knowledge_agent_includes_only_supplied_knowledge(self):
        client = FakeClient(chat_outputs=["London"])
        with patch.object(base_agents, "OpenAI", return_value=client):
            agent = base_agents.KnowledgeAugmentedPromptAgent(
                "key", "a professor", "The capital is London"
            )
            result = agent.respond("Capital?")

        self.assertEqual(result, "London")
        messages = client.chat_calls[0]["messages"]
        self.assertIn("The capital is London", messages[0]["content"])
        self.assertIn("do not use your own knowledge", messages[0]["content"])
        self.assertEqual(messages[1], {"role": "user", "content": "Capital?"})

    def test_evaluation_agent_refines_until_accepted(self):
        worker = SimpleNamespace(respond=lambda prompt: f"worker:{prompt}")
        client = FakeClient(
            chat_outputs=[
                "No, the format is wrong.",
                "Return only a city name.",
                "Yes, it meets the criteria.",
            ]
        )
        with patch.object(base_agents, "OpenAI", return_value=client):
            result = base_agents.EvaluationAgent(
                "key", "strict evaluator", "city only", worker, 3
            ).evaluate("Capital?")

        self.assertEqual(
            set(result), {"final_response", "evaluation", "iterations"}
        )
        self.assertEqual(result["iterations"], 2)
        self.assertTrue(result["evaluation"].startswith("Yes"))
        self.assertEqual(len(client.chat_calls), 3)
        self.assertTrue(all(call["temperature"] == 0 for call in client.chat_calls))
        self.assertIn("Make only these corrections", result["final_response"])

    def test_evaluation_agent_returns_last_attempt_at_limit(self):
        worker = SimpleNamespace(respond=lambda prompt: "attempt")
        client = FakeClient(chat_outputs=["No, incomplete", "Add details"])
        with patch.object(base_agents, "OpenAI", return_value=client):
            result = base_agents.EvaluationAgent(
                "key", "evaluator", "complete", worker, 1
            ).evaluate("Do work")

        self.assertEqual(result["iterations"], 1)
        self.assertEqual(result["final_response"], "attempt")
        self.assertEqual(result["evaluation"], "No, incomplete")

    def test_router_selects_highest_cosine_similarity(self):
        calls = []
        client = FakeClient(
            embeddings={
                "question": [1.0, 0.0],
                "Texas topics": [0.9, 0.1],
                "Europe topics": [0.0, 1.0],
            }
        )
        agents = [
            {
                "name": "Texas",
                "description": "Texas topics",
                "func": lambda value: calls.append(("Texas", value)) or "texas",
            },
            {
                "name": "Europe",
                "description": "Europe topics",
                "func": lambda value: calls.append(("Europe", value)) or "europe",
            },
        ]
        with patch.object(base_agents, "OpenAI", return_value=client):
            result = base_agents.RoutingAgent("key", agents).route("question")

        self.assertEqual(result, "texas")
        self.assertEqual(calls, [("Texas", "question")])
        self.assertTrue(
            all(
                call["model"] == "text-embedding-3-large"
                for call in client.embedding_calls
            )
        )

    def test_action_planner_returns_clean_steps(self):
        client = FakeClient(
            chat_outputs=["Steps:\n1. Crack eggs\n- Beat eggs\n3) Cook eggs\n"]
        )
        with patch.object(base_agents, "OpenAI", return_value=client):
            steps = base_agents.ActionPlanningAgent(
                "key", "egg preparation"
            ).extract_steps_from_prompt("Make eggs")

        self.assertEqual(steps, ["Crack eggs", "Beat eggs", "Cook eggs"])
        self.assertEqual(client.chat_calls[0]["model"], "gpt-3.5-turbo")


if __name__ == "__main__":
    unittest.main()
