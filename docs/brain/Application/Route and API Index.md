---
title: Route and API Index
aliases: []
tags: [api, generated, index]
area: application
status: generated
audience: internal
maturity: approved
confidence: confirmed
covers: []
generated: true
---

# Route and API Index

Every route the extractors found, with its handler.

%% generated:routes start (do not edit; run brain docs generate) %%
| Method | Path | Handler | Framework | Auth | Component | Code |
|---|---|---|---|---|---|---|
| `GET` | `/` | `missing_build` | fastapi | - | src/ai_usage_cost | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:399` |
| `GET` | `/api/meta` | `meta` | fastapi | - | src/ai_usage_cost | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:256` |
| `GET` | `/api/rates` | `rates` | fastapi | - | src/ai_usage_cost | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:385` |
| `POST` | `/api/refresh` | `refresh` | fastapi | - | src/ai_usage_cost | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:389` |
| `GET` | `/api/report` | `report` | fastapi | - | src/ai_usage_cost | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:290` |
| `DELETE` | `/api/sessions/{source}/{session_id}` | `forget_session` | fastapi | - | src/ai_usage_cost | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:362` |
| `GET` | `/api/sessions/{source}/{session_id}/context` | `context` | fastapi | - | src/ai_usage_cost | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:346` |
| `GET` | `/api/sessions/{source}/{session_id}/economics` | `economics` | fastapi | - | src/ai_usage_cost | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:334` |
| `GET` | `/api/sessions/{source}/{session_id}/outcome` | `outcome` | fastapi | - | src/ai_usage_cost | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:351` |
| `PUT` | `/api/sessions/{source}/{session_id}/outcome` | `rate_session` | fastapi | - | src/ai_usage_cost | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:356` |
| `GET` | `/api/sessions/{source}/{session_id}/spans/{span_id}/content` | `span_content` | fastapi | - | src/ai_usage_cost | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:374` |
| `GET` | `/api/sessions/{source}/{session_id}/trace` | `trace` | fastapi | - | src/ai_usage_cost | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:321` |
%% generated:routes end %%
