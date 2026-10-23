import importlib
import io
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
PHASE_2 = ROOT / "phase_2"
sys.path.insert(0, str(PHASE_2))


class WorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workflow = importlib.import_module("agentic_workflow")

    def test_product_spec_is_loaded(self):
        self.assertIn("Email Router", self.workflow.product_spec)
        self.assertIn("10,000 emails per hour", self.workflow.product_spec)

    def test_support_functions_pass_step_directly_to_evaluator(self):
        evaluator = SimpleNamespace(
            evaluate=lambda step: {
                "final_response": f"validated:{step}",
                "evaluation": "Yes",
                "iterations": 1,
            }
        )
        with patch.object(
            self.workflow, "product_manager_evaluation_agent", evaluator
        ):
            result = self.workflow.product_manager_support_function("define stories")

        self.assertEqual(result, "validated:define stories")

    def test_routes_have_required_shape_and_roles(self):
        routes = self.workflow.routing_agent.agents
        self.assertEqual(
            {route["name"] for route in routes},
            {"Product Manager", "Program Manager", "Development Engineer"},
        )
        self.assertTrue(
            all(set(route) == {"name", "description", "func"} for route in routes)
        )

    def test_run_workflow_keeps_and_prints_all_results(self):
        planner = SimpleNamespace(
            extract_steps_from_prompt=lambda prompt: [
                "Define user stories",
                "Define product features",
                "Define engineering tasks",
            ]
        )
        router = SimpleNamespace(
            route=lambda step: {
                "Define user stories": "As a user, I want routing so that replies are faster.",
                "Define product features": "Feature Name: Smart Routing",
                "Define engineering tasks": "Task ID: ER-001",
            }[step]
        )
        output = io.StringIO()

        with redirect_stdout(output):
            completed = self.workflow.run_workflow(
                "Create the development plan", planner=planner, router=router
            )

        self.assertEqual(len(completed), 3)
        rendered = output.getvalue()
        self.assertIn("As a user", rendered)
        self.assertIn("Feature Name", rendered)
        self.assertIn("Task ID", rendered)


if __name__ == "__main__":
    unittest.main()
