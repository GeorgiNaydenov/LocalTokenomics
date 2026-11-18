---
title: Coverage Map
aliases: []
tags: [catalog, generated, operations, reference]
area: operations
status: generated
audience: internal
maturity: approved
confidence: confirmed
covers: []
generated: true
---

# Coverage Map

Which note owns each source file and which tests reach it. A row with none is a gap, not an error.

%% generated:coverage-map start (do not edit; run brain docs generate) %%
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
115 source files; 10 have an owning note; 45 are imported by a test; 70 have no test that imports them.
=======
115 source files; 75 have an owning note; 45 are imported by a test; 70 have no test that imports them.
>>>>>>> docs/chunk-ch-localtokenomics-root
=======
115 source files; 73 have an owning note; 45 are imported by a test; 70 have no test that imports them.
>>>>>>> docs/chunk-ch-localtokenomics-web-src
=======
115 source files; 25 have an owning note; 45 are imported by a test; 70 have no test that imports them.
>>>>>>> docs/chunk-ch-localtokenomics-web-src-components-ui

| Source file | Owning notes | Tests that import it |
|---|---|---|
| `scripts/demo_logs.py` | none | none |
| `scripts/rates_diff.py` | none | none |
| `src/ai_usage_cost/__init__.py` | none | `tests/test_api.py`, `tests/test_cli.py`, `tests/test_cline.py` and 10 more |
| `src/ai_usage_cost/aggregate.py` | none | `tests/test_api.py`, `tests/test_cli.py`, `tests/test_pipeline.py` and 2 more |
| `src/ai_usage_cost/api.py` | none | `tests/test_api.py` |
| `src/ai_usage_cost/cli.py` | none | `tests/test_cli.py`, `tests/test_demo.py` |
| `src/ai_usage_cost/collect.py` | none | `tests/test_collect.py` |
| `src/ai_usage_cost/demo.py` | none | `tests/test_demo.py` |
| `src/ai_usage_cost/models.py` | none | `tests/test_antigravity.py`, `tests/test_api.py`, `tests/test_claude_code.py` and 24 more |
| `src/ai_usage_cost/pipeline.py` | none | `tests/test_api.py`, `tests/test_cli.py`, `tests/test_cline.py` and 8 more |
| `src/ai_usage_cost/pricing.py` | none | `tests/test_codex.py`, `tests/test_copilot_cli.py`, `tests/test_insights.py` and 7 more |
| `src/ai_usage_cost/privacy.py` | none | `tests/test_api.py`, `tests/test_pipeline.py`, `tests/test_privacy.py` and 1 more |
| `src/ai_usage_cost/render/__init__.py` | none | none |
| `src/ai_usage_cost/render/png.py` | none | none |
| `src/ai_usage_cost/render/terminal.py` | none | none |
| `src/ai_usage_cost/sources/__init__.py` | none | `tests/test_api.py`, `tests/test_cline.py`, `tests/test_copilot_cli.py` and 6 more |
| `src/ai_usage_cost/sources/antigravity.py` | none | `tests/test_antigravity.py`, `tests/test_trace_antigravity.py` |
| `src/ai_usage_cost/sources/base.py` | none | `tests/test_claude_code.py`, `tests/test_cline.py`, `tests/test_codex.py` and 4 more |
| `src/ai_usage_cost/sources/claude_code.py` | none | `tests/test_claude_code.py`, `tests/test_insights.py`, `tests/test_trace_claude_code.py` |
| `src/ai_usage_cost/sources/cline.py` | none | `tests/test_cline.py` |
| `src/ai_usage_cost/sources/codex.py` | none | `tests/test_codex.py`, `tests/test_trace_codex.py` |
| `src/ai_usage_cost/sources/copilot_chat.py` | none | `tests/test_copilot_chat.py` |
| `src/ai_usage_cost/sources/copilot_cli.py` | none | `tests/test_copilot_cli.py` |
| `src/ai_usage_cost/sources/cursor.py` | none | `tests/test_cursor.py` |
| `src/ai_usage_cost/sources/dyad.py` | none | `tests/test_dyad.py` |
| `src/ai_usage_cost/sources/gemini_cli.py` | none | `tests/test_gemini_cli.py` |
| `src/ai_usage_cost/sources/grok_build.py` | none | `tests/test_grok_build.py` |
| `src/ai_usage_cost/sources/jan.py` | none | `tests/test_jan.py` |
| `src/ai_usage_cost/sources/kilo_code.py` | none | `tests/test_kilo_code.py` |
| `src/ai_usage_cost/sources/kilo_legacy.py` | none | `tests/test_cline.py` |
| `src/ai_usage_cost/sources/muse_code.py` | none | `tests/test_muse_code.py` |
| `src/ai_usage_cost/sources/ollama_app.py` | none | `tests/test_ollama_app.py` |
| `src/ai_usage_cost/sources/openai_compat.py` | none | `tests/test_openai_compat.py` |
| `src/ai_usage_cost/sources/opencode.py` | none | `tests/test_opencode.py` |
| `src/ai_usage_cost/sources/qwen_code.py` | none | `tests/test_qwen_code.py` |
| `src/ai_usage_cost/sources/roo_code.py` | none | `tests/test_cline.py` |
| `src/ai_usage_cost/sources/windsurf.py` | none | `tests/test_windsurf.py` |
| `src/ai_usage_cost/store.py` | none | `tests/test_cline.py`, `tests/test_collect.py`, `tests/test_copilot_cli.py` and 6 more |
| `src/ai_usage_cost/trace.py` | none | `tests/test_insights.py`, `tests/test_pricing_v2.py`, `tests/test_privacy.py` and 4 more |
| `src/ai_usage_cost/tui.py` | none | none |
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> docs/chunk-ch-localtokenomics-web-src-components-ui
| `web/eslint.config.js` | none | none |
| `web/src/App.tsx` | none | none |
| `web/src/ContextTab.tsx` | none | none |
| `web/src/EconomicsTab.tsx` | none | `web/src/EconomicsTab.test.ts` |
| `web/src/FilterRail.tsx` | none | none |
| `web/src/Header.tsx` | none | none |
| `web/src/Overview.tsx` | none | none |
| `web/src/Pricing.tsx` | none | `web/src/Pricing.test.ts` |
| `web/src/SessionWorkspace.tsx` | none | none |
| `web/src/Sessions.tsx` | none | none |
| `web/src/Sources.tsx` | none | none |
| `web/src/TraceTab.tsx` | none | `web/src/TraceTab.test.ts` |
| `web/src/api.ts` | none | `web/src/EconomicsTab.test.ts`, `web/src/Pricing.test.ts`, `web/src/TraceTab.test.ts` and 2 more |
| `web/src/components/chart-hover.tsx` | none | none |
| `web/src/components/chart-time.tsx` | none | none |
| `web/src/components/columns.tsx` | none | none |
| `web/src/components/detail.tsx` | none | none |
| `web/src/components/filters.tsx` | none | none |
| `web/src/components/metric-info.tsx` | none | `web/src/components/metric-info.test.tsx` |
| `web/src/components/panel.tsx` | none | none |
| `web/src/components/rank.ts` | none | `web/src/components/rank.test.ts` |
| `web/src/components/series.ts` | none | none |
| `web/src/components/session.tsx` | none | none |
| `web/src/components/source-card.tsx` | none | none |
| `web/src/components/sparkline.tsx` | none | `web/src/components/sparkline.test.ts` |
| `web/src/components/stat.tsx` | none | none |
| `web/src/components/states.tsx` | none | none |
| `web/src/components/status.tsx` | none | none |
| `web/src/components/trace.tsx` | none | none |
<<<<<<< HEAD
| `web/src/components/ui/accordion.tsx` | none | none |
| `web/src/components/ui/alert.tsx` | none | none |
| `web/src/components/ui/badge.tsx` | none | none |
| `web/src/components/ui/button.tsx` | none | none |
| `web/src/components/ui/chart.tsx` | none | none |
| `web/src/components/ui/checkbox.tsx` | none | none |
| `web/src/components/ui/collapsible.tsx` | none | none |
| `web/src/components/ui/dialog.tsx` | none | none |
| `web/src/components/ui/dropdown-menu.tsx` | none | none |
| `web/src/components/ui/input.tsx` | none | none |
| `web/src/components/ui/label.tsx` | none | none |
| `web/src/components/ui/popover.tsx` | none | none |
| `web/src/components/ui/progress.tsx` | none | none |
| `web/src/components/ui/select.tsx` | none | none |
| `web/src/components/ui/separator.tsx` | none | none |
| `web/src/components/ui/sheet.tsx` | none | none |
| `web/src/components/ui/skeleton.tsx` | none | none |
| `web/src/components/ui/sonner.tsx` | none | none |
| `web/src/components/ui/switch.tsx` | none | none |
| `web/src/components/ui/table.tsx` | none | none |
| `web/src/components/ui/tabs.tsx` | none | none |
| `web/src/components/ui/textarea.tsx` | none | none |
| `web/src/components/ui/toggle-group.tsx` | none | none |
| `web/src/components/ui/toggle.tsx` | none | none |
| `web/src/components/ui/tooltip.tsx` | none | none |
=======
| `web/src/components/ui/accordion.tsx` | [[Web ui UI components API]], [[Web ui UI components Data Model]], [[Web ui UI components Diagrams]], [[Web ui UI components Operations]], [[Web ui UI components Overview]], [[Web ui UI components Security]], [[Web ui UI components Tests]], [[Web ui UI components Workflows]] | none |
| `web/src/components/ui/alert.tsx` | [[Web ui UI components API]], [[Web ui UI components Data Model]], [[Web ui UI components Diagrams]], [[Web ui UI components Operations]], [[Web ui UI components Overview]], [[Web ui UI components Security]], [[Web ui UI components Tests]], [[Web ui UI components Workflows]] | none |
| `web/src/components/ui/badge.tsx` | [[Web ui UI components API]], [[Web ui UI components Data Model]], [[Web ui UI components Diagrams]], [[Web ui UI components Operations]], [[Web ui UI components Overview]], [[Web ui UI components Security]], [[Web ui UI components Tests]], [[Web ui UI components Workflows]] | none |
| `web/src/components/ui/button.tsx` | [[Web ui UI components API]], [[Web ui UI components Data Model]], [[Web ui UI components Diagrams]], [[Web ui UI components Operations]], [[Web ui UI components Overview]], [[Web ui UI components Security]], [[Web ui UI components Tests]], [[Web ui UI components Workflows]] | none |
| `web/src/components/ui/chart.tsx` | [[Web ui UI components API]], [[Web ui UI components Data Model]], [[Web ui UI components Diagrams]], [[Web ui UI components Operations]], [[Web ui UI components Overview]], [[Web ui UI components Security]], [[Web ui UI components Tests]], [[Web ui UI components Workflows]] | none |
| `web/src/components/ui/checkbox.tsx` | [[Web ui UI components API]], [[Web ui UI components Data Model]], [[Web ui UI components Diagrams]], [[Web ui UI components Operations]], [[Web ui UI components Overview]], [[Web ui UI components Security]], [[Web ui UI components Tests]], [[Web ui UI components Workflows]] | none |
| `web/src/components/ui/collapsible.tsx` | [[Web ui UI components API]], [[Web ui UI components Data Model]], [[Web ui UI components Diagrams]], [[Web ui UI components Operations]], [[Web ui UI components Overview]], [[Web ui UI components Security]], [[Web ui UI components Tests]], [[Web ui UI components Workflows]] | none |
| `web/src/components/ui/dialog.tsx` | [[Web ui UI components API]], [[Web ui UI components Data Model]], [[Web ui UI components Diagrams]], [[Web ui UI components Operations]], [[Web ui UI components Overview]], [[Web ui UI components Security]], [[Web ui UI components Tests]], [[Web ui UI components Workflows]] | none |
| `web/src/components/ui/dropdown-menu.tsx` | [[Web ui UI components API]], [[Web ui UI components Data Model]], [[Web ui UI components Diagrams]], [[Web ui UI components Operations]], [[Web ui UI components Overview]], [[Web ui UI components Security]], [[Web ui UI components Tests]], [[Web ui UI components Workflows]] | none |
| `web/src/components/ui/input.tsx` | [[Web ui UI components API]], [[Web ui UI components Data Model]], [[Web ui UI components Diagrams]], [[Web ui UI components Operations]], [[Web ui UI components Overview]], [[Web ui UI components Security]], [[Web ui UI components Tests]], [[Web ui UI components Workflows]] | none |
| `web/src/components/ui/label.tsx` | [[Web ui UI components API]], [[Web ui UI components Data Model]], [[Web ui UI components Diagrams]], [[Web ui UI components Operations]], [[Web ui UI components Overview]], [[Web ui UI components Security]], [[Web ui UI components Tests]], [[Web ui UI components Workflows]] | none |
| `web/src/components/ui/popover.tsx` | [[Web ui UI components API]], [[Web ui UI components Data Model]], [[Web ui UI components Diagrams]], [[Web ui UI components Operations]], [[Web ui UI components Overview]], [[Web ui UI components Security]], [[Web ui UI components Tests]], [[Web ui UI components Workflows]] | none |
| `web/src/components/ui/progress.tsx` | [[Web ui UI components API]], [[Web ui UI components Data Model]], [[Web ui UI components Diagrams]], [[Web ui UI components Operations]], [[Web ui UI components Overview]], [[Web ui UI components Security]], [[Web ui UI components Tests]], [[Web ui UI components Workflows]] | none |
| `web/src/components/ui/select.tsx` | [[Web ui UI components API]], [[Web ui UI components Data Model]], [[Web ui UI components Diagrams]], [[Web ui UI components Operations]], [[Web ui UI components Overview]], [[Web ui UI components Security]], [[Web ui UI components Tests]], [[Web ui UI components Workflows]] | none |
| `web/src/components/ui/separator.tsx` | [[Web ui UI components API]], [[Web ui UI components Data Model]], [[Web ui UI components Diagrams]], [[Web ui UI components Operations]], [[Web ui UI components Overview]], [[Web ui UI components Security]], [[Web ui UI components Tests]], [[Web ui UI components Workflows]] | none |
| `web/src/components/ui/sheet.tsx` | [[Web ui UI components API]], [[Web ui UI components Data Model]], [[Web ui UI components Diagrams]], [[Web ui UI components Operations]], [[Web ui UI components Overview]], [[Web ui UI components Security]], [[Web ui UI components Tests]], [[Web ui UI components Workflows]] | none |
| `web/src/components/ui/skeleton.tsx` | [[Web ui UI components API]], [[Web ui UI components Data Model]], [[Web ui UI components Diagrams]], [[Web ui UI components Operations]], [[Web ui UI components Overview]], [[Web ui UI components Security]], [[Web ui UI components Tests]], [[Web ui UI components Workflows]] | none |
| `web/src/components/ui/sonner.tsx` | [[Web ui UI components API]], [[Web ui UI components Data Model]], [[Web ui UI components Diagrams]], [[Web ui UI components Operations]], [[Web ui UI components Overview]], [[Web ui UI components Security]], [[Web ui UI components Tests]], [[Web ui UI components Workflows]] | none |
| `web/src/components/ui/switch.tsx` | [[Web ui UI components API]], [[Web ui UI components Data Model]], [[Web ui UI components Diagrams]], [[Web ui UI components Operations]], [[Web ui UI components Overview]], [[Web ui UI components Security]], [[Web ui UI components Tests]], [[Web ui UI components Workflows]] | none |
| `web/src/components/ui/table.tsx` | [[Web ui UI components API]], [[Web ui UI components Data Model]], [[Web ui UI components Diagrams]], [[Web ui UI components Operations]], [[Web ui UI components Overview]], [[Web ui UI components Security]], [[Web ui UI components Tests]], [[Web ui UI components Workflows]] | none |
| `web/src/components/ui/tabs.tsx` | [[Web ui UI components API]], [[Web ui UI components Data Model]], [[Web ui UI components Diagrams]], [[Web ui UI components Operations]], [[Web ui UI components Overview]], [[Web ui UI components Security]], [[Web ui UI components Tests]], [[Web ui UI components Workflows]] | none |
| `web/src/components/ui/textarea.tsx` | [[Web ui UI components API]], [[Web ui UI components Data Model]], [[Web ui UI components Diagrams]], [[Web ui UI components Operations]], [[Web ui UI components Overview]], [[Web ui UI components Security]], [[Web ui UI components Tests]], [[Web ui UI components Workflows]] | none |
| `web/src/components/ui/toggle-group.tsx` | [[Web ui UI components API]], [[Web ui UI components Data Model]], [[Web ui UI components Diagrams]], [[Web ui UI components Operations]], [[Web ui UI components Overview]], [[Web ui UI components Security]], [[Web ui UI components Tests]], [[Web ui UI components Workflows]] | none |
| `web/src/components/ui/toggle.tsx` | [[Web ui UI components API]], [[Web ui UI components Data Model]], [[Web ui UI components Diagrams]], [[Web ui UI components Operations]], [[Web ui UI components Overview]], [[Web ui UI components Security]], [[Web ui UI components Tests]], [[Web ui UI components Workflows]] | none |
| `web/src/components/ui/tooltip.tsx` | [[Web ui UI components API]], [[Web ui UI components Data Model]], [[Web ui UI components Diagrams]], [[Web ui UI components Operations]], [[Web ui UI components Overview]], [[Web ui UI components Security]], [[Web ui UI components Tests]], [[Web ui UI components Workflows]] | none |
>>>>>>> docs/chunk-ch-localtokenomics-web-src-components-ui
| `web/src/components/use-media-query.ts` | none | none |
| `web/src/components/workspace-panel.ts` | none | none |
| `web/src/design-system/cn.ts` | none | none |
| `web/src/format.ts` | none | `web/src/format.test.ts` |
| `web/src/main.tsx` | none | none |
| `web/src/pricing-format.ts` | none | `web/src/pricing-format.test.ts` |
| `web/src/pricing-notes.ts` | none | `web/src/pricing-notes.test.ts` |
<<<<<<< HEAD
| `web/src/prototype/Gallery.tsx` | [[Web prototype API]], [[Web prototype C4 components]], [[Web prototype Data Model]], [[Web prototype Diagrams]], [[Web prototype Operations]], [[Web prototype Overview]], [[Web prototype Security]], [[Web prototype Tests]], [[Web prototype Workflows]] | none |
| `web/src/prototype/OverviewScreen.tsx` | [[Web prototype API]], [[Web prototype C4 components]], [[Web prototype Data Model]], [[Web prototype Diagrams]], [[Web prototype Operations]], [[Web prototype Overview]], [[Web prototype Security]], [[Web prototype Tests]], [[Web prototype Workflows]] | none |
| `web/src/prototype/PricingScreen.tsx` | [[Web prototype API]], [[Web prototype C4 components]], [[Web prototype Data Model]], [[Web prototype Diagrams]], [[Web prototype Operations]], [[Web prototype Overview]], [[Web prototype Security]], [[Web prototype Tests]], [[Web prototype Workflows]] | none |
| `web/src/prototype/Prototype.tsx` | [[Web prototype API]], [[Web prototype C4 components]], [[Web prototype Data Model]], [[Web prototype Diagrams]], [[Web prototype Operations]], [[Web prototype Overview]], [[Web prototype Security]], [[Web prototype Tests]], [[Web prototype Workflows]] | none |
| `web/src/prototype/Rail.tsx` | [[Web prototype API]], [[Web prototype C4 components]], [[Web prototype Data Model]], [[Web prototype Diagrams]], [[Web prototype Operations]], [[Web prototype Overview]], [[Web prototype Security]], [[Web prototype Tests]], [[Web prototype Workflows]] | none |
| `web/src/prototype/Screens.tsx` | [[Web prototype API]], [[Web prototype C4 components]], [[Web prototype Data Model]], [[Web prototype Diagrams]], [[Web prototype Operations]], [[Web prototype Overview]], [[Web prototype Security]], [[Web prototype Tests]], [[Web prototype Workflows]] | none |
| `web/src/prototype/SessionsScreen.tsx` | [[Web prototype API]], [[Web prototype C4 components]], [[Web prototype Data Model]], [[Web prototype Diagrams]], [[Web prototype Operations]], [[Web prototype Overview]], [[Web prototype Security]], [[Web prototype Tests]], [[Web prototype Workflows]] | none |
| `web/src/prototype/SourcesScreen.tsx` | [[Web prototype API]], [[Web prototype C4 components]], [[Web prototype Data Model]], [[Web prototype Diagrams]], [[Web prototype Operations]], [[Web prototype Overview]], [[Web prototype Security]], [[Web prototype Tests]], [[Web prototype Workflows]] | none |
| `web/src/prototype/data.ts` | [[Web prototype API]], [[Web prototype C4 components]], [[Web prototype Data Model]], [[Web prototype Diagrams]], [[Web prototype Operations]], [[Web prototype Overview]], [[Web prototype Security]], [[Web prototype Tests]], [[Web prototype Workflows]] | none |
| `web/src/prototype/main.tsx` | [[Web prototype API]], [[Web prototype C4 components]], [[Web prototype Data Model]], [[Web prototype Diagrams]], [[Web prototype Operations]], [[Web prototype Overview]], [[Web prototype Security]], [[Web prototype Tests]], [[Web prototype Workflows]] | none |
=======
| `web/src/prototype/Gallery.tsx` | none | none |
| `web/src/prototype/OverviewScreen.tsx` | none | none |
| `web/src/prototype/PricingScreen.tsx` | none | none |
| `web/src/prototype/Prototype.tsx` | none | none |
| `web/src/prototype/Rail.tsx` | none | none |
| `web/src/prototype/Screens.tsx` | none | none |
| `web/src/prototype/SessionsScreen.tsx` | none | none |
| `web/src/prototype/SourcesScreen.tsx` | none | none |
| `web/src/prototype/data.ts` | none | none |
| `web/src/prototype/main.tsx` | none | none |
>>>>>>> docs/chunk-ch-localtokenomics-web-src-components-ui
| `web/src/test-setup.ts` | none | none |
| `web/src/theme.ts` | none | none |
| `web/src/turn-insights.ts` | none | `web/src/turn-insights.test.ts` |
| `web/vite.config.ts` | none | none |
<<<<<<< HEAD
=======
| `web/eslint.config.js` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/App.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/ContextTab.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/EconomicsTab.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | `web/src/EconomicsTab.test.ts` |
| `web/src/FilterRail.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/Header.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/Overview.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/Pricing.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | `web/src/Pricing.test.ts` |
| `web/src/SessionWorkspace.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/Sessions.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/Sources.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/TraceTab.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | `web/src/TraceTab.test.ts` |
| `web/src/api.ts` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | `web/src/EconomicsTab.test.ts`, `web/src/Pricing.test.ts`, `web/src/TraceTab.test.ts` and 2 more |
| `web/src/components/chart-hover.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/components/chart-time.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/components/columns.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/components/detail.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/components/filters.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/components/metric-info.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | `web/src/components/metric-info.test.tsx` |
| `web/src/components/panel.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/components/rank.ts` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | `web/src/components/rank.test.ts` |
| `web/src/components/series.ts` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/components/session.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/components/source-card.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/components/sparkline.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | `web/src/components/sparkline.test.ts` |
| `web/src/components/stat.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/components/states.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/components/status.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/components/trace.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/components/ui/accordion.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/components/ui/alert.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/components/ui/badge.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/components/ui/button.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/components/ui/chart.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/components/ui/checkbox.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/components/ui/collapsible.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/components/ui/dialog.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/components/ui/dropdown-menu.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/components/ui/input.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/components/ui/label.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/components/ui/popover.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/components/ui/progress.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/components/ui/select.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/components/ui/separator.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/components/ui/sheet.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/components/ui/skeleton.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/components/ui/sonner.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/components/ui/switch.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/components/ui/table.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/components/ui/tabs.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/components/ui/textarea.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/components/ui/toggle-group.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/components/ui/toggle.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/components/ui/tooltip.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/components/use-media-query.ts` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/components/workspace-panel.ts` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/design-system/cn.ts` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/format.ts` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | `web/src/format.test.ts` |
| `web/src/main.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/pricing-format.ts` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | `web/src/pricing-format.test.ts` |
| `web/src/pricing-notes.ts` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | `web/src/pricing-notes.test.ts` |
| `web/src/prototype/Gallery.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/prototype/OverviewScreen.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/prototype/PricingScreen.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/prototype/Prototype.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/prototype/Rail.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/prototype/Screens.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/prototype/SessionsScreen.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/prototype/SourcesScreen.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/prototype/data.ts` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/prototype/main.tsx` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/test-setup.ts` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/theme.ts` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
| `web/src/turn-insights.ts` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | `web/src/turn-insights.test.ts` |
| `web/vite.config.ts` | [[LocalTokenomics root wiring]], [[localtokenomics root API]], [[localtokenomics root Data Model]], [[localtokenomics root Diagrams]], [[localtokenomics root Operations]], [[localtokenomics root Overview]], [[localtokenomics root Security]], [[localtokenomics root Tests]], [[localtokenomics root Workflows]] | none |
>>>>>>> docs/chunk-ch-localtokenomics-root
=======
| `web/eslint.config.js` | none | none |
| `web/src/App.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/ContextTab.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/EconomicsTab.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | `web/src/EconomicsTab.test.ts` |
| `web/src/FilterRail.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/Header.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/Overview.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/Pricing.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | `web/src/Pricing.test.ts` |
| `web/src/SessionWorkspace.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/Sessions.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/Sources.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/TraceTab.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | `web/src/TraceTab.test.ts` |
| `web/src/api.ts` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | `web/src/EconomicsTab.test.ts`, `web/src/Pricing.test.ts`, `web/src/TraceTab.test.ts` and 2 more |
| `web/src/components/chart-hover.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/components/chart-time.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/components/columns.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/components/detail.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/components/filters.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/components/metric-info.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | `web/src/components/metric-info.test.tsx` |
| `web/src/components/panel.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/components/rank.ts` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | `web/src/components/rank.test.ts` |
| `web/src/components/series.ts` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/components/session.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/components/source-card.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/components/sparkline.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | `web/src/components/sparkline.test.ts` |
| `web/src/components/stat.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/components/states.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/components/status.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/components/trace.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/components/ui/accordion.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/components/ui/alert.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/components/ui/badge.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/components/ui/button.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/components/ui/chart.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/components/ui/checkbox.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/components/ui/collapsible.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/components/ui/dialog.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/components/ui/dropdown-menu.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/components/ui/input.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/components/ui/label.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/components/ui/popover.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/components/ui/progress.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/components/ui/select.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/components/ui/separator.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/components/ui/sheet.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/components/ui/skeleton.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/components/ui/sonner.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/components/ui/switch.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/components/ui/table.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/components/ui/tabs.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/components/ui/textarea.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/components/ui/toggle-group.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/components/ui/toggle.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/components/ui/tooltip.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/components/use-media-query.ts` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/components/workspace-panel.ts` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/design-system/cn.ts` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/format.ts` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | `web/src/format.test.ts` |
| `web/src/main.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/pricing-format.ts` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | `web/src/pricing-format.test.ts` |
| `web/src/pricing-notes.ts` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | `web/src/pricing-notes.test.ts` |
| `web/src/prototype/Gallery.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/prototype/OverviewScreen.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/prototype/PricingScreen.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/prototype/Prototype.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/prototype/Rail.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/prototype/Screens.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/prototype/SessionsScreen.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/prototype/SourcesScreen.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/prototype/data.ts` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/prototype/main.tsx` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/test-setup.ts` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/theme.ts` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | none |
| `web/src/turn-insights.ts` | [[Web API]], [[Web Dashboard Components]], [[Web Data Model]], [[Web Diagrams]], [[Web Operations]], [[Web Overview]], [[Web Security]], [[Web Tests]], [[Web Workflows]] | `web/src/turn-insights.test.ts` |
| `web/vite.config.ts` | none | none |
>>>>>>> docs/chunk-ch-localtokenomics-web-src
=======
>>>>>>> docs/chunk-ch-localtokenomics-web-src-components-ui
%% generated:coverage-map end %%
