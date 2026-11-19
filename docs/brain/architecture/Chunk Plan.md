---
title: Chunk Plan
aliases: []
tags: [overview, index]
area: architecture
status: active
audience: internal
maturity: draft
confidence: inferred
covers: []
chunks:
- id: ch-localtokenomics-root
  title: localtokenomics root
  repo: localtokenomics
  components: ['localtokenomics:root']
  globs: [web/*]
  depends_on: []
  state: approved
  display_name: localtokenomics root
  files: 2
  lines: 56
  paths: [web/eslint.config.js, web/vite.config.ts]
  recommended: {c4: 2 files form this module; shows what it contains and depends on,
    mind-map: 2 files; the concepts of this module in one picture for a newcomer,
    component-tree: 79 UI components; shows which renders which, screen-map: 1 page
      component; one annotated map per screen, wireframe: '8 forms, tables or dialogs;
      the static layout of a region', state-chart: 'UI branches for empty, error,
      loading; how the component moves between them', screen-flow: 1 page component;
      how the user moves between them, config-map: 2 configuration files; names and
      who reads them, error-flow: '2 located refusals, assertions or validators; how
      failures are handled', glossary-map: 0 entities and 28 enums name domain terms,
    package-tree: 86 files in 6 folders; the structure of this module}
  diagrams: [c4, mind-map, capability, config-map, package-tree]
  diagrams_confirmed: true
  estimate: {tokens: 78223, minutes: 9, note: rough estimate; tune after the first
      runs}
  existing_docs: stale
  approved_by: human
  approved_at: '2026-11-19T00:10:32+00:00'
- id: ch-localtokenomics-src-ai-usage-cost-sources
  title: src/ai_usage_cost/sources
  repo: localtokenomics
  components: ['localtokenomics:src-ai-usage-cost-sources']
  globs: [src/ai_usage_cost/sources/**]
  depends_on: [ch-localtokenomics-src-ai-usage-cost]
  state: approved
  display_name: Ai usage cost sources
  files: 22
  lines: 4722
  paths: [src/ai_usage_cost/sources/__init__.py, src/ai_usage_cost/sources/antigravity.py,
    src/ai_usage_cost/sources/base.py, src/ai_usage_cost/sources/claude_code.py, src/ai_usage_cost/sources/cline.py,
    src/ai_usage_cost/sources/codex.py, src/ai_usage_cost/sources/copilot_chat.py,
    src/ai_usage_cost/sources/copilot_cli.py, src/ai_usage_cost/sources/cursor.py,
    src/ai_usage_cost/sources/dyad.py, src/ai_usage_cost/sources/gemini_cli.py, src/ai_usage_cost/sources/grok_build.py,
    src/ai_usage_cost/sources/jan.py, src/ai_usage_cost/sources/kilo_code.py, src/ai_usage_cost/sources/kilo_legacy.py,
    src/ai_usage_cost/sources/muse_code.py, src/ai_usage_cost/sources/ollama_app.py,
    src/ai_usage_cost/sources/openai_compat.py, src/ai_usage_cost/sources/opencode.py,
    src/ai_usage_cost/sources/qwen_code.py, src/ai_usage_cost/sources/roo_code.py,
    src/ai_usage_cost/sources/windsurf.py]
  recommended: {c4: 22 files form this module; shows what it contains and depends
      on, mind-map: 22 files; the concepts of this module in one picture for a newcomer,
    class: 2 types with fields and relations that are not tables, data-lineage: 2
      entities; where their data comes from and where it goes, dfd: 'data moves between
      routes, stores and callers', module-dependency: 36 imports cross this module's
      border, glossary-map: 2 entities and 1 enums name domain terms}
  diagrams: [c4, mind-map, class, data-lineage, dfd, module-dependency, glossary-map]
  diagrams_confirmed: true
  estimate: {tokens: 160113, minutes: 18, note: rough estimate; tune after the first
      runs}
  existing_docs: covered
  approved_by: human
  approved_at: '2026-11-19T00:12:16+00:00'
- id: ch-localtokenomics-src-ai-usage-cost
  title: src/ai_usage_cost
  repo: localtokenomics
  components: ['localtokenomics:src-ai-usage-cost']
  globs: [src/ai_usage_cost/*]
  depends_on: [ch-localtokenomics-src-ai-usage-cost-render, ch-localtokenomics-src-ai-usage-cost-sources]
  state: approved
  display_name: Ai usage cost
  files: 13
  lines: 5069
  paths: [src/ai_usage_cost/__init__.py, src/ai_usage_cost/aggregate.py, src/ai_usage_cost/api.py,
    src/ai_usage_cost/cli.py, src/ai_usage_cost/collect.py, src/ai_usage_cost/demo.py,
    src/ai_usage_cost/models.py, src/ai_usage_cost/pipeline.py, src/ai_usage_cost/pricing.py,
    src/ai_usage_cost/privacy.py, src/ai_usage_cost/store.py, src/ai_usage_cost/trace.py,
    src/ai_usage_cost/tui.py]
  recommended: {c4: 13 files form this module; shows what it contains and depends
      on, mind-map: 13 files; the concepts of this module in one picture for a newcomer,
    api-map: '12 routes; endpoints grouped by resource with method, auth and handler',
    sequence: 12 routes; one sequence per key route, use-case-diagram: 12 routes serve
      actors; one use case per goal they serve, flowchart: handlers with branching
      logic, erd: 6 tables or mapped entities are defined here, erd-conceptual: enough
      tables that a concept-level view helps, class: 45 types with fields and relations
      that are not tables, data-lineage: 51 entities; where their data comes from
      and where it goes, state: 'status or lifecycle fields on EconRow, OutcomeSignals,
      PricedEvent', dfd: 'data moves between routes, stores and callers', activity: '2
      job or script files (collect.py, pipeline.py); the steps, decisions and parallel
      work', timeline: '2 job or script files (collect.py, pipeline.py); what runs
      when', gantt: '2 job or script files (collect.py, pipeline.py); the schedule
      laid over time', bpmn: 'several actors, outgoing calls or job-like files', error-flow: '27
      located refusals, assertions or validators; how failures are handled', glossary-map: 51
      entities and 9 enums name domain terms, package-tree: 38 files in 3 folders;
      the structure of this module}
  diagrams: [c4, mind-map, api-map, sequence, use-case-diagram, flowchart, erd, erd-conceptual,
    class, data-lineage, state, dfd, activity, timeline, gantt, bpmn, error-flow,
    glossary-map, package-tree]
  diagrams_confirmed: true
  estimate: {tokens: 220126, minutes: 24, note: rough estimate; tune after the first
      runs}
  existing_docs: stale
  approved_by: human
  approved_at: '2026-11-19T06:39:10+00:00'
- id: ch-localtokenomics-src-ai-usage-cost-render
  title: src/ai_usage_cost/render
  repo: localtokenomics
  components: ['localtokenomics:src-ai-usage-cost-render']
  globs: [src/ai_usage_cost/render/**]
  depends_on: [ch-localtokenomics-src-ai-usage-cost]
  state: approved
  display_name: Ai usage cost render
  files: 3
  lines: 187
  paths: [src/ai_usage_cost/render/__init__.py, src/ai_usage_cost/render/png.py, src/ai_usage_cost/render/terminal.py]
  recommended: {c4: 3 files form this module; shows what it contains and depends on,
    mind-map: 3 files; the concepts of this module in one picture for a newcomer,
    module-dependency: 2 imports cross this module's border}
  diagrams: [c4, mind-map, module-dependency]
  diagrams_confirmed: true
  estimate: {tokens: 71167, minutes: 8, note: rough estimate; tune after the first
      runs}
  existing_docs: none
  approved_by: human
  approved_at: '2026-11-18T19:06:21+00:00'
- id: ch-localtokenomics-web-src-components
  title: web/src/components
  repo: localtokenomics
  components: ['localtokenomics:web-src-components']
  globs: [web/src/components/*]
  depends_on: [ch-localtokenomics-web-src, ch-localtokenomics-web-src-components-ui]
  state: approved
  display_name: Web UI components
  files: 18
  lines: 3024
  paths: [web/src/components/chart-hover.tsx, web/src/components/chart-time.tsx, web/src/components/columns.tsx,
    web/src/components/detail.tsx, web/src/components/filters.tsx, web/src/components/metric-info.tsx,
    web/src/components/panel.tsx, web/src/components/rank.ts, web/src/components/series.ts,
    web/src/components/session.tsx, web/src/components/source-card.tsx, web/src/components/sparkline.tsx,
    web/src/components/stat.tsx, web/src/components/states.tsx, web/src/components/status.tsx,
    web/src/components/trace.tsx, web/src/components/use-media-query.ts, web/src/components/workspace-panel.ts]
  recommended: {c4: 18 files form this module; shows what it contains and depends
      on, mind-map: 18 files; the concepts of this module in one picture for a newcomer,
    component-tree: 57 UI components; shows which renders which, screen-map: '57 UI
      components, none named like a screen; one annotated map per screen', wireframe: '1
      forms, tables or dialogs; the static layout of a region', state-chart: 'UI branches
      for empty, error; how the component moves between them', screen-flow: '57 UI
      components, none named like a screen; how the user moves between them', module-dependency: 44
      imports cross this module's border, error-flow: '1 located refusals, assertions
      or validators; how failures are handled'}
  diagrams: [c4, mind-map, component-tree, screen-map, wireframe, state-chart, screen-flow,
    module-dependency, error-flow]
  diagrams_confirmed: true
  estimate: {tokens: 142724, minutes: 16, note: rough estimate; tune after the first
      runs}
  existing_docs: none
  approved_by: human
  approved_at: '2026-11-18T19:03:01+00:00'
- id: ch-localtokenomics-web-src
  title: web/src
  repo: localtokenomics
  components: ['localtokenomics:web-src']
  globs: [web/src/*, web/src/design-system/*]
  depends_on: [ch-localtokenomics-web-src-components, ch-localtokenomics-web-src-components-ui]
  state: approved
  display_name: Web
  files: 20
  lines: 7127
  paths: [web/src/App.tsx, web/src/ContextTab.tsx, web/src/EconomicsTab.tsx, web/src/FilterRail.tsx,
    web/src/Header.tsx, web/src/Overview.tsx, web/src/Pricing.tsx, web/src/SessionWorkspace.tsx,
    web/src/Sessions.tsx, web/src/Sources.tsx, web/src/TraceTab.tsx, web/src/api.ts,
    web/src/design-system/cn.ts, web/src/format.ts, web/src/main.tsx, web/src/pricing-format.ts,
    web/src/pricing-notes.ts, web/src/test-setup.ts, web/src/theme.ts, web/src/turn-insights.ts]
  recommended: {c4: 20 files form this module; shows what it contains and depends
      on, mind-map: 20 files; the concepts of this module in one picture for a newcomer,
    component-tree: 78 UI components; shows which renders which, screen-map: 8 screen
      components; one annotated map per screen, wireframe: '8 forms, tables or dialogs;
      the static layout of a region', state-chart: 'UI branches for empty, error,
      loading; how the component moves between them', screen-flow: 8 screen components;
      how the user moves between them, sitemap: 8 screens; how they are grouped and
      nested, user-journey: 8 screens; the steps a user takes across them, error-flow: '2
      located refusals, assertions or validators; how failures are handled', glossary-map: 0
      entities and 28 enums name domain terms, package-tree: 83 files in 5 folders;
      the structure of this module}
  diagrams: [c4, mind-map, component-tree, screen-map, wireframe, state-chart, screen-flow,
    sitemap, user-journey, error-flow, glossary-map, package-tree]
  diagrams_confirmed: true
  estimate: {tokens: 220381, minutes: 24, note: rough estimate; tune after the first
      runs}
  existing_docs: stale
  approved_by: human
  approved_at: '2026-11-18T19:02:13+00:00'
- id: ch-localtokenomics-web-src-components-ui
  title: web/src/components/ui
  repo: localtokenomics
  components: ['localtokenomics:web-src-components-ui']
  globs: [web/src/components/ui/**]
  depends_on: [ch-localtokenomics-web-src]
  state: approved
  display_name: Web ui UI components
  files: 25
  lines: 2083
  paths: [web/src/components/ui/accordion.tsx, web/src/components/ui/alert.tsx, web/src/components/ui/badge.tsx,
    web/src/components/ui/button.tsx, web/src/components/ui/chart.tsx, web/src/components/ui/checkbox.tsx,
    web/src/components/ui/collapsible.tsx, web/src/components/ui/dialog.tsx, web/src/components/ui/dropdown-menu.tsx,
    web/src/components/ui/input.tsx, web/src/components/ui/label.tsx, web/src/components/ui/popover.tsx,
    web/src/components/ui/progress.tsx, web/src/components/ui/select.tsx, web/src/components/ui/separator.tsx,
    web/src/components/ui/sheet.tsx, web/src/components/ui/skeleton.tsx, web/src/components/ui/sonner.tsx,
    web/src/components/ui/switch.tsx, web/src/components/ui/table.tsx, web/src/components/ui/tabs.tsx,
    web/src/components/ui/textarea.tsx, web/src/components/ui/toggle-group.tsx, web/src/components/ui/toggle.tsx,
    web/src/components/ui/tooltip.tsx]
  recommended: {c4: 25 files form this module; shows what it contains and depends
      on, mind-map: 25 files; the concepts of this module in one picture for a newcomer,
    module-dependency: 24 imports cross this module's border, error-flow: '1 located
      refusals, assertions or validators; how failures are handled'}
  diagrams: [c4, mind-map, module-dependency, error-flow]
  diagrams_confirmed: true
  estimate: {tokens: 105294, minutes: 12, note: rough estimate; tune after the first
      runs}
  existing_docs: none
  approved_by: human
  approved_at: '2026-11-18T19:04:28+00:00'
- id: ch-localtokenomics-web-src-prototype
  title: web/src/prototype
  repo: localtokenomics
  components: ['localtokenomics:web-src-prototype']
  globs: [web/src/prototype/**]
  depends_on: [ch-localtokenomics-web-src, ch-localtokenomics-web-src-components,
    ch-localtokenomics-web-src-components-ui]
  state: approved
  display_name: Web prototype
  files: 10
  lines: 3215
  paths: [web/src/prototype/Gallery.tsx, web/src/prototype/OverviewScreen.tsx, web/src/prototype/PricingScreen.tsx,
    web/src/prototype/Prototype.tsx, web/src/prototype/Rail.tsx, web/src/prototype/Screens.tsx,
    web/src/prototype/SessionsScreen.tsx, web/src/prototype/SourcesScreen.tsx, web/src/prototype/data.ts,
    web/src/prototype/main.tsx]
  recommended: {c4: 10 files form this module; shows what it contains and depends
      on, mind-map: 10 files; the concepts of this module in one picture for a newcomer,
    component-tree: 10 UI components; shows which renders which, screen-map: 4 screen
      components; one annotated map per screen, wireframe: '4 forms, tables or dialogs;
      the static layout of a region', state-chart: UI branches for error; how the
      component moves between them, screen-flow: 4 screen components; how the user
      moves between them, sitemap: 4 screens; how they are grouped and nested, user-journey: 4
      screens; the steps a user takes across them, module-dependency: 88 imports cross
      this module's border, glossary-map: 0 entities and 4 enums name domain terms}
  diagrams: [c4, mind-map, component-tree, screen-map, wireframe, state-chart, screen-flow,
    sitemap, user-journey, module-dependency, glossary-map]
  diagrams_confirmed: true
  estimate: {tokens: 154804, minutes: 17, note: rough estimate; tune after the first
      runs}
  existing_docs: stale
  approved_by: human
  approved_at: '2026-11-18T18:48:19+00:00'
plan_approved_by: human
plan_approved_at: '2026-11-18T22:51:39+00:00'
---

# Chunk Plan

The ordered plan for documenting this codebase one chunk at a time. Edit the `chunks` list in the frontmatter to reorder, rename, split or skip chunks; nothing is documented before the plan is approved.

%% generated:plan-table start (do not edit; run brain docs generate) %%
| Chunk | Title | State | Depends on | Files | Lines | Est. tokens | Diagrams | Existing docs |
|---|---|---|---|---|---|---|---|---|
| ch-localtokenomics-root | localtokenomics root | approved | - | 2 | 56 | 78223 | c4, mind-map, capability, config-map, package-tree | stale |
| ch-localtokenomics-src-ai-usage-cost-sources | src/ai_usage_cost/sources | approved | ch-localtokenomics-src-ai-usage-cost | 22 | 4722 | 160113 | c4, mind-map, class, data-lineage, dfd, module-dependency, glossary-map | covered |
| ch-localtokenomics-src-ai-usage-cost | src/ai_usage_cost | approved | ch-localtokenomics-src-ai-usage-cost-render, ch-localtokenomics-src-ai-usage-cost-sources | 13 | 5069 | 220126 | c4, mind-map, api-map, sequence, use-case-diagram, flowchart, erd, erd-conceptual, class, data-lineage, state, dfd, activity, timeline, gantt, bpmn, error-flow, glossary-map, package-tree | stale |
| ch-localtokenomics-src-ai-usage-cost-render | src/ai_usage_cost/render | approved | ch-localtokenomics-src-ai-usage-cost | 3 | 187 | 71167 | c4, mind-map, module-dependency | none |
| ch-localtokenomics-web-src-components | web/src/components | approved | ch-localtokenomics-web-src, ch-localtokenomics-web-src-components-ui | 18 | 3024 | 142724 | c4, mind-map, component-tree, screen-map, wireframe, state-chart, screen-flow, module-dependency, error-flow | none |
| ch-localtokenomics-web-src | web/src | approved | ch-localtokenomics-web-src-components, ch-localtokenomics-web-src-components-ui | 20 | 7127 | 220381 | c4, mind-map, component-tree, screen-map, wireframe, state-chart, screen-flow, sitemap, user-journey, error-flow, glossary-map, package-tree | stale |
| ch-localtokenomics-web-src-components-ui | web/src/components/ui | approved | ch-localtokenomics-web-src | 25 | 2083 | 105294 | c4, mind-map, module-dependency, error-flow | none |
| ch-localtokenomics-web-src-prototype | web/src/prototype | approved | ch-localtokenomics-web-src, ch-localtokenomics-web-src-components, ch-localtokenomics-web-src-components-ui | 10 | 3215 | 154804 | c4, mind-map, component-tree, screen-map, wireframe, state-chart, screen-flow, sitemap, user-journey, module-dependency, glossary-map | stale |
%% generated:plan-table end %%
