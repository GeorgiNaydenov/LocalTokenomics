---
title: Ai usage cost Security
aliases: []
tags: [security]
area: security
status: draft
audience: internal
maturity: draft
confidence: inferred
covers: [src/ai_usage_cost/*]
verified-against: e5313fbd7062
chunk: ch-localtokenomics-src-ai-usage-cost
---

# Ai usage cost Security

Security-relevant code in the Ai usage cost chunk: authentication, tokens, validation and configuration names.

## How it works

64 security-relevant lines were found. Configuration is listed by variable name only, never by value.

### What protects the user

The package works on the owner's own logs, so the risks are leaking prompt text or credentials, not attacks from outside. The code answers them in four ways.

1. Metadata only by default. The privacy configuration starts with `metadata_only` true, and reading a span's text raises `ContentUnavailable` while it is on (`src/ai_usage_cost/privacy.py:52-57`, `src/ai_usage_cost/privacy.py:86-88`). The interface turns that into a 404 (`src/ai_usage_cost/api.py:379-382`).
2. Redaction. Text that is released is cut to at most 65,536 bytes by default and then passed through nine patterns that replace private keys, cloud keys, GitHub tokens, vendor API keys, JWTs, bearer tokens and generic key or password assignments with a redaction marker that names the kind. The count of redactions is returned with the text (`src/ai_usage_cost/privacy.py:11`, `src/ai_usage_cost/privacy.py:14-45`, `src/ai_usage_cost/privacy.py:78-101`).
3. Exclusion. A project listed in `exclude_projects` has its spans dropped at ingest, and a session the user forgets is remembered in `session_exclusions` so the next scan does not bring its spans back (`src/ai_usage_cost/store.py:213-216`, `src/ai_usage_cost/store.py:273-277`, `src/ai_usage_cost/store.py:595-606`). Both controls act on spans only, see below.
4. Local only. The server host defaults to `127.0.0.1` (`src/ai_usage_cost/cli.py:109-111`), and source databases are opened read only (`src/ai_usage_cost/sources/base.py:123-124`).

### Things a reader should not assume

- A missing or invalid configuration file silently gives the defaults, so a typo in `config.json` turns every privacy setting back on rather than off (`src/ai_usage_cost/privacy.py:60-68`).
- `content_retention_days` is accepted but inert. The pipeline says so in a warning (`src/ai_usage_cost/pipeline.py:240-244`). Only `metadata_retention_days` deletes anything, and it deletes trace rows older than the window (`src/ai_usage_cost/store.py:300-303`).
- Forgetting a session deletes its spans and rating but not its requests, so its cost stays in every total and its stored raw records remain (`src/ai_usage_cost/store.py:595-606`). Requests are inserted without the exclusion or project test, which only guards spans (`src/ai_usage_cost/store.py:270-277`).
- Released text is cut to the byte limit before it is redacted, so a secret split at the limit may be too short for its pattern to match (`src/ai_usage_cost/privacy.py:97-98`).
- The HTTP routes have no authentication and the content route does not check a caller (`src/ai_usage_cost/api.py:370-382`).
- Two outbound network paths exist in the core files. The GPU sampler asks a local Ollama endpoint which models are loaded, and `alert` sends a notification to the targets the user passes (`src/ai_usage_cost/collect.py:27`, `src/ai_usage_cost/collect.py:197-208`, `src/ai_usage_cost/cli.py:344-354`).
- Configuration names read by the source parsers, such as `APPDATA` and `XDG_DATA_HOME`, only locate log folders. They are listed in the table below by name.

## Reference

%% generated:chunk-security start (do not edit; run brain docs generate) %%
| Concern | Matched | Code |
|---|---|---|
| input validation | `pydantic` | [[src/ai_usage_cost/aggregate.py]] `src/ai_usage_cost/aggregate.py:9` |
| input validation | `BaseModel` | [[src/ai_usage_cost/aggregate.py]] `src/ai_usage_cost/aggregate.py:26` |
| input validation | `BaseModel` | [[src/ai_usage_cost/aggregate.py]] `src/ai_usage_cost/aggregate.py:37` |
| input validation | `BaseModel` | [[src/ai_usage_cost/aggregate.py]] `src/ai_usage_cost/aggregate.py:48` |
| input validation | `BaseModel` | [[src/ai_usage_cost/aggregate.py]] `src/ai_usage_cost/aggregate.py:77` |
| input validation | `BaseModel` | [[src/ai_usage_cost/aggregate.py]] `src/ai_usage_cost/aggregate.py:100` |
| input validation | `BaseModel` | [[src/ai_usage_cost/aggregate.py]] `src/ai_usage_cost/aggregate.py:115` |
| input validation | `BaseModel` | [[src/ai_usage_cost/aggregate.py]] `src/ai_usage_cost/aggregate.py:454` |
| input validation | `BaseModel` | [[src/ai_usage_cost/aggregate.py]] `src/ai_usage_cost/aggregate.py:462` |
| input validation | `pydantic` | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:13` |
| input validation | `BaseModel` | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:86` |
| input validation | `BaseModel` | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:91` |
| input validation | `BaseModel` | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:105` |
| input validation | `pydantic` | [[src/ai_usage_cost/collect.py]] `src/ai_usage_cost/collect.py:14` |
| input validation | `BaseModel` | [[src/ai_usage_cost/collect.py]] `src/ai_usage_cost/collect.py:49` |
| input validation | `pydantic` | [[src/ai_usage_cost/models.py]] `src/ai_usage_cost/models.py:6` |
| input validation | `BaseModel` | [[src/ai_usage_cost/models.py]] `src/ai_usage_cost/models.py:12` |
| input validation | `BaseModel` | [[src/ai_usage_cost/models.py]] `src/ai_usage_cost/models.py:49` |
| input validation | `BaseModel` | [[src/ai_usage_cost/models.py]] `src/ai_usage_cost/models.py:75` |
| input validation | `BaseModel` | [[src/ai_usage_cost/models.py]] `src/ai_usage_cost/models.py:117` |
| input validation | `BaseModel` | [[src/ai_usage_cost/models.py]] `src/ai_usage_cost/models.py:123` |
| input validation | `pydantic` | [[src/ai_usage_cost/pipeline.py]] `src/ai_usage_cost/pipeline.py:9` |
| input validation | `BaseModel` | [[src/ai_usage_cost/pipeline.py]] `src/ai_usage_cost/pipeline.py:31` |
| input validation | `pydantic` | [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:9` |
| input validation | `BaseModel` | [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:11` |
| input validation | `BaseModel` | [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:29` |
| input validation | `BaseModel` | [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:68` |
| input validation | `BaseModel` | [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:101` |
| input validation | `BaseModel` | [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:109` |
| input validation | `BaseModel` | [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:169` |
| input validation | `BaseModel` | [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:224` |
| input validation | `BaseModel` | [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:232` |
| input validation | `BaseModel` | [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:252` |
| input validation | `pydantic` | [[src/ai_usage_cost/privacy.py]] `src/ai_usage_cost/privacy.py:7` |
| credentials and tokens | `jwt` | [[src/ai_usage_cost/privacy.py]] `src/ai_usage_cost/privacy.py:36` |
| input validation | `BaseModel` | [[src/ai_usage_cost/privacy.py]] `src/ai_usage_cost/privacy.py:52` |
| configuration read by name | `APPDATA` | [[src/ai_usage_cost/sources/cline.py]] `src/ai_usage_cost/sources/cline.py:97` |
| configuration read by name | `CLINE_SESSION_DATA_DIR` | [[src/ai_usage_cost/sources/cline.py]] `src/ai_usage_cost/sources/cline.py:124` |
| configuration read by name | `CLINE_DATA_DIR` | [[src/ai_usage_cost/sources/cline.py]] `src/ai_usage_cost/sources/cline.py:127` |
| configuration read by name | `CLINE_DIR` | [[src/ai_usage_cost/sources/cline.py]] `src/ai_usage_cost/sources/cline.py:130` |
| configuration read by name | `APPDATA` | [[src/ai_usage_cost/sources/copilot_chat.py]] `src/ai_usage_cost/sources/copilot_chat.py:18` |
| configuration read by name | `COPILOT_HOME` | [[src/ai_usage_cost/sources/copilot_cli.py]] `src/ai_usage_cost/sources/copilot_cli.py:62` |
| configuration read by name | `APPDATA` | [[src/ai_usage_cost/sources/cursor.py]] `src/ai_usage_cost/sources/cursor.py:19` |
| configuration read by name | `APPDATA` | [[src/ai_usage_cost/sources/dyad.py]] `src/ai_usage_cost/sources/dyad.py:16` |
| configuration read by name | `GEMINI_CLI_HOME` | [[src/ai_usage_cost/sources/gemini_cli.py]] `src/ai_usage_cost/sources/gemini_cli.py:32` |
| configuration read by name | `GROK_HOME` | [[src/ai_usage_cost/sources/grok_build.py]] `src/ai_usage_cost/sources/grok_build.py:15` |
| configuration read by name | `APPDATA` | [[src/ai_usage_cost/sources/jan.py]] `src/ai_usage_cost/sources/jan.py:19` |
| configuration read by name | `MUSE_DATA_DIR` | [[src/ai_usage_cost/sources/muse_code.py]] `src/ai_usage_cost/sources/muse_code.py:60` |
| configuration read by name | `XDG_DATA_HOME` | [[src/ai_usage_cost/sources/muse_code.py]] `src/ai_usage_cost/sources/muse_code.py:63` |
| configuration read by name | `LOCALAPPDATA` | [[src/ai_usage_cost/sources/ollama_app.py]] `src/ai_usage_cost/sources/ollama_app.py:16` |
| configuration read by name | `XDG_DATA_HOME` | [[src/ai_usage_cost/sources/opencode.py]] `src/ai_usage_cost/sources/opencode.py:65` |
| configuration read by name | `APPDATA` | [[src/ai_usage_cost/sources/opencode.py]] `src/ai_usage_cost/sources/opencode.py:76` |
| configuration read by name | `APPDATA` | [[src/ai_usage_cost/sources/windsurf.py]] `src/ai_usage_cost/sources/windsurf.py:20` |
| input validation | `pydantic` | [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:7` |
| input validation | `BaseModel` | [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:55` |
| input validation | `BaseModel` | [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:104` |
| input validation | `BaseModel` | [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:112` |
| input validation | `BaseModel` | [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:134` |
| input validation | `BaseModel` | [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:141` |
| input validation | `BaseModel` | [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:154` |
| input validation | `BaseModel` | [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:177` |
| input validation | `BaseModel` | [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:184` |
| input validation | `BaseModel` | [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:192` |
| input validation | `BaseModel` | [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:201` |
%% generated:chunk-security end %%
