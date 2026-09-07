Goal
Build the smallest correct solution for the current requirement.
Priority:

1. simplicity
2. correctness
3. readability
4. maintainability
5. minimal files, dependencies, code, and abstractions

Use KISS and YAGNI. Prefer explicit code over indirection or speculative flexibility.

Core Rules

* Read relevant code before changing it.
* Follow existing project conventions unless this file explicitly overrides them.
* Check the skill and agent catalog at the end of this file before starting non-trivial work; use a matching one instead of improvising.
* Make the smallest coherent diff.
* Do not refactor unrelated code.
* Do not add unrequested features, configurability, fallbacks, or future-proofing.
* Reuse existing code and dependencies when they are already a good fit.
* Prefer standard language/framework features over new packages.
* Add a dependency only when it removes more complexity than it introduces.
* Validate untrusted data at system boundaries, not impossible internal states.
* Preserve existing contracts unless the task explicitly changes them.
* Never hard-code behavior only to satisfy tests.
* Never commit secrets, credentials, tokens, or environment-specific values.
* Remove temporary scripts, scratch files, and generated artifacts before finishing.

Before Coding

1. Inspect the relevant files.
2. Find the smallest existing place where the change belongs.
3. Check nearby patterns, dependencies, tests, and repository commands.
4. Implement directly before creating an abstraction.
5. Keep the diff local to the requested behavior.

Never speculate about code that has not been inspected.

Files
New files are a maintenance cost.
Create a source file only when:

* the framework requires it
* it is an independent entry point or configuration unit
* it contains a distinct responsibility with real reuse
* keeping it in the current file would mix unrelated responsibilities

Otherwise, extend the existing cohesive file.
Rules:

* Do not create a directory for one ordinary source file.
* Keep source nesting shallow; prefer at most two meaningful levels unless the framework requires more.
* Do not create generic `utils`, `helpers`, `common`, or `shared` dumping grounds.
* Name files by domain or responsibility.
* Do not create barrel/index files only to shorten imports.
* Do not split files by arbitrary line count.
* Split when responsibilities change independently or have a real reuse boundary.
* A normal feature should usually add 0–3 source files. If more are needed, simplify first.
* Prefer tiny local duplication over premature abstraction.
* Extract shared non-trivial logic when it reaches a third real use.

Architecture
Use the fewest layers that keep boundaries clear.

* Do not introduce controller/service/repository/factory layers by default.
* Add a layer only when it owns real behavior, a stable boundary, or multiple implementations.
* Keep data flow obvious from the call site.
* Prefer composition over inheritance.
* Prefer pure functions for transformations and business rules.
* Keep side effects near system boundaries.
* Avoid hidden global state and circular dependencies.
* Keep configuration centralized and explicit.
* Keep public interfaces small.

When two designs are correct, choose the one with fewer concepts, files, dependencies, and indirections.

React
Applies to `web/` (React 19 + TypeScript + Vite + Tailwind + Recharts).

* Use function components.
* Keep Components and Hooks pure.
* Never mutate props or state.
* Keep state local unless distant consumers genuinely need it.
* Store the minimum state; derive everything else during render.
* Avoid duplicated or contradictory state.
* Use `useEffect` only to synchronize with an external system.
* Do not use Effects for derived render data, normal user events, or mirroring props into state.
* Prefer event handlers for user-triggered side effects.
* Do not introduce Context when local composition or props remain simple.
* Do not introduce reducers until state transitions are genuinely complex.
* Do not create custom Hooks as one-off wrappers.
* Create custom Hooks for real reuse or a meaningful stateful/external-system boundary.
* Keep small, tightly related components in the same file.
* Extract a component when reused, independently meaningful, or materially clearer.
* Do not add memoization by default; use it for measured or clearly material performance needs.
* Prefer semantic HTML.
* Reuse the existing styling, component, state, form, and data-fetching stack.
* Preserve strict typing and avoid `any` unless unavoidable.

Python
Applies to `src/`, `scripts/`, `tests/` (pyproject-managed). Follow PEP 8 and the spirit of PEP 20: explicit, simple, flat, readable.

* Prefer functions over classes unless meaningful state, lifecycle, protocol, or polymorphism requires a class.
* Keep modules flat and domain-focused.
* Prefer straightforward control flow over clever expressions.
* Prefer the standard library when it remains clear.
* Use comprehensions only when immediately readable.
* Keep imports explicit; avoid wildcard imports.
* Avoid mutable default arguments.
* Use type hints on meaningful function and boundary contracts when they improve correctness.
* Do not add typing noise to obvious locals.
* Raise specific exceptions.
* Do not swallow exceptions.
* Catch exceptions only where they can be handled or translated meaningfully.
* Validate external input at API, file, database, queue, and third-party boundaries.
* Keep synchronous code synchronous unless concurrency has a real benefit.
* Avoid blocking I/O inside async code.
* Do not create generic base classes, registries, factories, or plugin systems for hypothetical needs.

Comments and Markdown
Application code should explain itself.

* Do not add inline comments, block comments, docstrings, JSDoc, or TSDoc.
* Exceptions: unavoidable shebangs, formatter/linter pragmas, coverage directives, or generated-file markers.
* Use precise names and small coherent units instead of comments.
* Put architecture, contracts, invariants, workflows, and non-obvious decisions in Markdown.
* Do not duplicate obvious code behavior in documentation.

Keep documentation minimal:

* `README.md`: purpose, setup, commands, environment, high-level usage
* `CLAUDE.md`: engineering rules
* `docs/architecture.md`: only when architecture cannot stay concise in `README.md`

Do not create per-feature Markdown files by default.
Update docs only when commands, architecture, public behavior, or important constraints change.
Delete stale documentation.

Testing
Test behavior, not implementation.

* Add the smallest test set that proves the change.
* Cover the main path, meaningful edge cases, and regressions.
* Prefer real behavior over excessive mocking.
* Avoid snapshots unless serialized/rendered output is the contract.
* Do not create test helpers for one-off setup.
* Keep related tests together when useful.
* Run the narrowest relevant checks while iterating.
* Before finishing, run the relevant formatter, linter, type checker, and tests supported by the repository.
* Discover commands from existing files such as `pyproject.toml`, `web/package.json`, task runners, CI, or `README.md`. Do not invent commands.

Refactoring
Refactor only when required by the task or when current structure blocks a clean implementation.
Allowed:

* remove code made obsolete by the change
* simplify touched code without changing behavior
* extract logic after a real reuse or responsibility boundary appears

Avoid:

* drive-by cleanup
* broad renames or file moves
* framework migrations
* replacing working libraries
* speculative extension points

Done
A task is done when:

* requested behavior works
* the implementation is the smallest clear solution
* no unnecessary files, dependencies, layers, or abstractions were added
* temporary files are removed
* relevant checks pass
* unrelated behavior is unchanged
* documentation changed only where necessary
* the diff is easy to explain briefly

Decision Order
Prefer:
existing file > new file
existing dependency > new dependency
function > class
local state > global state
derived value > duplicated state
direct code > abstraction
composition > inheritance
standard library > new package
clear duplication > premature reuse
simple solution > flexible solution

Skills and Agents
Everything below lives in `.claude/skills/` and `.claude/agents/`. Match the task to an entry by its trigger, don't invoke by name alone.

Entry point

* `poteto-mode` — default starting point for any non-trivial task; routes to a playbook and the skills below.

Direct-use skills

* `how` — explain how a subsystem or runtime flow works, before changing it.
* `why` — explain why something was built this way, with cited evidence.
* `teach` — combine `how` + `why` into one plain explanation.
* `recall` — rebuild recent working context before resuming a task.
* `architect` — sketch types, signatures, and module shape before writing code.
* `arena` — run N parallel attempts at a task, then merge the best parts.
* `swarm` — fan out N parallel workers over different slices, return one report.
* `interrogate` — multi-model adversarial review of a diff.
* `blast-radius` — find and prove what a small change could break elsewhere.
* `figure-it-out` — design an auditable playbook when no narrower one fits.
* `tdd` — write a failing test first, then the fix, when explicitly requested or the test path is cheap.
* `automate-me` — draft or refresh a personal "-mode" skill from your working style.
* `make-bot-ui` — build a UI whose actions wake a bot over a webhook.
* `setup-pstack` — choose which models pstack uses per role.
* `reflect` — review the transcript and turn learnings into skill edits.
* `unslop` — strip AI writing tells from any text.
* `bro` — restate the last message in plain language.
* `no-comments` — spawn Comment Sicko to strip unnecessary comments from a diff.
* `technical-writing` — apply layered doc-writing standards to docs, RFCs, PRs, commits.
* `typescript-best-practices` — best practices when reading or editing `.ts`/`.tsx`.
* `show-me-your-work` — log a reviewable decision trail for unattended or multi-phase work.
* `create-verification-skill` — generate a project-local skill that drives the app to prove behavior.
* `maintain-verification-skill` — audit and refresh an existing verification skill's feature map.

Principles (`principle-*`, used internally by `poteto-mode` — apply the matching one rather than invoking directly)

* `principle-boundary-discipline` — put validation at system boundaries; trust internal types.
* `principle-build-the-lever` — build the tool or script that does or proves the work, not manual effort.
* `principle-encode-lessons-in-structure` — turn a repeated correction into a lint or check, not more text.
* `principle-exhaust-the-design-space` — prototype 2-3 competing designs before committing on a novel decision.
* `principle-experience-first` — choose user delight over implementation convenience.
* `principle-fix-root-causes` — trace bugs to their root cause instead of guarding symptoms.
* `principle-foundational-thinking` — get core data structures right before writing logic.
* `principle-guard-the-context-window` — route bulk work to subagents; keep the main thread summarized.
* `principle-laziness-protocol` — default to deletion and the smallest change that solves it.
* `principle-make-operations-idempotent` — design operations to converge to the same end state under retries.
* `principle-migrate-callers-then-delete-legacy-apis` — migrate callers and delete the old API in one wave.
* `principle-minimize-reader-load` — collapse indirection and hidden state that make code hard to trace.
* `principle-model-the-domain` — encode domain rules in structure instead of scattered conditionals.
* `principle-never-block-on-the-human` — proceed on reversible work instead of asking permission first.
* `principle-outcome-oriented-execution` — converge straight to the target architecture during migrations.
* `principle-prove-it-works` — verify against the real artifact before declaring a task done.
* `principle-redesign-from-first-principles` — redesign as if a new requirement had been there from day one.
* `principle-separate-before-serializing-shared-state` — remove shared state before adding synchronization.
* `principle-sequence-verifiable-units` — break work into small, independently verifiable steps.
* `principle-subtract-before-you-add` — remove dead weight before building on top of it.
* `principle-type-system-discipline` — make illegal states unrepresentable in the type system.

Agents

* `Comment Sicko` — adversarially hunts down and deletes unnecessary comments from a diff.
* `poteto-agent` — routing target for `/poteto-mode`; carries the full poteto agent style across turns.
