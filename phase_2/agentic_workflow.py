import os
from pathlib import Path

from dotenv import load_dotenv

from workflow_agents.base_agents import (
    ActionPlanningAgent,
    EvaluationAgent,
    KnowledgeAugmentedPromptAgent,
    RoutingAgent,
)


load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

product_spec_path = Path(__file__).with_name("Product-Spec-Email-Router.txt")
product_spec = product_spec_path.read_text(encoding="utf-8")

knowledge_action_planning = (
    "Stories are defined from a product spec by identifying a persona, an "
    "action, and a desired outcome for each story. Each story represents a "
    "specific functionality of the product described in the specification.\n"
    "Features are defined by grouping related user stories.\n"
    "Tasks are defined for each story and represent the engineering work "
    "required to develop the product.\n"
    "A development plan contains exactly these ordered steps:\n"
    "1. Define user stories from the product specification.\n"
    "2. Define product features from the user stories and product specification.\n"
    "3. Define engineering tasks from the user stories, product features, and "
    "product specification."
)
action_planning_agent = ActionPlanningAgent(openai_api_key, knowledge_action_planning)

persona_product_manager = (
    "You are a Product Manager responsible for defining user stories for a product."
)
knowledge_product_manager = (
    "Stories are defined by writing sentences with a persona, an action, and a "
    "desired outcome. Every story must use exactly this pattern: "
    "As a [type of user], I want [an action or feature] so that [benefit/value]. "
    "Write several stories for the product specification below, using its user "
    "classes and requirements.\n\n"
    + product_spec
)
product_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(
    openai_api_key, persona_product_manager, knowledge_product_manager
)

persona_product_manager_eval = (
    "You are an evaluation agent that checks the answers of other worker agents."
)
evaluation_criteria_product_manager = (
    "The answer should be user stories that follow this structure: "
    "As a [type of user], I want [an action or feature] so that [benefit/value]."
)
product_manager_evaluation_agent = EvaluationAgent(
    openai_api_key,
    persona_product_manager_eval,
    evaluation_criteria_product_manager,
    product_manager_knowledge_agent,
    5,
)

persona_program_manager = (
    "You are a Program Manager responsible for defining product features."
)
knowledge_program_manager = (
    "Features are cohesive groups of related product capabilities. Use the "
    "product specification below and return each feature with all four fields: "
    "Feature Name, Description, Key Functionality, and User Benefit.\n\n"
    + product_spec
)
program_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(
    openai_api_key, persona_program_manager, knowledge_program_manager
)

persona_program_manager_eval = (
    "You are an evaluation agent that checks the answers of other worker agents."
)
evaluation_criteria_program_manager = (
    "The answer should be product features that follow this structure:\n"
    "Feature Name: A clear, concise title that identifies the capability\n"
    "Description: A brief explanation of what the feature does and its purpose\n"
    "Key Functionality: The specific capabilities or actions the feature provides\n"
    "User Benefit: How this feature creates value for the user"
)
program_manager_evaluation_agent = EvaluationAgent(
    openai_api_key,
    persona_program_manager_eval,
    evaluation_criteria_program_manager,
    program_manager_knowledge_agent,
    5,
)

persona_dev_engineer = (
    "You are a Development Engineer responsible for defining development tasks."
)
knowledge_dev_engineer = (
    "Development tasks identify the technical work required to implement the "
    "product specification below. Return every task with these fields: Task ID, "
    "Task Title, Related User Story, Description, Acceptance Criteria, Estimated "
    "Effort, and Dependencies.\n\n"
    + product_spec
)
development_engineer_knowledge_agent = KnowledgeAugmentedPromptAgent(
    openai_api_key, persona_dev_engineer, knowledge_dev_engineer
)

persona_dev_engineer_eval = (
    "You are an evaluation agent that checks the answers of other worker agents."
)
evaluation_criteria_dev_engineer = (
    "The answer should be tasks following this exact structure:\n"
    "Task ID: A unique identifier for tracking purposes\n"
    "Task Title: Brief description of the specific development work\n"
    "Related User Story: Reference to the parent user story\n"
    "Description: Detailed explanation of the technical work required\n"
    "Acceptance Criteria: Specific requirements that must be met for completion\n"
    "Estimated Effort: Time or complexity estimation\n"
    "Dependencies: Any tasks that must be completed first"
)
development_engineer_evaluation_agent = EvaluationAgent(
    openai_api_key,
    persona_dev_engineer_eval,
    evaluation_criteria_dev_engineer,
    development_engineer_knowledge_agent,
    5,
)


def product_manager_support_function(query):
    """Evaluate the user-story step with the Product Manager worker."""
    result = product_manager_evaluation_agent.evaluate(query)
    return result["final_response"]


def program_manager_support_function(query):
    """Evaluate the feature-definition step with the Program Manager worker."""
    result = program_manager_evaluation_agent.evaluate(query)
    return result["final_response"]


def development_engineer_support_function(query):
    """Evaluate the engineering-task step with the Development Engineer worker."""
    result = development_engineer_evaluation_agent.evaluate(query)
    return result["final_response"]


agents = [
    {
        "name": "Product Manager",
        "description": (
            "Define product personas and user stories only. Do not group stories "
            "into features or create engineering tasks."
        ),
        "func": product_manager_support_function,
    },
    {
        "name": "Program Manager",
        "description": (
            "Group user stories and product requirements into product features. "
            "Do not create user stories or engineering tasks."
        ),
        "func": program_manager_support_function,
    },
    {
        "name": "Development Engineer",
        "description": (
            "Define detailed engineering tasks, acceptance criteria, effort, and "
            "dependencies needed to build the product."
        ),
        "func": development_engineer_support_function,
    },
]
routing_agent = RoutingAgent(openai_api_key, agents)


def run_workflow(workflow_prompt, planner=None, router=None):
    """Print a consolidated plan; injectable agents allow offline contract tests."""
    planner = planner or action_planning_agent
    router = router or routing_agent

    print("\n*** Workflow execution started ***\n")
    print(f"Task to complete in this workflow: {workflow_prompt}")
    print("\nDefining workflow steps from the workflow prompt")

    workflow_steps = planner.extract_steps_from_prompt(workflow_prompt)
    completed_steps = []
    selected_routes = []

    for step_number, step in enumerate(workflow_steps, start=1):
        print(f"\nExecuting step {step_number}: {step}")
        result = router.route(step)
        completed_steps.append(result)
        selected_routes.append(getattr(router, "last_agent_name", None))
        print(f"Step {step_number} result:\n{result}")

    print("\n*** Consolidated development plan ***")
    for index, (step, result) in enumerate(
        zip(workflow_steps, completed_steps), start=1
    ):
        route_headings = {
            "Product Manager": "User Stories",
            "Program Manager": "Product Features",
            "Development Engineer": "Engineering Tasks",
        }
        normalized_step = step.lower()
        if selected_routes[index - 1] in route_headings:
            heading = route_headings[selected_routes[index - 1]]
        elif "stor" in normalized_step:
            heading = "User Stories"
        elif "feature" in normalized_step:
            heading = "Product Features"
        elif "task" in normalized_step:
            heading = "Engineering Tasks"
        else:
            heading = f"Workflow Result {index}"
        print(f"\n## {heading}\n{result}")

    return completed_steps


if __name__ == "__main__":
    workflow_prompt = (
        "Create a complete development plan for the Email Router product, "
        "including user stories, product features, and engineering tasks."
    )
    run_workflow(workflow_prompt)
