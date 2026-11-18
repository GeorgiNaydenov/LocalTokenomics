---
title: Ai usage cost Workflows
aliases: []
tags: [workflow]
area: application
status: draft
audience: internal
maturity: draft
confidence: inferred
covers: [src/ai_usage_cost/*]
verified-against: e5313fbd7062
chunk: ch-localtokenomics-src-ai-usage-cost
---

# Ai usage cost Workflows

How requests enter the Ai usage cost chunk and which files they reach.

## How it works

Entry files are the files that declare routes. The table lists the files each entry file imports inside this chunk; runtime order is described in the sequence diagrams authored for this chunk.

### The command line is the second entry point

The route scanner only sees the API module, but most runs start in the command line. Every command that shows costs calls `analyze` and then `report_of` (`src/ai_usage_cost/cli.py:87-94`, `src/ai_usage_cost/cli.py:184-185`, `src/ai_usage_cost/cli.py:331-332`, `src/ai_usage_cost/cli.py:369-370`).

| Command | What it does | Code |
|---|---|---|
| `scan` | Prints a terminal report, or JSON with `--json`, and exits with code 1 when no usage is found | `src/ai_usage_cost/cli.py:71-105` |
| `serve` | Scans, then starts the HTTP interface and optionally opens the browser | `src/ai_usage_cost/cli.py:108-137` |
| `demo` | Generates synthetic logs, then serves them; `--off` deletes them and serves the real logs | `src/ai_usage_cost/cli.py:140-172` |
| `export` | Writes the report as `.json` or `.png` and refuses other extensions with exit code 2 | `src/ai_usage_cost/cli.py:175-196` |
| `collect` | Samples GPU use into the store until the duration ends or the user interrupts | `src/ai_usage_cost/cli.py:199-225` |
| `sql` | Opens the store in Datasette, which needs the `sql` extra | `src/ai_usage_cost/cli.py:228-248` |
| `alert` | Sends a notification through Apprise when spend crosses a threshold | `src/ai_usage_cost/cli.py:298-354` |
| `tui` | Shows the sessions in a terminal table | `src/ai_usage_cost/cli.py:357-376` |

The optional features sql, alert and tui import their library only when the command runs. If the library is missing the command prints an install hint and exits with code 2 (`src/ai_usage_cost/cli.py:48-56`).

### The main flow

A scan runs in this order. It loads the privacy configuration, opens or migrates the store, ingests changed log files, loads the stored requests, prices each one and attaches warnings (`src/ai_usage_cost/pipeline.py:174-245`). The report is then built by filtering the priced events and grouping them (`src/ai_usage_cost/pipeline.py:305-349`, `src/ai_usage_cost/aggregate.py:675-723`). The order is drawn in [[Scan pipeline from logs to report]], the data movement in [[Usage data flow]], the same process as a business view in [[Scan and report process]] and the pricing decisions in [[How one request is priced]].

### Why ingest is incremental

A file whose modification time, size and parser version are unchanged is skipped (`src/ai_usage_cost/store.py:229-231`). A file that only grew, and whose earlier bytes still hash the same, can be read from where the last scan stopped if its source declares a resume hook (`src/ai_usage_cost/store.py:243-253`). Everything else is parsed again in full and its old rows are replaced (`src/ai_usage_cost/store.py:254-255`, `src/ai_usage_cost/store.py:267-269`).

### Alerts

The alert command compares the window's own total with a threshold, or its rise over the window before. It refuses `--over` and `--rise-over` together, and it needs one of them (`src/ai_usage_cost/cli.py:322-326`). The message says what was left out of the cost, namely unpriced models and sessions without token counts, and calls that "unknown, not zero" (`src/ai_usage_cost/cli.py:285-295`).

## Reference

%% generated:chunk-entry-points start (do not edit; run brain docs generate) %%
| Entry file | Uses (imports in chunk) | Code |
|---|---|---|
| `src/ai_usage_cost/api.py` | `src/ai_usage_cost/__init__.py`, `src/ai_usage_cost/aggregate.py`, `src/ai_usage_cost/models.py`, `src/ai_usage_cost/pipeline.py`, `src/ai_usage_cost/pricing.py`, `src/ai_usage_cost/privacy.py`, `src/ai_usage_cost/sources/__init__.py`, `src/ai_usage_cost/store.py`, `src/ai_usage_cost/trace.py` | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:1-404` |
%% generated:chunk-entry-points end %%
