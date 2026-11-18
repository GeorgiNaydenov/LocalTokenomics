---
title: Invariants Catalogue
aliases: []
tags: [api, catalog, generated, reference]
area: application
status: generated
audience: internal
maturity: approved
confidence: confirmed
covers: []
generated: true
---

# Invariants Catalogue

Rules the code enforces, each with where it is enforced and which test mentions it.

%% generated:invariants start (do not edit; run brain docs generate) %%
| Invariant | Outcome | Source | Guarded by |
|---|---|---|---|
| `load_rates` refuses when not isinstance(data, dict) or not isinstance(data.get('models'), list) | raises CatalogError | [[scripts/rates_diff.py]] `scripts/rates_diff.py:260` | none |
| `load_catalog` refuses when not isinstance(data, dict) | raises CatalogError | [[scripts/rates_diff.py]] `scripts/rates_diff.py:279` | `tests/test_rates_diff.py:90` |
| `create_app` refuses when path is None | raises HTTPException (503) | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:222` | `tests/test_api.py:13` |
| `opened` refuses when path is None | raises HTTPException (503) | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:222` | `tests/test_trace_antigravity.py:130` |
| `create_app` refuses when not store.session_exists(conn, source, session_id) | raises HTTPException (404) | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:235` | `tests/test_api.py:13` |
| `session_spans` refuses when not store.session_exists(conn, source, session_id) | raises HTTPException (404) | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:235` | none |
| `create_app` refuses when not store.session_exists(conn, source, session_id) | raises HTTPException (404) | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:364` | `tests/test_api.py:13` |
| `forget_session` refuses when not store.session_exists(conn, source, session_id) | raises HTTPException (404) | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:364` | none |
| `create_app` refuses when span is None | raises HTTPException (404) | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:377` | `tests/test_api.py:13` |
| `span_content` refuses when span is None | raises HTTPException (404) | [[src/ai_usage_cost/api.py]] `src/ai_usage_cost/api.py:377` | `tests/test_api.py:568` |
| `_roots` refuses when not path | raises typer.BadParameter | [[src/ai_usage_cost/cli.py]] `src/ai_usage_cost/cli.py:65` | `tests/conftest.py:28` |
| `alert` refuses when days < 1 | raises typer.BadParameter | [[src/ai_usage_cost/cli.py]] `src/ai_usage_cost/cli.py:320` | `tests/test_cli.py:67` |
| `alert` refuses when over is not None and rise_over is not None | raises typer.BadParameter | [[src/ai_usage_cost/cli.py]] `src/ai_usage_cost/cli.py:322` | `tests/test_cli.py:67` |
| `alert` refuses when threshold is None | raises typer.BadParameter | [[src/ai_usage_cost/cli.py]] `src/ai_usage_cost/cli.py:325` | `tests/test_cli.py:67` |
| `_valid_window` validates the model | validates before accepting the value | [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:54` | none |
| `_valid_window` refuses when any((not 0 <= day <= 6 for day in self.weekdays)) | raises ValueError | [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:55` | none |
| `_valid_window` refuses when any((not 0 <= start < end <= 24 for start, end in self.utc_hours)) | raises ValueError | [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:58` | none |
| `_ordered` validates the model | validates before accepting the value | [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:90` | none |
| `_ordered` refuses when self.from_ is not None and self.until is not None and (self.from_ >= self.until) | raises ValueError | [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:91` | none |
| `_sorted_bands` validates bands | validates before accepting the value | [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:149` | none |
| `_disjoint_periods` validates the model | validates before accepting the value | [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:153` | none |
| `_disjoint_periods` refuses when earlier.until is None or (later.from_ or date.min) < earlier.until | raises ValueError | [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:158` | none |
| `_consistent` validates the model | validates before accepting the value | [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:272` | none |
| `_consistent` refuses when duplicates | raises ValueError | [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:275` | none |
| `_consistent` refuses when missing | raises ValueError | [[src/ai_usage_cost/pricing.py]] `src/ai_usage_cost/pricing.py:281` | none |
| `read_content` refuses when config.metadata_only or span.content_path is None | raises ContentUnavailable | [[src/ai_usage_cost/privacy.py]] `src/ai_usage_cost/privacy.py:87` | `tests/test_privacy.py:13` |
| `resolve_path` refuses when index >= len(current) | raises ContentUnavailable | [[src/ai_usage_cost/privacy.py]] `src/ai_usage_cost/privacy.py:109` | none |
| `_values_match_provenance` validates the model | validates before accepting the value | [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:89` | none |
| `_values_match_provenance` refuses when (value is None) != (provenance == 'unavailable') | raises ValueError | [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:96` | none |
| `getJson` refuses when !response.ok | throws ApiError | [[web/src/api.ts]] `web/src/api.ts:496` | none |
| `useChart` refuses when !context | throws Error | [[web/src/components/ui/chart.tsx]] `web/src/components/ui/chart.tsx:32` | none |

31 refusals, requirements and constraints were read from the code; 19 have no test that mentions their enclosing symbol.
%% generated:invariants end %%
