---
title: Application Catalog
aliases: []
tags: [catalog, generated, module]
area: catalogs
status: generated
audience: internal
maturity: approved
confidence: confirmed
covers: []
generated: true
---

# Application Catalog

Every application component with its size, interfaces and entities.

%% generated:app-catalog start (do not edit; run brain docs generate) %%
| Component | Repo | Language | Files | Lines | Routes | Entities | Depends on |
|---|---|---|---|---|---|---|---|
| `(root)` | localtokenomics | python | 2 | 1668 | 0 | 0 | `localtokenomics:src-ai-usage-cost` |
| `src/ai_usage_cost` | localtokenomics | python | 13 | 5069 | 12 | 51 | `localtokenomics:src-ai-usage-cost-sources`, `localtokenomics:src-ai-usage-cost-render` |
| `src/ai_usage_cost/render` | localtokenomics | python | 3 | 187 | 0 | 0 | `localtokenomics:src-ai-usage-cost` |
| `src/ai_usage_cost/sources` | localtokenomics | python | 22 | 4722 | 0 | 0 | `localtokenomics:src-ai-usage-cost` |
| `(root)` | localtokenomics | typescript | 2 | 56 | 0 | 0 | - |
| `web/src` | localtokenomics | typescript | 20 | 7127 | 0 | 0 | `localtokenomics:web-src-components`, `localtokenomics:web-src-components-ui` |
| `web/src/components` | localtokenomics | typescript | 18 | 3024 | 0 | 0 | `localtokenomics:web-src`, `localtokenomics:web-src-components-ui` |
| `web/src/components/ui` | localtokenomics | typescript | 25 | 2083 | 0 | 0 | `localtokenomics:web-src` |
| `web/src/prototype` | localtokenomics | typescript | 10 | 3215 | 0 | 0 | `localtokenomics:web-src-components`, `localtokenomics:web-src-components-ui`, `localtokenomics:web-src` |
%% generated:app-catalog end %%
