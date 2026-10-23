# Project requirements and validation plan

## Source register

| Source | Authority | Material used | Status |
|---|---|---|---|
| `../Introduction.docx` | Final assignment rubric and submission instructions | Phase 1 agent contracts, Phase 2 workflow requirements, output structures | Read and visually verified (24 pages) |
| `phase_1/README.md` | Starter guidance | Seven agent scripts and class behavior | Read in full |
| `phase_2/README.md` | Starter guidance | Workflow construction and route descriptions | Read in full |
| `phase_2/Product-Spec-Email-Router.txt` | Required workflow input | Email Router scope and requirements | Read in full |
| `requirements.txt` | Dependency contract | Pinned Python dependencies | Accessible |

When the final rubric and starter README differ, the final rubric controls. In particular, each Phase 2 support function passes the workflow step to `EvaluationAgent.evaluate`; the evaluation agent invokes its worker internally.

## Rubric matrix

| ID | Requirement | Artifact | Verification | Status |
|---|---|---|---|---|
| P1-1 | Direct agent uses `gpt-3.5-turbo`, a user message only, and returns text | `phase_1/workflow_agents/base_agents.py` | Offline unit test | Verified |
| P1-2 | Augmented agent stores and applies its persona while resetting context | Same | Offline unit test | Verified |
| P1-3 | Knowledge agent stores persona and knowledge and restricts its answer to supplied knowledge | Same | Offline unit test | Verified |
| P1-4 | Supplied RAG agent remains available | Same | Import, regression test, static check | Verified |
| P1-5 | Evaluation agent iterates, uses temperature 0, and returns exactly `final_response`, `evaluation`, `iterations` | Same | Offline unit tests | Verified |
| P1-6 | Router embeds with `text-embedding-3-large`, selects by cosine similarity, and calls the selected route | Same | Offline unit test | Verified |
| P1-7 | Action planner returns a clean list of steps | Same | Offline unit test | Verified |
| P1-8 | Seven runnable demonstration scripts load credentials from the environment | `phase_1/*.py` | Compile/static check; live run if key exists | Structurally verified; live run blocked |
| P2-1 | Product specification is loaded and four required classes are imported | `phase_2/agentic_workflow.py` | Offline unit/static test | Verified |
| P2-2 | Three worker/evaluator pairs and three semantic routes are configured | Same | Offline unit test | Verified |
| P2-3 | Support functions call their evaluation agents with the workflow step | Same | Offline unit test | Verified |
| P2-4 | Workflow plans, routes, retains, and prints all completed outputs | Same | Offline unit test | Verified |
| P2-5 | Final output contains user stories, product features, and engineering tasks in the required structures | Same | Prompt/static inspection; live run if key exists | Structurally verified; live run blocked |
| Q-1 | Keys are never hardcoded and generated/private files are excluded | All | Secret scan and hygiene check | Verified |
| Q-2 | Dependencies install and project compiles/tests cleanly | All | Isolated environment, `unittest`, `compileall` | Verified |
| E-1 | Live evidence for all scripts and final workflow | `outputs/` | Live execution | Blocked: no `OPENAI_API_KEY` is available |
| S-1 | Public repository is named `Udacity_MS_AI_Powered_Agentic_Workflow` | Repository | Remote/visibility check | Not authorized |

Comparable public repositories are advisory only; no external code or text is copied into this project.

## Comparative repository review

| Reference | Observed convention used for review | Project response |
|---|---|---|
| `https://github.com/MelvinJoshua1375/ai-powered-agentic-workflow-for-project-management` | Keeps matching Phase 1 and Phase 2 agent libraries; documents live output evidence separately | Agent libraries are kept byte-for-byte identical; live evidence remains explicitly blocked without credentials |
| `https://github.com/peymangraph/ai-agentic-project-management-workflow` | Includes a root README, environment exclusions, and a rubric checklist | Added root setup/run guidance, `.gitignore`, tests, and this rubric matrix |
| `https://github.com/tobiassteidle/AgenticAI_ND_P2_Agentic-Workflow-for-Project-Management` | Preserves the two-phase starter layout and documents required output structures | Preserved starter filenames and added deterministic checks for the required structures |
