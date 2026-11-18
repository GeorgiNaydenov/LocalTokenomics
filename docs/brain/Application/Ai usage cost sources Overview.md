---
title: Ai usage cost sources Overview
aliases: []
tags: [module, overview]
area: application
status: draft
audience: internal
maturity: draft
confidence: inferred
covers: [src/ai_usage_cost/sources/**]
verified-against: e5313fbd7062
chunk: ch-localtokenomics-src-ai-usage-cost-sources
---

# Ai usage cost sources Overview

What Ai usage cost sources is made of and how it connects to the rest of the code.

## How it works

Ai usage cost sources holds 22 source files and 4722 lines, with 2 entities, 515 tests that live in it or import its files. The most depended-on files are `src/ai_usage_cost/sources/base.py`, `src/ai_usage_cost/sources/__init__.py`, `src/ai_usage_cost/sources/claude_code.py`. It uses Ai usage cost Overview. It is used by Ai usage cost Overview.

The purpose column quotes each file's own header comment where it has one. Every file is cited by its full line range, and every public name by the line that declares it.

### What a reader is

A reader is one module that holds a single module level `SOURCE` value of type `Source`, a frozen dataclass. `src/ai_usage_cost/sources/claude_code.py:672` `Source` carries an id, a label, a map of client names, a function returning the default root paths, a function listing the files under one root, a `parse` function that yields usage events from one file, a `token_data` flag, a display path, and optional span, capability and resume hooks. `src/ai_usage_cost/sources/base.py:17-40`

`token_data` is either `full` or `session`. `src/ai_usage_cost/sources/base.py:14` Readers that can only see that a conversation happened, not how many tokens it used, declare `session` and emit events with `tokens=None`. Examples are Cursor, Windsurf, Dyad, Jan and Ollama. `src/ai_usage_cost/sources/cursor.py:72-83` `src/ai_usage_cost/sources/ollama_app.py:25-43` Readers that find real token counts, such as Claude Code, Codex, Gemini CLI and Grok Build, declare `full`. `src/ai_usage_cost/sources/claude_code.py:672-678` `src/ai_usage_cost/sources/grok_build.py:113-121`

Each reader repeats the same four steps: find candidate roots, list the files under a root, read records, and map them to a `UsageEvent` with a model, a timestamp, a session id, a request id, a project and a title. `src/ai_usage_cost/sources/claude_code.py:34-110` The shared helpers in the base module do the file reading, so a reader holds only the format knowledge, and the shared helpers live in one place. `src/ai_usage_cost/sources/base.py:69-176`

### Shared helpers

- `read_json_lines` and `read_json_records` read a JSON Lines file, skip blank lines, count lines that fail to parse and add one warning per file. `read_json_records` also returns the byte offset and length of each record and can start from a byte offset. `src/ai_usage_cost/sources/base.py:69-114`
- `read_sqlite` opens a database through a read only URI, returns no rows when the file is missing, and turns a SQLite error into a warning instead of a crash. `src/ai_usage_cost/sources/base.py:117-129`
- `jsonl_files` finds every `*.jsonl` under a root and `single_file` treats the root itself as the one file. `src/ai_usage_cost/sources/base.py:132-137`
- `parse_timestamp` accepts seconds, milliseconds or an ISO string, and falls back to the file modification time. `src/ai_usage_cost/sources/base.py:140-156`
- `project_of` takes the last path segment of a working directory, and `title_of` builds the folder fallback title from the project and the session id. `src/ai_usage_cost/sources/base.py:159-176`

### Where each reader looks

Roots are computed per machine, never configured in the repository. Several readers read an environment variable by name to move the root: `GEMINI_CLI_HOME`, `COPILOT_HOME`, `GROK_HOME`, `MUSE_DATA_DIR`, `QWEN_RUNTIME_DIR`, `QWEN_HOME` and the Cline directory variables. `src/ai_usage_cost/sources/gemini_cli.py:31-35` `src/ai_usage_cost/sources/copilot_cli.py:61-64` `src/ai_usage_cost/sources/grok_build.py:14-17` `src/ai_usage_cost/sources/muse_code.py:59-65` `src/ai_usage_cost/sources/qwen_code.py:30-35` `src/ai_usage_cost/sources/cline.py:123-132`

| Reader id | What it reads | Token data |
|---|---|---|
| claude-code | JSONL files under the Claude projects folders of the home directory; assistant records with a `usage` object `src/ai_usage_cost/sources/claude_code.py:34-37` `src/ai_usage_cost/sources/claude_code.py:71-86` | full |
| codex | Rollout JSONL files under the `.codex` sessions folder; `token_count` and `token_usage_record` payloads `src/ai_usage_cost/sources/codex.py:46-47` `src/ai_usage_cost/sources/codex.py:169-178` | full |
| gemini-cli | `chats/session-*.jsonl` and older `session-*.json` under the `.gemini` tmp folder `src/ai_usage_cost/sources/gemini_cli.py:38-54` | full |
| `copilot-chat` | `session-store.db` of the VS Code family `github.copilot-chat` extension; one event per turn without tokens `src/ai_usage_cost/sources/copilot_chat.py:16-59` | session |
| copilot-cli | `events.jsonl` under `session-state`; per model usage taken from `session.shutdown` metrics `src/ai_usage_cost/sources/copilot_cli.py:61-72` | session |
| `cursor` | `state.vscdb` databases, table `cursorDiskKV`, keys `composerData:%` `src/ai_usage_cost/sources/cursor.py:30-62` | session |
| `windsurf` | `state.vscdb`, table `ItemTable`, key `cascade.chatdata` `src/ai_usage_cost/sources/windsurf.py:15` `src/ai_usage_cost/sources/windsurf.py:33` `src/ai_usage_cost/sources/windsurf.py:45-48` | session |
| ollama-app | Ollama `db.sqlite`, assistant rows of `messages` `src/ai_usage_cost/sources/ollama_app.py:13-31` | session |
| `dyad` | Dyad `sqlite.db`, assistant rows of `messages` joined to chats and apps `src/ai_usage_cost/sources/dyad.py:24-33` | session |
| `jan` | `messages.jsonl` per thread under the Jan data folder `src/ai_usage_cost/sources/jan.py:16-38` | session |
| grok-build | `updates.jsonl` under the Grok home `sessions` folder; `turn_completed` updates `src/ai_usage_cost/sources/grok_build.py:14-35` | full |
| `antigravity` | Transcript logs under `~/.gemini/antigravity/brain`; spans only, no tokens or cost `src/ai_usage_cost/sources/antigravity.py:44-45` `src/ai_usage_cost/sources/antigravity.py:297-314` | session |
| openai-compat | JSONL files from a root the user passes; records with a `usage` object `src/ai_usage_cost/sources/openai_compat.py:11-25` | full |
| cline, roo-code, kilo-code-legacy | `ui_messages.json` task files and Cline SDK `*.messages.json` files `src/ai_usage_cost/sources/cline.py:139-149` | full |
| `opencode`, `kilo-code` | SQLite `opencode.db` or `kilo.db`, `step-finish` parts `src/ai_usage_cost/sources/opencode.py:1-8` `src/ai_usage_cost/sources/kilo_code.py:5-11` | full |
| qwen-code | per project `chats` folder session JSONL, assistant `usageMetadata` `src/ai_usage_cost/sources/qwen_code.py:1-8` | full |
| muse-code | `session.jsonl` files, `model_completed` events `src/ai_usage_cost/sources/muse_code.py:18-21` `src/ai_usage_cost/sources/muse_code.py:68-73` | full |

The OpenAI-compatible reader returns no default roots at all and needs `--root openai-compat=PATH`. `src/ai_usage_cost/sources/openai_compat.py:11-12` `src/ai_usage_cost/sources/openai_compat.py:88`

### Format notes worth knowing

- Claude Code splits cache writes into 5 minute and 1 hour buckets and reads the thinking token count separately. `src/ai_usage_cost/sources/claude_code.py:623-642` Records whose model is missing or marked synthetic are dropped. `src/ai_usage_cost/sources/claude_code.py:80-82` Claude Code is the only reader that declares `parse_resume`, so a log that only grew is read from its last offset. `src/ai_usage_cost/sources/claude_code.py:43-50` `src/ai_usage_cost/sources/claude_code.py:672-678`
- Codex skips a `token_count` whose total did not change, because Codex repeats such records on rate limit updates. `src/ai_usage_cost/sources/codex.py:194-197` It also works out how many tokens a forked thread inherited from its parent. `src/ai_usage_cost/sources/codex.py:181-189`
- Gemini CLI replays an append only operation log and counts every distinct billed message id once, including messages later rewound. `src/ai_usage_cost/sources/gemini_cli.py:1-15`
- Copilot CLI emits the difference between consecutive shutdown totals per model, and counts no compaction calls by default. `src/ai_usage_cost/sources/copilot_cli.py:7-17` `src/ai_usage_cost/sources/copilot_cli.py:55-58`
- The OpenCode reader never selects prompt or response text, and it lists the `-wal` file next to the database only as a change trigger. `src/ai_usage_cost/sources/opencode.py:19-22`
- The Cline reader drops the `request` prompt text the moment it parses the usage string, and never stores or logs it. `src/ai_usage_cost/sources/cline.py:5-8`
- Roo Code and Kilo Code legacy are thin modules that call the Cline `make_source` with their own spec. `src/ai_usage_cost/sources/roo_code.py:5-29` `src/ai_usage_cost/sources/kilo_legacy.py:15-33` Kilo Code v7 reuses the OpenCode `make_source`. `src/ai_usage_cost/sources/kilo_code.py:5-11`

### Experimental readers

`Source.experimental` marks a parser built from the tool's source and synthetic fixtures but not yet checked against a real session. It surfaces as a badge so the numbers are read with that caveat. `src/ai_usage_cost/sources/base.py:29-31` The readers that set it are Gemini CLI, Copilot CLI, Muse Code and Qwen Code directly, and OpenCode, Kilo Code, Cline, Roo Code and Kilo Code legacy through their shared `make_source` functions. `src/ai_usage_cost/sources/gemini_cli.py:214-225` `src/ai_usage_cost/sources/copilot_cli.py:264-275` `src/ai_usage_cost/sources/muse_code.py:284-295` `src/ai_usage_cost/sources/qwen_code.py:163-175` `src/ai_usage_cost/sources/opencode.py:324-343` `src/ai_usage_cost/sources/cline.py:409-430` The Copilot CLI and Muse Code module headers say plainly that no real log was available to check against. `src/ai_usage_cost/sources/copilot_cli.py:3-5` `src/ai_usage_cost/sources/muse_code.py:1-7` The Cline module also lists token meaning per source as unverified. `src/ai_usage_cost/sources/cline.py:23-26`

### How the pipeline picks readers

`registry()` walks every module in the package except `base`, imports it, and keeps the module's `SOURCE` when it is a `Source`. Adding a reader therefore means adding a module, with no list to edit. The result is sorted by id. `src/ai_usage_cost/sources/__init__.py:11-20` `client_labels()` merges the client name maps of all readers. `src/ai_usage_cost/sources/__init__.py:23-27`

The `analyze` function passes every registered reader, with any user roots, to `store.ingest`. `src/ai_usage_cost/pipeline.py:166-185` For each reader the store keeps only roots that exist, lists their files, and skips a file whose modification time, size and parser version match the stored row. `src/ai_usage_cost/sources/base.py:47-49` `src/ai_usage_cost/store.py:218-231` A file that only grew, whose reader has `parse_resume`, is read from its stored offset when the boundary hash still matches. Every other changed file is parsed again in full. `src/ai_usage_cost/store.py:234-255` After parsing, the store replaces the file's rows and its file record. `src/ai_usage_cost/store.py:262-290`

After ingest, `_sources_of` builds one `SourceInfo` per registered reader with its label, token data, root hint, files found, capabilities and `experimental` flag, and marks it detected when files were found. `src/ai_usage_cost/pipeline.py:141-163` The web page lists verified readers first and experimental ones after. `web/src/Sources.tsx:36-38`

`base.scan` is a second, store free way to run one reader: it skips missing roots, parses each file, and turns an `OSError` into a warning. `src/ai_usage_cost/sources/base.py:52-66`

## Reference

%% generated:chunk-files start (do not edit; run brain docs generate) %%
### Files

| File | Purpose | Lines | Imports | Imported by | Code |
|---|---|---|---|---|---|
| `src/ai_usage_cost/sources/__init__.py` | - | 27 | 1 | 13 | [[src/ai_usage_cost/sources/__init__.py]] `src/ai_usage_cost/sources/__init__.py:1-27` |
| `src/ai_usage_cost/sources/antigravity.py` | - | 314 | 3 | 2 | [[src/ai_usage_cost/sources/antigravity.py]] `src/ai_usage_cost/sources/antigravity.py:1-314` |
| `src/ai_usage_cost/sources/base.py` | - | 176 | 2 | 28 | [[src/ai_usage_cost/sources/base.py]] `src/ai_usage_cost/sources/base.py:1-176` |
| `src/ai_usage_cost/sources/claude_code.py` | - | 690 | 3 | 3 | [[src/ai_usage_cost/sources/claude_code.py]] `src/ai_usage_cost/sources/claude_code.py:1-690` |
| `src/ai_usage_cost/sources/cline.py` | - | 442 | 3 | 3 | [[src/ai_usage_cost/sources/cline.py]] `src/ai_usage_cost/sources/cline.py:1-442` |
| `src/ai_usage_cost/sources/codex.py` | - | 962 | 3 | 2 | [[src/ai_usage_cost/sources/codex.py]] `src/ai_usage_cost/sources/codex.py:1-962` |
| `src/ai_usage_cost/sources/copilot_chat.py` | - | 72 | 3 | 1 | [[src/ai_usage_cost/sources/copilot_chat.py]] `src/ai_usage_cost/sources/copilot_chat.py:1-72` |
| `src/ai_usage_cost/sources/copilot_cli.py` | - | 275 | 3 | 1 | [[src/ai_usage_cost/sources/copilot_cli.py]] `src/ai_usage_cost/sources/copilot_cli.py:1-275` |
| `src/ai_usage_cost/sources/cursor.py` | - | 97 | 3 | 1 | [[src/ai_usage_cost/sources/cursor.py]] `src/ai_usage_cost/sources/cursor.py:1-97` |
| `src/ai_usage_cost/sources/dyad.py` | - | 64 | 3 | 1 | [[src/ai_usage_cost/sources/dyad.py]] `src/ai_usage_cost/sources/dyad.py:1-64` |
| `src/ai_usage_cost/sources/gemini_cli.py` | Gemini CLI (google-gemini/gemini-cli) session logs. | 225 | 3 | 1 | [[src/ai_usage_cost/sources/gemini_cli.py]] `src/ai_usage_cost/sources/gemini_cli.py:1-225` |
| `src/ai_usage_cost/sources/grok_build.py` | - | 123 | 3 | 1 | [[src/ai_usage_cost/sources/grok_build.py]] `src/ai_usage_cost/sources/grok_build.py:1-123` |
| `src/ai_usage_cost/sources/jan.py` | - | 110 | 3 | 1 | [[src/ai_usage_cost/sources/jan.py]] `src/ai_usage_cost/sources/jan.py:1-110` |
| `src/ai_usage_cost/sources/kilo_code.py` | Kilo Code v7 -- an OpenCode fork storing kilo.db; same parser, different roots. | 17 | 1 | 1 | [[src/ai_usage_cost/sources/kilo_code.py]] `src/ai_usage_cost/sources/kilo_code.py:1-17` |
| `src/ai_usage_cost/sources/kilo_legacy.py` | Kilo Code legacy v5 task dirs: see cline.py for the format. | 33 | 1 | 1 | [[src/ai_usage_cost/sources/kilo_legacy.py]] `src/ai_usage_cost/sources/kilo_legacy.py:1-33` |
| `src/ai_usage_cost/sources/muse_code.py` | - | 295 | 3 | 1 | [[src/ai_usage_cost/sources/muse_code.py]] `src/ai_usage_cost/sources/muse_code.py:1-295` |
| `src/ai_usage_cost/sources/ollama_app.py` | - | 56 | 3 | 1 | [[src/ai_usage_cost/sources/ollama_app.py]] `src/ai_usage_cost/sources/ollama_app.py:1-56` |
| `src/ai_usage_cost/sources/openai_compat.py` | - | 96 | 3 | 1 | [[src/ai_usage_cost/sources/openai_compat.py]] `src/ai_usage_cost/sources/openai_compat.py:1-96` |
| `src/ai_usage_cost/sources/opencode.py` | OpenCode (anomalyco/opencode, formerly sst/opencode) -- SQLite opencode.db. | 352 | 3 | 2 | [[src/ai_usage_cost/sources/opencode.py]] `src/ai_usage_cost/sources/opencode.py:1-352` |
| `src/ai_usage_cost/sources/qwen_code.py` | Qwen Code (QwenLM/qwen-code, a Gemini CLI fork) session logs. | 175 | 3 | 1 | [[src/ai_usage_cost/sources/qwen_code.py]] `src/ai_usage_cost/sources/qwen_code.py:1-175` |
| `src/ai_usage_cost/sources/roo_code.py` | Roo Code (final release 3.53.0, archived 2026-05-15): see cline.py for the format. | 29 | 1 | 1 | [[src/ai_usage_cost/sources/roo_code.py]] `src/ai_usage_cost/sources/roo_code.py:1-29` |
| `src/ai_usage_cost/sources/windsurf.py` | - | 92 | 3 | 1 | [[src/ai_usage_cost/sources/windsurf.py]] `src/ai_usage_cost/sources/windsurf.py:1-92` |
%% generated:chunk-files end %%

%% generated:chunk-interface start (do not edit; run brain docs generate) %%
### Public interface

| Name | Kind | File | Code |
|---|---|---|---|
| `Source` | class | `src/ai_usage_cost/sources/base.py` | [[src/ai_usage_cost/sources/base.py]] `src/ai_usage_cost/sources/base.py:18` |
| `present_roots` | function | `src/ai_usage_cost/sources/base.py` | [[src/ai_usage_cost/sources/base.py]] `src/ai_usage_cost/sources/base.py:47` |
| `scan` | function | `src/ai_usage_cost/sources/base.py` | [[src/ai_usage_cost/sources/base.py]] `src/ai_usage_cost/sources/base.py:52` |
| `read_json_lines` | function | `src/ai_usage_cost/sources/base.py` | [[src/ai_usage_cost/sources/base.py]] `src/ai_usage_cost/sources/base.py:69` |
| `read_json_records` | function | `src/ai_usage_cost/sources/base.py` | [[src/ai_usage_cost/sources/base.py]] `src/ai_usage_cost/sources/base.py:87` |
| `read_sqlite` | function | `src/ai_usage_cost/sources/base.py` | [[src/ai_usage_cost/sources/base.py]] `src/ai_usage_cost/sources/base.py:117` |
| `jsonl_files` | function | `src/ai_usage_cost/sources/base.py` | [[src/ai_usage_cost/sources/base.py]] `src/ai_usage_cost/sources/base.py:132` |
| `single_file` | function | `src/ai_usage_cost/sources/base.py` | [[src/ai_usage_cost/sources/base.py]] `src/ai_usage_cost/sources/base.py:136` |
| `parse_timestamp` | function | `src/ai_usage_cost/sources/base.py` | [[src/ai_usage_cost/sources/base.py]] `src/ai_usage_cost/sources/base.py:140` |
| `project_of` | function | `src/ai_usage_cost/sources/base.py` | [[src/ai_usage_cost/sources/base.py]] `src/ai_usage_cost/sources/base.py:159` |
| `as_int` | function | `src/ai_usage_cost/sources/base.py` | [[src/ai_usage_cost/sources/base.py]] `src/ai_usage_cost/sources/base.py:165` |
| `title_of` | function | `src/ai_usage_cost/sources/base.py` | [[src/ai_usage_cost/sources/base.py]] `src/ai_usage_cost/sources/base.py:169` |
| `registry` | function | `src/ai_usage_cost/sources/__init__.py` | [[src/ai_usage_cost/sources/__init__.py]] `src/ai_usage_cost/sources/__init__.py:11` |
| `client_labels` | function | `src/ai_usage_cost/sources/__init__.py` | [[src/ai_usage_cost/sources/__init__.py]] `src/ai_usage_cost/sources/__init__.py:23` |
| `default_roots` | function | `src/ai_usage_cost/sources/claude_code.py` | [[src/ai_usage_cost/sources/claude_code.py]] `src/ai_usage_cost/sources/claude_code.py:34` |
| `parse` | function | `src/ai_usage_cost/sources/claude_code.py` | [[src/ai_usage_cost/sources/claude_code.py]] `src/ai_usage_cost/sources/claude_code.py:39` |
| `parse_resume` | function | `src/ai_usage_cost/sources/claude_code.py` | [[src/ai_usage_cost/sources/claude_code.py]] `src/ai_usage_cost/sources/claude_code.py:43` |
| `spans` | function | `src/ai_usage_cost/sources/claude_code.py` | [[src/ai_usage_cost/sources/claude_code.py]] `src/ai_usage_cost/sources/claude_code.py:113` |
| `Spec` | class | `src/ai_usage_cost/sources/cline.py` | [[src/ai_usage_cost/sources/cline.py]] `src/ai_usage_cost/sources/cline.py:82` |
| `vscode_bases` | function | `src/ai_usage_cost/sources/cline.py` | [[src/ai_usage_cost/sources/cline.py]] `src/ai_usage_cost/sources/cline.py:95` |
| `task_roots` | function | `src/ai_usage_cost/sources/cline.py` | [[src/ai_usage_cost/sources/cline.py]] `src/ai_usage_cost/sources/cline.py:108` |
| `sdk_sessions_root` | function | `src/ai_usage_cost/sources/cline.py` | [[src/ai_usage_cost/sources/cline.py]] `src/ai_usage_cost/sources/cline.py:123` |
| `cline_roots` | function | `src/ai_usage_cost/sources/cline.py` | [[src/ai_usage_cost/sources/cline.py]] `src/ai_usage_cost/sources/cline.py:135` |
| `data_files` | function | `src/ai_usage_cost/sources/cline.py` | [[src/ai_usage_cost/sources/cline.py]] `src/ai_usage_cost/sources/cline.py:139` |
| `parse` | function | `src/ai_usage_cost/sources/cline.py` | [[src/ai_usage_cost/sources/cline.py]] `src/ai_usage_cost/sources/cline.py:152` |
| `make_source` | function | `src/ai_usage_cost/sources/cline.py` | [[src/ai_usage_cost/sources/cline.py]] `src/ai_usage_cost/sources/cline.py:409` |
| `default_roots` | function | `src/ai_usage_cost/sources/antigravity.py` | [[src/ai_usage_cost/sources/antigravity.py]] `src/ai_usage_cost/sources/antigravity.py:44` |
| `antigravity_files` | function | `src/ai_usage_cost/sources/antigravity.py` | [[src/ai_usage_cost/sources/antigravity.py]] `src/ai_usage_cost/sources/antigravity.py:48` |
| `parse` | function | `src/ai_usage_cost/sources/antigravity.py` | [[src/ai_usage_cost/sources/antigravity.py]] `src/ai_usage_cost/sources/antigravity.py:62` |
| `spans` | function | `src/ai_usage_cost/sources/antigravity.py` | [[src/ai_usage_cost/sources/antigravity.py]] `src/ai_usage_cost/sources/antigravity.py:91` |
| `default_roots` | function | `src/ai_usage_cost/sources/codex.py` | [[src/ai_usage_cost/sources/codex.py]] `src/ai_usage_cost/sources/codex.py:46` |
| `parse` | function | `src/ai_usage_cost/sources/codex.py` | [[src/ai_usage_cost/sources/codex.py]] `src/ai_usage_cost/sources/codex.py:107` |
| `spans` | function | `src/ai_usage_cost/sources/codex.py` | [[src/ai_usage_cost/sources/codex.py]] `src/ai_usage_cost/sources/codex.py:246` |
| `make_roots` | function | `src/ai_usage_cost/sources/opencode.py` | [[src/ai_usage_cost/sources/opencode.py]] `src/ai_usage_cost/sources/opencode.py:69` |
| `make_files` | function | `src/ai_usage_cost/sources/opencode.py` | [[src/ai_usage_cost/sources/opencode.py]] `src/ai_usage_cost/sources/opencode.py:88` |
| `make_parse` | function | `src/ai_usage_cost/sources/opencode.py` | [[src/ai_usage_cost/sources/opencode.py]] `src/ai_usage_cost/sources/opencode.py:154` |
| `make_source` | function | `src/ai_usage_cost/sources/opencode.py` | [[src/ai_usage_cost/sources/opencode.py]] `src/ai_usage_cost/sources/opencode.py:324` |
| `default_roots` | function | `src/ai_usage_cost/sources/copilot_chat.py` | [[src/ai_usage_cost/sources/copilot_chat.py]] `src/ai_usage_cost/sources/copilot_chat.py:16` |
| `parse` | function | `src/ai_usage_cost/sources/copilot_chat.py` | [[src/ai_usage_cost/sources/copilot_chat.py]] `src/ai_usage_cost/sources/copilot_chat.py:32` |
| `default_roots` | function | `src/ai_usage_cost/sources/copilot_cli.py` | [[src/ai_usage_cost/sources/copilot_cli.py]] `src/ai_usage_cost/sources/copilot_cli.py:61` |
| `session_files` | function | `src/ai_usage_cost/sources/copilot_cli.py` | [[src/ai_usage_cost/sources/copilot_cli.py]] `src/ai_usage_cost/sources/copilot_cli.py:67` |
| `parse` | function | `src/ai_usage_cost/sources/copilot_cli.py` | [[src/ai_usage_cost/sources/copilot_cli.py]] `src/ai_usage_cost/sources/copilot_cli.py:75` |
| `default_roots` | function | `src/ai_usage_cost/sources/cursor.py` | [[src/ai_usage_cost/sources/cursor.py]] `src/ai_usage_cost/sources/cursor.py:17` |
| `cursor_files` | function | `src/ai_usage_cost/sources/cursor.py` | [[src/ai_usage_cost/sources/cursor.py]] `src/ai_usage_cost/sources/cursor.py:30` |
| `parse` | function | `src/ai_usage_cost/sources/cursor.py` | [[src/ai_usage_cost/sources/cursor.py]] `src/ai_usage_cost/sources/cursor.py:54` |
| `default_roots` | function | `src/ai_usage_cost/sources/dyad.py` | [[src/ai_usage_cost/sources/dyad.py]] `src/ai_usage_cost/sources/dyad.py:13` |
| `parse` | function | `src/ai_usage_cost/sources/dyad.py` | [[src/ai_usage_cost/sources/dyad.py]] `src/ai_usage_cost/sources/dyad.py:24` |
| `default_roots` | function | `src/ai_usage_cost/sources/gemini_cli.py` | [[src/ai_usage_cost/sources/gemini_cli.py]] `src/ai_usage_cost/sources/gemini_cli.py:31` |
| `session_files` | function | `src/ai_usage_cost/sources/gemini_cli.py` | [[src/ai_usage_cost/sources/gemini_cli.py]] `src/ai_usage_cost/sources/gemini_cli.py:38` |
| `parse` | function | `src/ai_usage_cost/sources/gemini_cli.py` | [[src/ai_usage_cost/sources/gemini_cli.py]] `src/ai_usage_cost/sources/gemini_cli.py:172` |
| `default_roots` | function | `src/ai_usage_cost/sources/grok_build.py` | [[src/ai_usage_cost/sources/grok_build.py]] `src/ai_usage_cost/sources/grok_build.py:14` |
| `session_files` | function | `src/ai_usage_cost/sources/grok_build.py` | [[src/ai_usage_cost/sources/grok_build.py]] `src/ai_usage_cost/sources/grok_build.py:20` |
| `parse` | function | `src/ai_usage_cost/sources/grok_build.py` | [[src/ai_usage_cost/sources/grok_build.py]] `src/ai_usage_cost/sources/grok_build.py:24` |
| `default_roots` | function | `src/ai_usage_cost/sources/jan.py` | [[src/ai_usage_cost/sources/jan.py]] `src/ai_usage_cost/sources/jan.py:16` |
| `jan_files` | function | `src/ai_usage_cost/sources/jan.py` | [[src/ai_usage_cost/sources/jan.py]] `src/ai_usage_cost/sources/jan.py:28` |
| `parse` | function | `src/ai_usage_cost/sources/jan.py` | [[src/ai_usage_cost/sources/jan.py]] `src/ai_usage_cost/sources/jan.py:32` |
| `default_roots` | function | `src/ai_usage_cost/sources/kilo_legacy.py` | [[src/ai_usage_cost/sources/kilo_legacy.py]] `src/ai_usage_cost/sources/kilo_legacy.py:22` |
| `default_roots` | function | `src/ai_usage_cost/sources/muse_code.py` | [[src/ai_usage_cost/sources/muse_code.py]] `src/ai_usage_cost/sources/muse_code.py:59` |
| `session_files` | function | `src/ai_usage_cost/sources/muse_code.py` | [[src/ai_usage_cost/sources/muse_code.py]] `src/ai_usage_cost/sources/muse_code.py:68` |
| `parse` | function | `src/ai_usage_cost/sources/muse_code.py` | [[src/ai_usage_cost/sources/muse_code.py]] `src/ai_usage_cost/sources/muse_code.py:205` |
| `default_roots` | function | `src/ai_usage_cost/sources/ollama_app.py` | [[src/ai_usage_cost/sources/ollama_app.py]] `src/ai_usage_cost/sources/ollama_app.py:13` |
| `parse` | function | `src/ai_usage_cost/sources/ollama_app.py` | [[src/ai_usage_cost/sources/ollama_app.py]] `src/ai_usage_cost/sources/ollama_app.py:25` |
| `default_roots` | function | `src/ai_usage_cost/sources/openai_compat.py` | [[src/ai_usage_cost/sources/openai_compat.py]] `src/ai_usage_cost/sources/openai_compat.py:11` |
| `parse` | function | `src/ai_usage_cost/sources/openai_compat.py` | [[src/ai_usage_cost/sources/openai_compat.py]] `src/ai_usage_cost/sources/openai_compat.py:15` |
| `default_roots` | function | `src/ai_usage_cost/sources/qwen_code.py` | [[src/ai_usage_cost/sources/qwen_code.py]] `src/ai_usage_cost/sources/qwen_code.py:30` |
| `session_files` | function | `src/ai_usage_cost/sources/qwen_code.py` | [[src/ai_usage_cost/sources/qwen_code.py]] `src/ai_usage_cost/sources/qwen_code.py:38` |
| `parse` | function | `src/ai_usage_cost/sources/qwen_code.py` | [[src/ai_usage_cost/sources/qwen_code.py]] `src/ai_usage_cost/sources/qwen_code.py:95` |
| `spans` | function | `src/ai_usage_cost/sources/qwen_code.py` | [[src/ai_usage_cost/sources/qwen_code.py]] `src/ai_usage_cost/sources/qwen_code.py:131` |
| `default_roots` | function | `src/ai_usage_cost/sources/roo_code.py` | [[src/ai_usage_cost/sources/roo_code.py]] `src/ai_usage_cost/sources/roo_code.py:17` |
| `default_roots` | function | `src/ai_usage_cost/sources/windsurf.py` | [[src/ai_usage_cost/sources/windsurf.py]] `src/ai_usage_cost/sources/windsurf.py:18` |
| `windsurf_files` | function | `src/ai_usage_cost/sources/windsurf.py` | [[src/ai_usage_cost/sources/windsurf.py]] `src/ai_usage_cost/sources/windsurf.py:31` |
| `parse` | function | `src/ai_usage_cost/sources/windsurf.py` | [[src/ai_usage_cost/sources/windsurf.py]] `src/ai_usage_cost/sources/windsurf.py:45` |
%% generated:chunk-interface end %%
