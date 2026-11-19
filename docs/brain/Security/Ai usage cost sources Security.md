---
title: Ai usage cost sources Security
aliases: []
tags: [security]
area: security
status: active
audience: internal
maturity: approved
confidence: inferred
covers: [src/ai_usage_cost/sources/**]
verified-against: 4d81cedd5403
chunk: ch-localtokenomics-src-ai-usage-cost-sources
approved-by: human
approved-at: '2026-11-19T00:12:14+00:00'
---

# Ai usage cost sources Security

Security-relevant code in the Ai usage cost sources chunk: authentication, tokens, validation and configuration names.

## How it works

17 security-relevant lines were found. Configuration is listed by variable name only, never by value.

Every reader here is read only. SQLite files are opened through a read only URI, and a database error becomes a warning, not a crash. `src/ai_usage_cost/sources/base.py:117-129` JSON Lines readers open files for reading only and replace undecodable bytes instead of failing. `src/ai_usage_cost/sources/base.py:69-84`

Readers avoid prompt and response text where the format allows it. The OpenCode reader pulls fields with `json_extract` and never selects message text. `src/ai_usage_cost/sources/opencode.py:19-22` The Cline reader drops the prompt text the moment it parses a usage string. `src/ai_usage_cost/sources/cline.py:5-8` The Muse Code reader never reads the `auth.json` file. `src/ai_usage_cost/sources/muse_code.py:12`

The environment variables a reader consults only move where it looks for files, for example the Gemini CLI home or the Copilot home. `src/ai_usage_cost/sources/gemini_cli.py:31-35` `src/ai_usage_cost/sources/copilot_cli.py:61-64`

## Reference

%% generated:chunk-security start (do not edit; run brain docs generate) %%
| Concern | Matched | Code |
|---|---|---|
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
%% generated:chunk-security end %%
