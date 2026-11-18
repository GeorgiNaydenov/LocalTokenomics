---
title: Module Atlas
aliases: []
tags: [generated, index, module]
area: architecture
status: generated
audience: internal
maturity: approved
confidence: confirmed
covers: []
generated: true
---

# Module Atlas

Every component found in the code, with size and dependencies.

%% generated:module-atlas start (do not edit; run brain docs generate) %%
| Component | Repo | Language | Files | Lines | Depends on |
|---|---|---|---|---|---|
| `(root)` | localtokenomics | python | 2 | 1668 | `localtokenomics:src-ai-usage-cost` |
| `src/ai_usage_cost` | localtokenomics | python | 13 | 5069 | `localtokenomics:src-ai-usage-cost-sources`, `localtokenomics:src-ai-usage-cost-render` |
| `src/ai_usage_cost/render` | localtokenomics | python | 3 | 187 | `localtokenomics:src-ai-usage-cost` |
| `src/ai_usage_cost/sources` | localtokenomics | python | 22 | 4722 | `localtokenomics:src-ai-usage-cost` |
| `(root)` | localtokenomics | typescript | 2 | 56 | - |
| `web/src` | localtokenomics | typescript | 20 | 7127 | `localtokenomics:web-src-components`, `localtokenomics:web-src-components-ui` |
| `web/src/components` | localtokenomics | typescript | 18 | 3024 | `localtokenomics:web-src`, `localtokenomics:web-src-components-ui` |
| `web/src/components/ui` | localtokenomics | typescript | 25 | 2083 | `localtokenomics:web-src` |
| `web/src/prototype` | localtokenomics | typescript | 10 | 3215 | `localtokenomics:web-src-components`, `localtokenomics:web-src-components-ui`, `localtokenomics:web-src` |
%% generated:module-atlas end %%
