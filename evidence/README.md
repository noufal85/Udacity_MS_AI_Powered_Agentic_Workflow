# Live execution evidence

The `live/` directory contains the actual captured standard output and standard
error from all seven Phase 1 scripts and the Phase 2 workflow. No generated
answer text was edited after capture. The manifest records exit codes,
timestamps, source-file hashes, and log hashes.

Seven PNG files render the captured Phase 1 terminal transcripts for visual
review. They are clearly labeled as transcript renders, rather than desktop
screenshots; the corresponding text files preserve the exact output.

## Model and endpoint

- Chat model: `gpt-4.1-mini`, explicitly authorized by the project owner after
  the API rejected the rubric's `gpt-3.5-turbo` model as deprecated.
- Embeddings: `text-embedding-3-large`, unchanged from the rubric.
- Endpoint: `https://api.openai.com/v1`, including the supplied RAG agent.
- Temperature: zero for chat completions.
- Credentials: passed privately through the subprocess environment; never
  written to evidence or tracked files.

The rubric's original model is still the code default. These logs demonstrate
successful execution with the documented override, rather than claiming a run
of the unavailable model. Course acceptance of the substitution is a separate
grading decision.

## Evidence map

| Criterion | Captured output |
|---|---|
| Direct prompt | `live/direct_prompt_agent.txt` |
| Persona augmentation | `live/augmented_prompt_agent.txt` |
| Supplied knowledge | `live/knowledge_augmented_prompt_agent.txt` |
| Retrieval augmentation | `live/rag_knowledge_prompt_agent.txt` |
| Evaluation and refinement | `live/evaluation_agent.txt` |
| Semantic routing | `live/routing_agent.txt` |
| Action planning | `live/action_planning_agent.txt` |
| Consolidated development plan | `live/agentic_workflow.txt` |
| Extracted final plan, without intermediate traces | `live/development_plan.txt` |
| Run metadata and integrity | `live/manifest.json` |
| Per-record structure checks | `live/validation.json` |

The knowledge demonstration intentionally supplies the false statement that
London is France's capital to show knowledge conditioning. Its output is an
exercise result, not a factual assertion. The evaluation demonstration may
revise that answer while satisfying its city-name-only criterion.

## Reviewer feedback resolution

The missing output is now captured directly from live execution. Each final
user story is checked for the literal `so that`; every feature is checked for
all four required labels; every engineering task is checked for all seven
required labels. All three consolidated headings must occur exactly once.

The first live workflow exposed the optional heading issue: steps for features
and tasks also mentioned user stories. A regression test now covers that case,
and consolidated headings follow the actual selected route. Four concise
workflow docstrings address the reviewer's other optional suggestion.

The earlier access-check document is retained as historical diagnostic evidence.
The logs in `live/` are the final runs after the route-heading correction.
