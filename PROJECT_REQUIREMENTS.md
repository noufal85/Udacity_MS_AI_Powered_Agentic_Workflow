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
| P1-1 | Direct agent uses `gpt-3.5-turbo`, a user message only, and returns text | `phase_1/workflow_agents/base_agents.py` | Offline unit test; live log | Default contract verified; live runs use owner-authorized `gpt-4.1-mini` override |
| P1-2 | Augmented agent stores and applies its persona while resetting context | Same | Offline unit test | Verified |
| P1-3 | Knowledge agent stores persona and knowledge and restricts its answer to supplied knowledge | Same | Offline unit test | Verified |
| P1-4 | Supplied RAG agent remains available | Same | Import, regression test, static check | Verified |
| P1-5 | Evaluation agent iterates, uses temperature 0, and returns exactly `final_response`, `evaluation`, `iterations` | Same | Offline unit tests | Verified |
| P1-6 | Router embeds with `text-embedding-3-large`, selects by cosine similarity, and calls the selected route | Same | Offline unit test | Verified |
| P1-7 | Action planner returns a clean list of steps | Same | Offline unit test | Verified |
| P1-8 | Seven runnable demonstration scripts load credentials from the environment | `phase_1/*.py` | Seven successful live logs and PNG transcript renders in `evidence/live/` | Verified with documented model override |
| P2-1 | Product specification is loaded and four required classes are imported | `phase_2/agentic_workflow.py` | Offline unit/static test | Verified |
| P2-2 | Three worker/evaluator pairs and three semantic routes are configured | Same | Offline unit test | Verified |
| P2-3 | Support functions call their evaluation agents with the workflow step | Same | Offline unit test | Verified |
| P2-4 | Workflow plans, routes, retains, and prints all completed outputs | Same | Offline unit test | Verified |
| P2-5 | Final output contains user stories, product features, and engineering tasks in the required structures | Same | `evidence/live/agentic_workflow.txt` and `validation.json` | Verified: 15 stories, 6 features, 10 tasks; documented model override |
| Q-1 | Keys are never hardcoded and generated/private files are excluded | All | Secret scan and hygiene check | Verified |
| Q-2 | Dependencies install and project compiles/tests cleanly | All | Isolated environment, `unittest`, `compileall` | Verified |
| E-1 | Live evidence for all scripts and final workflow | `evidence/live/` | Eight successful live runs, output inspection, manifest and structure validation | Verified with documented model override; original access failure retained in `evidence/API_ACCESS_CHECK.md` |
| S-1 | Public repository is named `Udacity_MS_AI_Powered_Agentic_Workflow` | Repository | Remote/visibility check | Verified: `noufal85/Udacity_MS_AI_Powered_Agentic_Workflow` |

Comparable public repositories are advisory only; no external code or text is copied into this project.

## Comparative repository review

| Reference | Observed convention used for review | Project response |
|---|---|---|
| `https://github.com/MelvinJoshua1375/ai-powered-agentic-workflow-for-project-management` | Keeps matching Phase 1 and Phase 2 agent libraries; documents live output evidence separately | Agent libraries are kept byte-for-byte identical; actual live logs are included separately |
| `https://github.com/peymangraph/ai-agentic-project-management-workflow` | Includes a root README, environment exclusions, and a rubric checklist | Added root setup/run guidance, `.gitignore`, tests, and this rubric matrix |
| `https://github.com/tobiassteidle/AgenticAI_ND_P2_Agentic-Workflow-for-Project-Management` | Preserves the two-phase starter layout and documents required output structures | Preserved starter filenames and added deterministic checks for the required structures |

### Resubmission comparison and independent review

Two independent review agents checked the feedback and the full thirteen-criterion
rubric against baseline `0356c56`. Both verified the eight successful runs,
manifest integrity, required output structures, route-based headings, and four
docstrings. The rubric reviewer identified an additional literal requirement:
the augmented-agent output must explain the knowledge source and persona impact.
A failing regression test reproduced that omission, the script now prints both
explanations, and its live log and rendered transcript were recaptured. The
model substitution remains disclosed as a course approval caveat.

The following public repositories were inspected through GitHub's API at the
listed revisions. Repository trees and README files were used for comparison;
no external implementation or prose was copied. Their grading outcomes were
not verified.

| Repository | Inspected revision | Observation and conclusion |
|---|---|---|
| `MelvinJoshua1375/ai-powered-agentic-workflow-for-project-management` | `0ffc160d9e3127a0861a426cb25a152ccc514798` | Two phase directories and eight per-script output files match the expected organization. Its README describes those logs as simulated, so it is not a standard for successful live-execution evidence. |
| `peymangraph/ai-agentic-project-management-workflow` | `ffece31f8402cb7c5ce12b2f987e6b8a09f365f0` | Separate submission outputs, a rubric checklist, and explicit story/feature/task formats support this project's evidence map and field checks. Its root README contains an outdated development-status statement, illustrating why actual artifacts matter more than status prose. |
| `tobiassteidle/AgenticAI_ND_P2_Agentic-Workflow-for-Project-Management` | `8c8c70b768664451ef98116f5641ce173c0c2462` | Preserves the starter layout and stores Phase 1 and Phase 2 output text separately. Its tracked RAG intermediate CSVs are not adopted here because the assignment excludes datasets from the submission. |

The comparison supports the two-phase structure, seven demonstration captures,
complete workflow capture, reproducible setup instructions, and evidence index.
The supplied rubric and reviewer feedback remain authoritative, including the
need to disclose the replacement model rather than claiming the original ran.
