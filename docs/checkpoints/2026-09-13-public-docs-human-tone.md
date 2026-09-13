# Public documentation tone and authorship standard — 2026-09-13

Decision: before public release, the user-facing documentation must be rewritten so it reads like concise technical documentation written by a maintainer, not like a chat transcript or AI-generated explainer.

Observed problems in current public-facing drafts:

- too much explanatory padding and repetition,
- excessive sectioning and numbered prose,
- mixing user instructions with development notes, test status and project philosophy,
- obvious local-path examples presented too prominently,
- too many "expected result" blocks for trivial steps,
- unnecessary narration of design intent inside operational instructions,
- wording that sounds generated rather than maintained by a project author.

Public documentation style target:

- concise, factual, task-oriented,
- normal maintainer voice rather than assistant voice,
- explain only what helps the user make a decision or complete a step,
- examples must be path-agnostic unless explicitly marked as examples,
- no chatty reassurance, no synthetic enthusiasm, no repeated cautions,
- keep development/test caveats in DEVELOPMENT.md or dedicated status docs,
- keep README focused on what FX11 is, current capabilities, limitations and quick start,
- keep USER_GUIDE.md focused on installation/build/use,
- retain detailed checkpoints/history for transparency, but do not make them the primary user path.

Release gate: user-facing docs should be manually reviewed before treating the repository as ready for public presentation.
