---
title: Interface Catalog
aliases: []
tags: [api, catalog, generated]
area: catalogs
status: generated
audience: internal
maturity: approved
confidence: confirmed
covers: []
generated: true
---

# Interface Catalog

Every interface the code exposes, grouped by owning component.

%% generated:interface-catalog start (do not edit; run brain docs generate) %%
| Method | Path | Component | Framework | Auth | Code |
|---|---|---|---|---|---|
| `GET` | `/` | src/ai_usage_cost | fastapi | - | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:399` |
| `GET` | `/api/meta` | src/ai_usage_cost | fastapi | - | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:256` |
| `GET` | `/api/rates` | src/ai_usage_cost | fastapi | - | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:385` |
| `POST` | `/api/refresh` | src/ai_usage_cost | fastapi | - | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:389` |
| `GET` | `/api/report` | src/ai_usage_cost | fastapi | - | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:290` |
| `DELETE` | `/api/sessions/{source}/{session_id}` | src/ai_usage_cost | fastapi | - | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:362` |
| `GET` | `/api/sessions/{source}/{session_id}/context` | src/ai_usage_cost | fastapi | - | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:346` |
| `GET` | `/api/sessions/{source}/{session_id}/economics` | src/ai_usage_cost | fastapi | - | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:334` |
| `GET` | `/api/sessions/{source}/{session_id}/outcome` | src/ai_usage_cost | fastapi | - | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:351` |
| `PUT` | `/api/sessions/{source}/{session_id}/outcome` | src/ai_usage_cost | fastapi | - | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:356` |
| `GET` | `/api/sessions/{source}/{session_id}/spans/{span_id}/content` | src/ai_usage_cost | fastapi | - | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:374` |
| `GET` | `/api/sessions/{source}/{session_id}/trace` | src/ai_usage_cost | fastapi | - | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:321` |
%% generated:interface-catalog end %%
