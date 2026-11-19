<!-- BEGIN product-brain:docs -->
## Documentation (Product Brain)

This repository is documented in chunks with `brain docs`. The documentation vault is `docs/`; machine reports are under `.brain/docs/`.

- Read `docs/Start Here.md` first, then the notes of the area you work in. Each note names the code it owns in `covers` and the commit it was checked against in `verified-against`.
- Code is the truth. When a note and the code disagree, say so and fix one of them; `brain docs check` lists stale notes.
- Every behavioural statement carries a citation written as `path:start-end` in backticks.
- Never write secrets or values of configuration; name variables only.

Workflow, one chunk at a time: `brain docs explore`, `brain docs plan` (a person approves with `--approve`), `brain docs chunk ID`, write the explanations and diagrams, `brain docs spec` for use cases and rules, `brain docs verify ID`, then a person runs `brain docs review ID --approve`.
Diagrams follow `docs/Diagrams/Diagram Notation Guide.md`; run `brain docs diagram guide KIND` before drawing, then `brain docs diagram check` and `brain docs diagram render`.
After code changes run `brain docs drift --ask`; if new functionality is reported, ask the person whether to document it and which diagram kinds they prefer. `brain docs sync` blocks a commit that changes covered code without updating its note. Never approve a plan, a chunk or a decision yourself.

| Note | Use |
|---|---|
| `docs/brain/00 Start Here.md` | where to begin |
| `docs/brain/Reading Paths by Role.md` | reading order by role |
| `docs/brain/Vault Documentation Rules.md` | how notes are written |
| `docs/brain/Diagrams/Diagram Notation Guide.md` | how diagrams are drawn |
| `docs/brain/architecture/Chunk Plan.md` | the chunk plan |
| `docs/brain/Operations/Environment Variables.md` | environment variables |
| `docs/brain/Operations/Requirement Catalogue.md` | measures the repository enforces |
| `docs/brain/Application/Invariants Catalogue.md` | rules the code enforces |
| `docs/brain/Operations/Coverage Map.md` | which note and test reach each file |
| `docs/brain/Operations/Release Checklist.md` | how a release is made |
| `docs/brain/Operations/Rollback Runbook.md` | how to go back |
<!-- END product-brain:docs -->
