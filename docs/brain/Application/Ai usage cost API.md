---
title: Ai usage cost API
aliases: []
tags: [api]
area: application
status: draft
audience: internal
maturity: draft
confidence: inferred
covers: [src/ai_usage_cost/*]
verified-against: e5313fbd7062
chunk: ch-localtokenomics-src-ai-usage-cost
---

# Ai usage cost API

The routes and interfaces exposed by the Ai usage cost chunk.

## How it works

12 routes were found. Each row names the HTTP method, the path, the handler and where the route is declared.

### How the interface is built

`create_app` builds one FastAPI application per analysis. It keeps the current `Analysis` in a small state dictionary, and the post route `/api/refresh` is the only place that replaces it (`src/ai_usage_cost/api.py:198-216`, `src/ai_usage_cost/api.py:388-392`). The application title is `ai-usage-cost` and the interactive docs sit at `/api/docs` (`src/ai_usage_cost/api.py:214`).

The summary routes read the in memory analysis. The report route `/api/report` passes its query parameters straight to `report_of`, so the HTTP filters are the same filters the command line uses (`src/ai_usage_cost/api.py:289-318`). The meta route `/api/meta` lists the clients, providers, models and projects found, the first and last day, the rate table age and the warning counts (`src/ai_usage_cost/api.py:255-287`). The rates route `/api/rates` returns the loaded rate table (`src/ai_usage_cost/api.py:384-386`).

The session routes read the store. A request for a trace, the economics, the context or the outcome of a session opens the store, checks that the session exists and answers 404 when it does not (`src/ai_usage_cost/api.py:230-242`). Reconstructed spans are cached per source and session for the life of one analysis, and a refresh or a delete clears the entry (`src/ai_usage_cost/api.py:207-213`, `src/ai_usage_cost/api.py:367`, `src/ai_usage_cost/api.py:391`). A server started without a store answers 503 on those routes (`src/ai_usage_cost/api.py:219-223`).

The only write routes are the put route `/api/sessions/{source}/{session_id}/outcome`, which stores the human rating, and the delete route `/api/sessions/{source}/{session_id}`, which removes the session's spans and records an exclusion (`src/ai_usage_cost/api.py:355-368`, `src/ai_usage_cost/store.py:595-606`). Neither writes to the AI tools' own logs.

The content route `/api/sessions/{source}/{session_id}/spans/{span_id}/content` returns the text of one span only when the configuration allows it, redacts secrets and answers 404 otherwise (`src/ai_usage_cost/api.py:370-382`, `src/ai_usage_cost/privacy.py:86-101`). See [[Ai usage cost Security]].

When the built dashboard bundle exists the application serves it at `/`. When it does not, `/` returns a message telling the maintainer to build the web bundle (`src/ai_usage_cost/api.py:394-402`).

The routes carry no authentication. The command line binds the server to `127.0.0.1` by default (`src/ai_usage_cost/cli.py:109-111`), which is the only access control in the code.

## Reference

%% generated:chunk-routes start (do not edit; run brain docs generate) %%
| Method | Path | Handler | Framework | Auth | Code |
|---|---|---|---|---|---|
| `GET` | `/` | `missing_build` | fastapi | none detected | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:399` |
| `GET` | `/api/meta` | `meta` | fastapi | none detected | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:256` |
| `GET` | `/api/rates` | `rates` | fastapi | none detected | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:385` |
| `POST` | `/api/refresh` | `refresh` | fastapi | none detected | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:389` |
| `GET` | `/api/report` | `report` | fastapi | none detected | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:290` |
| `DELETE` | `/api/sessions/{source}/{session_id}` | `forget_session` | fastapi | none detected | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:362` |
| `GET` | `/api/sessions/{source}/{session_id}/context` | `context` | fastapi | none detected | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:346` |
| `GET` | `/api/sessions/{source}/{session_id}/economics` | `economics` | fastapi | none detected | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:334` |
| `GET` | `/api/sessions/{source}/{session_id}/outcome` | `outcome` | fastapi | none detected | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:351` |
| `PUT` | `/api/sessions/{source}/{session_id}/outcome` | `rate_session` | fastapi | none detected | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:356` |
| `GET` | `/api/sessions/{source}/{session_id}/spans/{span_id}/content` | `span_content` | fastapi | none detected | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:374` |
| `GET` | `/api/sessions/{source}/{session_id}/trace` | `trace` | fastapi | none detected | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:321` |
%% generated:chunk-routes end %%
