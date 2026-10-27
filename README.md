# AI-Powered Agentic Workflow for Project Management

This project implements a reusable OpenAI agent library and an agentic project-management workflow for the supplied Email Router product specification.

## Project structure

- `phase_1/workflow_agents/base_agents.py`: seven reusable agent classes
- `phase_1/*.py`: one runnable demonstration per agent
- `phase_2/agentic_workflow.py`: action planning, semantic routing, evaluation, and consolidated plan generation
- `phase_2/Product-Spec-Email-Router.txt`: required product specification
- `tests/`: deterministic offline contract tests
- `PROJECT_REQUIREMENTS.md`: source register and rubric validation matrix

## Setup

Use Python 3.13 or another version supported by the pinned dependencies.

```bash
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Set the API key in the environment or in an untracked `.env` file:

```bash
export OPENAI_API_KEY="your-key"
export OPENAI_BASE_URL="https://api.openai.com/v1"
export OPENAI_CHAT_MODEL="gpt-4.1-mini"
```

## Offline validation

The offline suite replaces OpenAI clients with deterministic fakes and does not require an API key.

```bash
python -m unittest discover -s tests -v
python -m compileall -q phase_1 phase_2 tests
```

## Live execution

Captured live execution evidence is in [evidence/live](evidence/live/). See
[the evidence guide](evidence/README.md) for the model change, run manifest,
and output validation results.

The original rubric names `gpt-3.5-turbo`. That remains the code's compatibility
default, but the API rejected it as deprecated during the October 26 access
check. The project owner authorized `gpt-4.1-mini` for these live runs. Set
`OPENAI_CHAT_MODEL` as above to reproduce them; embeddings still use
`text-embedding-3-large`. The supplied RAG agent also honors `OPENAI_BASE_URL`
so all eight programs can use the same endpoint.

Run the Phase 1 demonstrations from the project root:

```bash
python phase_1/direct_prompt_agent.py
python phase_1/augmented_prompt_agent.py
python phase_1/knowledge_augmented_prompt_agent.py
python phase_1/rag_knowledge_prompt_agent.py
python phase_1/evaluation_agent.py
python phase_1/routing_agent.py
python phase_1/action_planning_agent.py
```

Run the complete workflow:

```bash
python phase_2/agentic_workflow.py
```

The workflow prints a consolidated development plan containing user stories, product features, and engineering tasks. Live output depends on API access and may incur provider charges.
