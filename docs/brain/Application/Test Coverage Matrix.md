---
title: Test Coverage Matrix
aliases: []
tags: [generated, index, tests]
area: application
status: generated
audience: internal
maturity: approved
confidence: confirmed
covers: []
generated: true
---

# Test Coverage Matrix

Which code each test file exercises through imports.

%% generated:tests-matrix start (do not edit; run brain docs generate) %%
| Test file | Tests | Code under test (imports) | Code |
|---|---|---|---|
| `tests/test_antigravity.py` | 8 | `src/ai_usage_cost/models.py`, `src/ai_usage_cost/sources/antigravity.py` | [[tests/test_antigravity.py]] `tests/test_antigravity.py:19` |
| `tests/test_api.py` | 41 | `src/ai_usage_cost/__init__.py`, `src/ai_usage_cost/aggregate.py`, `src/ai_usage_cost/api.py`, `src/ai_usage_cost/models.py`, `src/ai_usage_cost/pipeline.py`, `src/ai_usage_cost/privacy.py` | [[tests/test_api.py]] `tests/test_api.py:77` |
| `tests/test_claude_code.py` | 23 | `src/ai_usage_cost/models.py`, `src/ai_usage_cost/sources/base.py`, `src/ai_usage_cost/sources/claude_code.py` | [[tests/test_claude_code.py]] `tests/test_claude_code.py:52` |
| `tests/test_cli.py` | 18 | `src/ai_usage_cost/__init__.py`, `src/ai_usage_cost/aggregate.py`, `src/ai_usage_cost/cli.py`, `src/ai_usage_cost/models.py`, `src/ai_usage_cost/pipeline.py` | [[tests/test_cli.py]] `tests/test_cli.py:66` |
| `tests/test_cline.py` | 28 | `src/ai_usage_cost/__init__.py`, `src/ai_usage_cost/models.py`, `src/ai_usage_cost/pipeline.py`, `src/ai_usage_cost/sources/__init__.py`, `src/ai_usage_cost/sources/base.py`, `src/ai_usage_cost/sources/cline.py` | [[tests/test_cline.py]] `tests/test_cline.py:59` |
| `tests/test_codex.py` | 44 | `src/ai_usage_cost/models.py`, `src/ai_usage_cost/pricing.py`, `src/ai_usage_cost/sources/base.py`, `src/ai_usage_cost/sources/codex.py` | [[tests/test_codex.py]] `tests/test_codex.py:85` |
| `tests/test_collect.py` | 13 | `src/ai_usage_cost/__init__.py`, `src/ai_usage_cost/collect.py`, `src/ai_usage_cost/store.py` | [[tests/test_collect.py]] `tests/test_collect.py:61` |
| `tests/test_copilot_chat.py` | 7 | `src/ai_usage_cost/models.py`, `src/ai_usage_cost/sources/copilot_chat.py` | [[tests/test_copilot_chat.py]] `tests/test_copilot_chat.py:28` |
| `tests/test_copilot_cli.py` | 25 | `src/ai_usage_cost/__init__.py`, `src/ai_usage_cost/models.py`, `src/ai_usage_cost/pipeline.py`, `src/ai_usage_cost/pricing.py`, `src/ai_usage_cost/sources/__init__.py`, `src/ai_usage_cost/sources/copilot_cli.py` | [[tests/test_copilot_cli.py]] `tests/test_copilot_cli.py:77` |
| `tests/test_cursor.py` | 10 | `src/ai_usage_cost/models.py`, `src/ai_usage_cost/sources/cursor.py` | [[tests/test_cursor.py]] `tests/test_cursor.py:28` |
| `tests/test_demo.py` | 8 | `src/ai_usage_cost/__init__.py`, `src/ai_usage_cost/cli.py`, `src/ai_usage_cost/demo.py`, `src/ai_usage_cost/pipeline.py`, `src/ai_usage_cost/sources/__init__.py` | [[tests/test_demo.py]] `tests/test_demo.py:27` |
| `tests/test_dyad.py` | 5 | `src/ai_usage_cost/models.py`, `src/ai_usage_cost/sources/dyad.py` | [[tests/test_dyad.py]] `tests/test_dyad.py:28` |
| `tests/test_gemini_cli.py` | 17 | `src/ai_usage_cost/__init__.py`, `src/ai_usage_cost/models.py`, `src/ai_usage_cost/pipeline.py`, `src/ai_usage_cost/sources/__init__.py`, `src/ai_usage_cost/sources/gemini_cli.py`, `src/ai_usage_cost/store.py` | [[tests/test_gemini_cli.py]] `tests/test_gemini_cli.py:57` |
| `tests/test_grok_build.py` | 18 | `src/ai_usage_cost/models.py`, `src/ai_usage_cost/sources/grok_build.py` | [[tests/test_grok_build.py]] `tests/test_grok_build.py:59` |
| `tests/test_insights.py` | 9 | `src/ai_usage_cost/models.py`, `src/ai_usage_cost/pricing.py`, `src/ai_usage_cost/sources/claude_code.py`, `src/ai_usage_cost/trace.py` | [[tests/test_insights.py]] `tests/test_insights.py:57` |
| `tests/test_jan.py` | 7 | `src/ai_usage_cost/models.py`, `src/ai_usage_cost/sources/jan.py` | [[tests/test_jan.py]] `tests/test_jan.py:19` |
| `tests/test_kilo_code.py` | 4 | `src/ai_usage_cost/sources/__init__.py`, `src/ai_usage_cost/sources/kilo_code.py` | [[tests/test_kilo_code.py]] `tests/test_kilo_code.py:28` |
| `tests/test_muse_code.py` | 28 | `src/ai_usage_cost/models.py`, `src/ai_usage_cost/pipeline.py`, `src/ai_usage_cost/sources/__init__.py`, `src/ai_usage_cost/sources/muse_code.py`, `src/ai_usage_cost/store.py` | [[tests/test_muse_code.py]] `tests/test_muse_code.py:92` |
| `tests/test_ollama_app.py` | 3 | `src/ai_usage_cost/models.py`, `src/ai_usage_cost/sources/ollama_app.py` | [[tests/test_ollama_app.py]] `tests/test_ollama_app.py:28` |
| `tests/test_openai_compat.py` | 11 | `src/ai_usage_cost/models.py`, `src/ai_usage_cost/sources/base.py`, `src/ai_usage_cost/sources/openai_compat.py` | [[tests/test_openai_compat.py]] `tests/test_openai_compat.py:22` |
| `tests/test_opencode.py` | 29 | `src/ai_usage_cost/__init__.py`, `src/ai_usage_cost/models.py`, `src/ai_usage_cost/sources/__init__.py`, `src/ai_usage_cost/sources/opencode.py`, `src/ai_usage_cost/store.py` | [[tests/test_opencode.py]] `tests/test_opencode.py:150` |
| `tests/test_pipeline.py` | 39 | `src/ai_usage_cost/__init__.py`, `src/ai_usage_cost/aggregate.py`, `src/ai_usage_cost/models.py`, `src/ai_usage_cost/pipeline.py`, `src/ai_usage_cost/pricing.py`, `src/ai_usage_cost/privacy.py` | [[tests/test_pipeline.py]] `tests/test_pipeline.py:71` |
| `tests/test_pricing.py` | 61 | `src/ai_usage_cost/models.py`, `src/ai_usage_cost/pipeline.py`, `src/ai_usage_cost/pricing.py` | [[tests/test_pricing.py]] `tests/test_pricing.py:41` |
| `tests/test_pricing_v2.py` | 67 | `src/ai_usage_cost/__init__.py`, `src/ai_usage_cost/aggregate.py`, `src/ai_usage_cost/models.py`, `src/ai_usage_cost/pipeline.py`, `src/ai_usage_cost/pricing.py`, `src/ai_usage_cost/sources/base.py` | [[tests/test_pricing_v2.py]] `tests/test_pricing_v2.py:128` |
| `tests/test_privacy.py` | 17 | `src/ai_usage_cost/privacy.py`, `src/ai_usage_cost/trace.py` | [[tests/test_privacy.py]] `tests/test_privacy.py:56` |
| `tests/test_qwen_code.py` | 13 | `src/ai_usage_cost/__init__.py`, `src/ai_usage_cost/models.py`, `src/ai_usage_cost/pipeline.py`, `src/ai_usage_cost/sources/__init__.py`, `src/ai_usage_cost/sources/qwen_code.py`, `src/ai_usage_cost/store.py` | [[tests/test_qwen_code.py]] `tests/test_qwen_code.py:61` |
| `tests/test_rates_data.py` | 31 | `src/ai_usage_cost/models.py`, `src/ai_usage_cost/pricing.py` | [[tests/test_rates_data.py]] `tests/test_rates_data.py:104` |
| `tests/test_rates_diff.py` | 18 | - | [[tests/test_rates_diff.py]] `tests/test_rates_diff.py:94` |
| `tests/test_store.py` | 34 | `src/ai_usage_cost/__init__.py`, `src/ai_usage_cost/models.py`, `src/ai_usage_cost/sources/base.py`, `src/ai_usage_cost/store.py`, `src/ai_usage_cost/trace.py` | [[tests/test_store.py]] `tests/test_store.py:142` |
| `tests/test_store_migration.py` | 4 | `src/ai_usage_cost/__init__.py`, `src/ai_usage_cost/models.py`, `src/ai_usage_cost/store.py` | [[tests/test_store_migration.py]] `tests/test_store_migration.py:25` |
| `tests/test_trace_antigravity.py` | 14 | `src/ai_usage_cost/pricing.py`, `src/ai_usage_cost/sources/antigravity.py`, `src/ai_usage_cost/trace.py` | [[tests/test_trace_antigravity.py]] `tests/test_trace_antigravity.py:26` |
| `tests/test_trace_claude_code.py` | 28 | `src/ai_usage_cost/models.py`, `src/ai_usage_cost/pricing.py`, `src/ai_usage_cost/sources/claude_code.py`, `src/ai_usage_cost/trace.py` | [[tests/test_trace_claude_code.py]] `tests/test_trace_claude_code.py:43` |
| `tests/test_trace_codex.py` | 24 | `src/ai_usage_cost/pricing.py`, `src/ai_usage_cost/privacy.py`, `src/ai_usage_cost/sources/base.py`, `src/ai_usage_cost/sources/codex.py`, `src/ai_usage_cost/trace.py` | [[tests/test_trace_codex.py]] `tests/test_trace_codex.py:56` |
| `tests/test_warning_groups.py` | 21 | `src/ai_usage_cost/aggregate.py` | [[tests/test_warning_groups.py]] `tests/test_warning_groups.py:8` |
| `tests/test_windsurf.py` | 10 | `src/ai_usage_cost/models.py`, `src/ai_usage_cost/sources/windsurf.py` | [[tests/test_windsurf.py]] `tests/test_windsurf.py:28` |
| `web/src/EconomicsTab.test.ts` | 5 | `web/src/EconomicsTab.tsx`, `web/src/api.ts` | [[web/src/EconomicsTab.test.ts]] `web/src/EconomicsTab.test.ts:16` |
| `web/src/Pricing.test.ts` | 22 | `web/src/Pricing.tsx`, `web/src/api.ts` | [[web/src/Pricing.test.ts]] `web/src/Pricing.test.ts:96` |
| `web/src/TraceTab.test.ts` | 32 | `web/src/TraceTab.tsx`, `web/src/api.ts` | [[web/src/TraceTab.test.ts]] `web/src/TraceTab.test.ts:64` |
| `web/src/components/metric-info.test.tsx` | 4 | `web/src/components/metric-info.tsx` | [[web/src/components/metric-info.test.tsx]] `web/src/components/metric-info.test.tsx:6` |
| `web/src/components/rank.test.ts` | 9 | `web/src/components/rank.ts` | [[web/src/components/rank.test.ts]] `web/src/components/rank.test.ts:4` |
| `web/src/components/sparkline.test.ts` | 5 | `web/src/components/sparkline.tsx` | [[web/src/components/sparkline.test.ts]] `web/src/components/sparkline.test.ts:4` |
| `web/src/format.test.ts` | 49 | `web/src/api.ts`, `web/src/format.ts` | [[web/src/format.test.ts]] `web/src/format.test.ts:20` |
| `web/src/pricing-format.test.ts` | 14 | `web/src/pricing-format.ts` | [[web/src/pricing-format.test.ts]] `web/src/pricing-format.test.ts:12` |
| `web/src/pricing-notes.test.ts` | 13 | `web/src/pricing-notes.ts` | [[web/src/pricing-notes.test.ts]] `web/src/pricing-notes.test.ts:11` |
| `web/src/turn-insights.test.ts` | 35 | `web/src/api.ts`, `web/src/turn-insights.ts` | [[web/src/turn-insights.test.ts]] `web/src/turn-insights.test.ts:56` |

Owned code files with no importing test: 70.

- `scripts/demo_logs.py`
- `scripts/rates_diff.py`
- `src/ai_usage_cost/render/__init__.py`
- `src/ai_usage_cost/render/png.py`
- `src/ai_usage_cost/render/terminal.py`
- `src/ai_usage_cost/tui.py`
- `web/eslint.config.js`
- `web/src/App.tsx`
- `web/src/ContextTab.tsx`
- `web/src/FilterRail.tsx`
- `web/src/Header.tsx`
- `web/src/Overview.tsx`
- `web/src/SessionWorkspace.tsx`
- `web/src/Sessions.tsx`
- `web/src/Sources.tsx`
- `web/src/components/chart-hover.tsx`
- `web/src/components/chart-time.tsx`
- `web/src/components/columns.tsx`
- `web/src/components/detail.tsx`
- `web/src/components/filters.tsx`
- `web/src/components/panel.tsx`
- `web/src/components/series.ts`
- `web/src/components/session.tsx`
- `web/src/components/source-card.tsx`
- `web/src/components/stat.tsx`
- `web/src/components/states.tsx`
- `web/src/components/status.tsx`
- `web/src/components/trace.tsx`
- `web/src/components/ui/accordion.tsx`
- `web/src/components/ui/alert.tsx`
- `web/src/components/ui/badge.tsx`
- `web/src/components/ui/button.tsx`
- `web/src/components/ui/chart.tsx`
- `web/src/components/ui/checkbox.tsx`
- `web/src/components/ui/collapsible.tsx`
- `web/src/components/ui/dialog.tsx`
- `web/src/components/ui/dropdown-menu.tsx`
- `web/src/components/ui/input.tsx`
- `web/src/components/ui/label.tsx`
- `web/src/components/ui/popover.tsx`
- `web/src/components/ui/progress.tsx`
- `web/src/components/ui/select.tsx`
- `web/src/components/ui/separator.tsx`
- `web/src/components/ui/sheet.tsx`
- `web/src/components/ui/skeleton.tsx`
- `web/src/components/ui/sonner.tsx`
- `web/src/components/ui/switch.tsx`
- `web/src/components/ui/table.tsx`
- `web/src/components/ui/tabs.tsx`
- `web/src/components/ui/textarea.tsx`
- `web/src/components/ui/toggle-group.tsx`
- `web/src/components/ui/toggle.tsx`
- `web/src/components/ui/tooltip.tsx`
- `web/src/components/use-media-query.ts`
- `web/src/components/workspace-panel.ts`
- `web/src/design-system/cn.ts`
- `web/src/main.tsx`
- `web/src/prototype/Gallery.tsx`
- `web/src/prototype/OverviewScreen.tsx`
- `web/src/prototype/PricingScreen.tsx`
- ...
%% generated:tests-matrix end %%
