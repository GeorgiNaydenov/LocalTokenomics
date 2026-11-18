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
  state: planned
  display_name: localtokenomics root
  files: 2
  lines: 56
  recommended: {c4: 2 files form this module; shows what it contains and depends on}
  diagrams: [c4]
  diagrams_confirmed: true
  estimate: {tokens: 60023, minutes: 7, note: rough estimate; tune after the first
      runs}
  existing_docs: stale
- id: ch-localtokenomics-src-ai-usage-cost-sources
  title: src/ai_usage_cost/sources
  repo: localtokenomics
  components: ['localtokenomics:src-ai-usage-cost-sources']
  globs: [src/ai_usage_cost/sources/**]
  depends_on: [ch-localtokenomics-src-ai-usage-cost]
  state: planned
  display_name: Ai usage cost sources
  files: 22
  lines: 4722
  recommended: {c4: 22 files form this module; shows what it contains and depends
      on, dfd: 'data moves between routes, stores and callers'}
  diagrams: [c4, dfd]
  diagrams_confirmed: true
  estimate: {tokens: 137363, minutes: 15, note: rough estimate; tune after the first
      runs}
  existing_docs: covered
- id: ch-localtokenomics-src-ai-usage-cost
  title: src/ai_usage_cost
  repo: localtokenomics
  components: ['localtokenomics:src-ai-usage-cost']
  globs: [src/ai_usage_cost/*]
  depends_on: [ch-localtokenomics-src-ai-usage-cost-render, ch-localtokenomics-src-ai-usage-cost-sources]
  state: in-review
  display_name: Ai usage cost
  files: 13
  lines: 5069
  recommended: {c4: 13 files form this module; shows what it contains and depends
      on, erd: 6 tables or mapped entities are defined here, erd-conceptual: enough
      tables that a concept-level view helps, state: 'status or lifecycle fields on
      EconRow, OutcomeSignals, PricedEvent', sequence: 12 routes; one sequence per
      key route, flowchart: handlers with branching logic, dfd: 'data moves between
      routes, stores and callers', bpmn: 'several actors, outgoing calls or job-like
      files'}
  diagrams: [c4, erd, erd-conceptual, state, sequence, flowchart, dfd, bpmn]
  diagrams_confirmed: true
  estimate: {tokens: 170076, minutes: 19, note: rough estimate; tune after the first
      runs}
  existing_docs: stale
- id: ch-localtokenomics-src-ai-usage-cost-render
  title: src/ai_usage_cost/render
  repo: localtokenomics
  components: ['localtokenomics:src-ai-usage-cost-render']
  globs: [src/ai_usage_cost/render/**]
  depends_on: [ch-localtokenomics-src-ai-usage-cost]
  state: planned
  display_name: Ai usage cost render
  files: 3
  lines: 187
  recommended: {c4: 3 files form this module; shows what it contains and depends on}
  diagrams: [c4]
  diagrams_confirmed: true
  estimate: {tokens: 62067, minutes: 7, note: rough estimate; tune after the first
      runs}
  existing_docs: none
- id: ch-localtokenomics-web-src-components
  title: web/src/components
  repo: localtokenomics
  components: ['localtokenomics:web-src-components']
  globs: [web/src/components/*]
  depends_on: [ch-localtokenomics-web-src, ch-localtokenomics-web-src-components-ui]
  state: planned
  display_name: Web UI components
  files: 18
  lines: 3024
  recommended: {c4: 18 files form this module; shows what it contains and depends
      on}
  diagrams: [c4]
  diagrams_confirmed: true
  estimate: {tokens: 106324, minutes: 12, note: rough estimate; tune after the first
      runs}
  existing_docs: none
- id: ch-localtokenomics-web-src
  title: web/src
  repo: localtokenomics
  components: ['localtokenomics:web-src']
  globs: [web/src/*, web/src/design-system/*]
  depends_on: [ch-localtokenomics-web-src-components, ch-localtokenomics-web-src-components-ui]
  state: planned
  display_name: Web
  files: 20
  lines: 7127
  recommended: {c4: 20 files form this module; shows what it contains and depends
      on}
  diagrams: [c4]
  diagrams_confirmed: true
  estimate: {tokens: 170331, minutes: 19, note: rough estimate; tune after the first
      runs}
  existing_docs: stale
- id: ch-localtokenomics-web-src-components-ui
  title: web/src/components/ui
  repo: localtokenomics
  components: ['localtokenomics:web-src-components-ui']
  globs: [web/src/components/ui/**]
  depends_on: [ch-localtokenomics-web-src]
  state: planned
  display_name: Web ui UI components
  files: 25
  lines: 2083
  recommended: {c4: 25 files form this module; shows what it contains and depends
      on}
  diagrams: [c4]
  diagrams_confirmed: true
  estimate: {tokens: 91644, minutes: 10, note: rough estimate; tune after the first
      runs}
  existing_docs: none
- id: ch-localtokenomics-web-src-prototype
  title: web/src/prototype
  repo: localtokenomics
  components: ['localtokenomics:web-src-prototype']
  globs: [web/src/prototype/**]
  depends_on: [ch-localtokenomics-web-src, ch-localtokenomics-web-src-components,
    ch-localtokenomics-web-src-components-ui]
  state: planned
  display_name: Web prototype
  files: 10
  lines: 3215
  recommended: {c4: 10 files form this module; shows what it contains and depends
      on}
  diagrams: [c4]
  diagrams_confirmed: true
  estimate: {tokens: 109304, minutes: 12, note: rough estimate; tune after the first
      runs}
  existing_docs: stale
plan_approved_by: human
plan_approved_at: '2026-11-18T18:20:42+00:00'
---

# Chunk Plan

The ordered plan for documenting this codebase one chunk at a time. Edit the `chunks` list in the frontmatter to reorder, rename, split or skip chunks; nothing is documented before the plan is approved.

%% generated:plan-table start (do not edit; run brain docs generate) %%
| Chunk | Title | State | Depends on | Files | Lines | Est. tokens | Diagrams | Existing docs |
|---|---|---|---|---|---|---|---|---|
| ch-localtokenomics-root | localtokenomics root | planned | - | 2 | 56 | 60023 | c4 | stale |
| ch-localtokenomics-src-ai-usage-cost-sources | src/ai_usage_cost/sources | planned | ch-localtokenomics-src-ai-usage-cost | 22 | 4722 | 137363 | c4, dfd | covered |
| ch-localtokenomics-src-ai-usage-cost | src/ai_usage_cost | in-review | ch-localtokenomics-src-ai-usage-cost-render, ch-localtokenomics-src-ai-usage-cost-sources | 13 | 5069 | 170076 | c4, erd, erd-conceptual, state, sequence, flowchart, dfd, bpmn | stale |
| ch-localtokenomics-src-ai-usage-cost-render | src/ai_usage_cost/render | planned | ch-localtokenomics-src-ai-usage-cost | 3 | 187 | 62067 | c4 | none |
| ch-localtokenomics-web-src-components | web/src/components | planned | ch-localtokenomics-web-src, ch-localtokenomics-web-src-components-ui | 18 | 3024 | 106324 | c4 | none |
| ch-localtokenomics-web-src | web/src | planned | ch-localtokenomics-web-src-components, ch-localtokenomics-web-src-components-ui | 20 | 7127 | 170331 | c4 | stale |
| ch-localtokenomics-web-src-components-ui | web/src/components/ui | planned | ch-localtokenomics-web-src | 25 | 2083 | 91644 | c4 | none |
| ch-localtokenomics-web-src-prototype | web/src/prototype | planned | ch-localtokenomics-web-src, ch-localtokenomics-web-src-components, ch-localtokenomics-web-src-components-ui | 10 | 3215 | 109304 | c4 | stale |
%% generated:plan-table end %%
