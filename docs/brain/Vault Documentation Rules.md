---
title: Vault Documentation Rules
aliases: []
tags: [overview, reference]
area: navigation
status: active
audience: internal
maturity: approved
confidence: confirmed
covers: []
---

# Obsidian Vault Documentation

Canonical skill for the project vault. The Codex copy at `.codex/skills/obsidian-vault-documentation/SKILL.md` is a pointer to this file. Derivable facts (route lists, counts, harness inventories, ADR indexes, diagram source) are generated; hand-written notes explain intent and declare which code they own.

## Required Context

1. Read `CLAUDE.md` (or `AGENTS.md` for Codex) and `MEMORY.md`.
2. Start at `docs/00 Start Here.md`.
3. Read the matching syntax skill when touching its file type: `.claude/skills/obsidian-markdown/SKILL.md` for notes, `.claude/skills/obsidian-bases/SKILL.md` for `.base` files, `.claude/skills/json-canvas/SKILL.md` for `.canvas` files, `.claude/skills/obsidian-cli/SKILL.md` when the CLI is available.
4. Treat code, `prisma/schema.prisma`, route files, `MEMORY.md`, and harness files as truth when a note disagrees.

## Vault Root and Links

- The vault root is the repository root. Obsidian detects all file extensions, applies `userIgnoreFilters`, and hides `src/`, `tests/`, `scripts/`, and `prisma/` from the graph.
- Link to source with a wikilink that uses the full vault-root path and the file extension, for example `[[src/lib/cache.ts]]` or `[[prisma/schema.prisma]]`.
- Never wikilink a directory, because Obsidian cannot resolve one. Write the directory as a backticked path such as `src/lib/auth/`.
- Never wikilink a path that contains `[` or `]` (for example `src/app/api/resources/[slug]/route.ts`), because Obsidian cannot resolve them. Write it as a backticked path.
- Never wikilink `README.md`; several files share that name. Use the full path.
- Dot-folders (`.claude/`, `.codex/`, `.github/`) are not indexed by Obsidian. Never wikilink into them from hand-written notes. Use a backticked path, or link to the generated note under `docs/Harness/`.
- Link notes to each other by title or by full path when titles collide.

## Folder Map

All folders live under `docs/`. The map is fixed so generators never move files. Note names carry no number prefixes; use "and" rather than "&" in file names; link notes by basename.

| Folder | Holds |
|---|---|
| (root) | `00 Start Here.md` and `Reading Paths by Role.md`, the only root notes |
| `01 Strategy/` | Drivers, goals, capability maps, the roadmap (TOGAF phase A) |
| `02 Business/` | Processes (BPMN), conceptual models, use cases, actors, rules, the language of the domain (phase B) |
| `03 Application/` | `Software/` (modules, routes, screens, sequences, state, tests) and `Data/` (entities, ER, flows, retention) (phase C) |
| `04 Technology/` | `Infrastructure/`, `Operations/`, `Security/` (phase D) |
| `05 Motivation/` | `Requirements/` and `Risks/` (requirements management) |
| `06 Implementation and Migration/` | `Decisions/`, `Releases/`, `Governance/`, `Change/` (phases E to H) |
| Inside each layer | `Notes/`, `Diagrams/` and `Use Cases/`, and one generated `<Layer> Layer.md` that lists them |
| `Harness/` | Generated, one note per rule, skill, command, agent, hook, and reference, plus the hand-written `Harness Overview.md` |
| `Decisions/` | Generated `ADR Index.md`; the ADRs themselves stay in `docs/adr/` |
| `Diagrams/` | The diagram hub, index and notation guide; each diagram's own wrapper note lives in its layer |
| `Glossary/` | Domain language |
| `Releases/` | Release notes |
| `Archive/` | Retired notes, kept with `status: archived` |
| `Bases/` | `.base` files |
| `Canvases/` | `.canvas` files |
| `Templates/` | Note templates |

## Frontmatter Schema

Flat YAML on every durable note.

| Key | Rule |
|---|---|
| `title` | String, required |
| `aliases` | List. Old filenames go here after a rename. May be `[]` |
| `tags` | List from the controlled list below |
| `area` | `navigation`, `business`, `application`, `data`, `security`, `operations`, `harness`, `decisions`, `diagrams`, `glossary`, `releases`, `archive` |
| `status` | `draft`, `active`, `generated`, `archived`. ADRs in `docs/adr/` use `Proposed`, `Accepted`, `Superseded`, or `Deprecated` instead |
| `audience` | `public` or `internal`. Default `internal`. Notes on the admin route, env var names, rate limits, threat model, harness, or secrets handling are always `internal` |
| `covers` | List of repo-relative globs the note owns (`*` and `**`). Brackets are literal, so `src/app/api/resources/[slug]/**` matches a literal `[slug]` folder. Omit or use `[]` when the note owns no code |
| `verified-against` | Git commit SHA (7 to 40 hex chars) the note was last checked against. Replaces the forbidden `reviewed:` date |
| `generated` | Boolean `true`, only on whole-file generated notes, which must also set `status: generated` |
| `sources` | Only on diagram wrappers: list of vault-root-relative paths to `.mmd` or `.bpmn` sources (see Diagrams). Legacy single `source` string also accepted |
| `date` | ADRs only, `YYYY-MM-DD` |

Controlled tags: `adr`, `diagram`, `bpmn`, `drawio`, `mermaid`, `c4`, `erd`, `canvas`, `base`, `generated`, `template`, `harness`, `rule`, `skill`, `command`, `agent`, `hook`, `release`, `runbook`, `reference`, `overview`, `accounts`, `auth`, `mfa`, `privacy`, `security`, `caching`, `deployment`, `ci`, `search`, `seo`, `curation`, `journeys`, `library`, `glossary`, `admin`, `roadmap`. Do not invent tags.

## Generated Blocks

Generators own regions of a note, delimited by paired Obsidian comments on their own lines, outside code fences:

```
%% generated:<id> start (do not edit; run npm run docs:vault) %%
...generated content...
%% generated:<id> end %%
```

- `<id>` uses lowercase letters, digits, and hyphens.
- Hand-written text outside the markers is never touched by generators. Never edit text inside the markers by hand; fix the source or the generator and rerun.
- A note that is generated end to end sets `generated: true` and `status: generated`.
- Never copy a number, count, or list that a generator owns into hand-written prose. Link to the generated note instead.

## Diagrams

- Mermaid sources live in `docs/architecture/diagrams/*.mmd`. BPMN sources live in `docs/architecture/bpmn/*.bpmn` and draw.io sources in `docs/architecture/drawio/*.drawio`; both render to `docs/architecture/rendered/*.svg` (`npm run docs:diagrams:drawio` needs the draw.io desktop application).
- A wrapper note in `docs/Diagrams/` lists its diagrams in `sources:`, a list of vault-root-relative `.mmd` or `.bpmn` paths. One wrapper may hold several diagrams, and one source may appear in several wrappers. The older single `source:` string stays valid and uses the block id `diagram`.
- For each `.mmd` entry, the wrapper holds a generated block with id `diagram-<stem>`, where `<stem>` is the file name without the extension (`docs/architecture/diagrams/foo-bar.mmd` gives `diagram-foo-bar`). The sync script copies the `.mmd` content into a `mermaid` code fence between the markers, filling every block of a note in one run. The generator skips an entry whose marker pair is missing.
- For BPMN and draw.io, list the `.bpmn` or `.drawio` path in `sources:`, omit any marker pair, and embed the render by hand with `![[docs/architecture/rendered/<name>.svg]]`. These entries are never synced. A draw.io file name starts with `drawio-` so its render name cannot collide with a Mermaid render.
- `check-vault` rule `wrapper-source` fails when a `sources`/`source` path does not exist, when a `.mmd` entry has no marker pair, or when a `diagram-<stem>` block has no matching `sources` entry.
- `Diagrams/Diagram Index.md` counts a wrapper as covering every path in `sources` and `source`.
- Canvas nodes use repo-root-relative `file` paths. Bases are embedded with `![[docs/Bases/<name>.base#<exact view name>]]`.

## Ownership and the Docs-Sync Guard

- A note owns the code its `covers` globs match. A change to a matching path requires that note to change in the same commit.
- `.claude/hooks/docs-sync-guard.mjs` is the enforcement point. Target behaviour: it maps changed paths to owning notes through `covers` and blocks when an owning note is missing from the change. The guard rewrite lands later in this overhaul; until then it applies the older rule that any documented-surface change needs some `docs/` or `docs/adr/` update.
- Run `node --preserve-symlinks-main .claude/hooks/docs-sync-guard.mjs --finalize` before finalizing a documented-surface change.
- `DOCS_SYNC_ACK=1` is an explicit override. Use it only with a stated rationale, such as a change with no documentable effect.
- When you add a note that owns code, set `covers` and `verified-against` at the commit you checked.

## Authoring Rules

- Code is truth. Verify every claim in the file before writing it, and set `verified-against` to the commit you checked.
- Keep notes small and single-topic so agents can load them cheaply. Split a note that serves two questions.
- Link generously with wikilinks. Use callouts sparingly.
- No emojis, no em dashes, and no arrow glyphs in note prose. Write normal prose, not terse chat style.
- One-line comments only in code samples, and only when the reason is not obvious.
- Never put `.env*` values, secrets, or admin credentials in a note. Env var names live in `.claude/references/env-vars.md`.
- Keep Obsidian local pane state out of git (`.obsidian/workspace*.json` is ignored).
- Do not edit generated notes by hand: everything under `docs/Harness/` except `Harness Overview.md`, plus `Decisions/ADR Index.md`, `Diagrams/Diagram Index.md`, `Application/Routes.md`, `Data/Schema ERD.md`, and `Operations/Project Facts.md`. Run `npm run docs:vault` instead.

## Verification

- `npm.cmd run check:vault` (once present): validates frontmatter, `covers` globs, wikilinks, and generated-block pairing.
- `npm.cmd run docs:vault` (once present): regenerates generated blocks and notes. Rerun it, then confirm a second run produces no diff.
- `npm.cmd run check:harness` when files under `.claude/`, `CLAUDE.md`, `AGENTS.md`, `MEMORY.md`, `.gitignore`, or `scripts/check-harness.mjs` change.
- `npm.cmd run check:memory` when `MEMORY.md` or the coverage map changes.
- Parse every `.canvas` file as JSON and every `.base` file as YAML.
- Optional: with `obsidian` on PATH and the app running, use the Obsidian CLI to list unresolved links (see `.claude/skills/obsidian-cli/SKILL.md`).

## Layer folders

`brain docs layout` (also run by `generate`, `review`, `showcase` and the chunk export) moves each note into the folder of its layer. The layer comes from a `layer:` key in the frontmatter when present, otherwise from the diagram kind (for example `bpmn` and `erd-conceptual` are Business, `dfd` and `erd` are Data, `sequence`, `c4` and `state` are Application, `deployment` is Technology, `trust-boundary` is Security, `capability` is Strategy) or from the note's `area`. Notes that belong to no layer stay where they are. Obsidian links by title, so a move breaks no link, and generators that still name the old path are redirected to the new one. Set `layout: flat` in the configuration to turn the grouping off.
