---
title: Environment Variables
aliases: []
tags: [generated, operations, reference]
area: operations
status: generated
audience: internal
maturity: approved
confidence: confirmed
covers: []
generated: true
---

# Environment Variables

Every environment variable the code reads, with where it is read and where it is declared.

%% generated:env-vars start (do not edit; run brain docs generate) %%
| Variable | Needed | Read at | Declared in an example file | Set in CI or compose |
|---|---|---|---|---|
| `APPDATA` | optional (a fallback exists) | [[src/ai_usage_cost/sources/cline.py]] `src/ai_usage_cost/sources/cline.py:97`, [[src/ai_usage_cost/sources/copilot_chat.py]] `src/ai_usage_cost/sources/copilot_chat.py:18`, [[src/ai_usage_cost/sources/cursor.py]] `src/ai_usage_cost/sources/cursor.py:19` and 4 more | - | - |
| `CLINE_DATA_DIR` | optional (a fallback exists) | [[src/ai_usage_cost/sources/cline.py]] `src/ai_usage_cost/sources/cline.py:127` | - | - |
| `CLINE_DIR` | optional (a fallback exists) | [[src/ai_usage_cost/sources/cline.py]] `src/ai_usage_cost/sources/cline.py:130` | - | - |
| `CLINE_SESSION_DATA_DIR` | optional (a fallback exists) | [[src/ai_usage_cost/sources/cline.py]] `src/ai_usage_cost/sources/cline.py:124` | - | - |
| `COPILOT_HOME` | optional (a fallback exists) | [[src/ai_usage_cost/sources/copilot_cli.py]] `src/ai_usage_cost/sources/copilot_cli.py:62` | - | - |
| `GEMINI_CLI_HOME` | optional (a fallback exists) | [[src/ai_usage_cost/sources/gemini_cli.py]] `src/ai_usage_cost/sources/gemini_cli.py:32` | - | - |
| `GROK_HOME` | optional (a fallback exists) | [[src/ai_usage_cost/sources/grok_build.py]] `src/ai_usage_cost/sources/grok_build.py:15` | - | - |
| `LOCALAPPDATA` | required | [[src/ai_usage_cost/sources/ollama_app.py]] `src/ai_usage_cost/sources/ollama_app.py:16` | - | - |
| `MUSE_DATA_DIR` | optional (a fallback exists) | [[src/ai_usage_cost/sources/muse_code.py]] `src/ai_usage_cost/sources/muse_code.py:60` | - | - |
| `XDG_DATA_HOME` | optional (a fallback exists) | [[src/ai_usage_cost/sources/muse_code.py]] `src/ai_usage_cost/sources/muse_code.py:63`, [[src/ai_usage_cost/sources/opencode.py]] `src/ai_usage_cost/sources/opencode.py:65` | - | - |

Names and locations only. Values never appear in this note, in logs or in commits.
%% generated:env-vars end %%
