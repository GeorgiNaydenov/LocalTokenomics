---
title: Requirement Catalogue
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

# Requirement Catalogue

Measures and thresholds the repository already states or enforces, each with its source and what checks it.

%% generated:requirements start (do not edit; run brain docs generate) %%
### Quality gates

| ID | Requirement | Measure | Threshold | Source | Checked by |
|---|---|---|---|---|---|
| QUAL-1 | Supported Python versions | version range | >=3.11 | [[pyproject.toml]] `pyproject.toml:6` | installer |
| QUAL-2 | Strict type checking | compiler mode | strict | [[web/tsconfig.json]] `web/tsconfig.json:19` | tsc |

### Time and performance limits

| ID | Requirement | Measure | Threshold | Source | Checked by |
|---|---|---|---|---|---|
| PERF-1 | Fetch timeout s | constant in code | 30 | [[scripts/rates_diff.py]] `scripts/rates_diff.py:33` | none |
| PERF-2 | Low cache hit ratio | constant in code | 0.2 | [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:36` | none |

### Capacity and size limits

| ID | Requirement | Measure | Threshold | Source | Checked by |
|---|---|---|---|---|---|
| CAP-1 | Max content bytes | constant in code | 65_536 | [[src/ai_usage_cost/privacy.py]] `src/ai_usage_cost/privacy.py:11` | none |
| CAP-2 | Long context capacity | constant in code | 1_000_000 | [[src/ai_usage_cost/sources/claude_code.py]] `src/ai_usage_cost/sources/claude_code.py:25` | none |
| CAP-3 | Max error chars | constant in code | 500 | [[src/ai_usage_cost/sources/claude_code.py]] `src/ai_usage_cost/sources/claude_code.py:26` | none |
| CAP-4 | Reconcile min tokens | constant in code | 1000 | [[src/ai_usage_cost/sources/codex.py]] `src/ai_usage_cost/sources/codex.py:22` | none |
| CAP-5 | Amplification limit | constant in code | 20.0 | [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:31` | none |
| CAP-6 | Repeated tool limit | constant in code | 3 | [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:32` | none |
| CAP-7 | Turn error limit | constant in code | 3 | [[src/ai_usage_cost/trace.py]] `src/ai_usage_cost/trace.py:33` | none |
| CAP-8 | Reveal batch | constant in code | 60 | [[web/src/ContextTab.tsx]] `web/src/ContextTab.tsx:14` | none |
| CAP-9 | Max contributors | constant in code | 6 | [[web/src/ContextTab.tsx]] `web/src/ContextTab.tsx:15` | none |
| CAP-10 | Reveal batch | constant in code | 40 | [[web/src/EconomicsTab.tsx]] `web/src/EconomicsTab.tsx:43` | none |
| CAP-11 | Reveal batch | constant in code | 20 | [[web/src/Pricing.tsx]] `web/src/Pricing.tsx:40` | none |
| CAP-12 | Resize step | constant in code | 24 | [[web/src/SessionWorkspace.tsx]] `web/src/SessionWorkspace.tsx:396` | none |
| CAP-13 | Shown limit | constant in code | 120 | [[web/src/Sessions.tsx]] `web/src/Sessions.tsx:48` | none |
| CAP-14 | Row batch | constant in code | 400 | [[web/src/TraceTab.tsx]] `web/src/TraceTab.tsx:25` | none |
| CAP-15 | Min width | constant in code | 360 | [[web/src/components/workspace-panel.ts]] `web/src/components/workspace-panel.ts:6` | none |
| CAP-16 | Max width | constant in code | 900 | [[web/src/components/workspace-panel.ts]] `web/src/components/workspace-panel.ts:8` | none |
| CAP-17 | Reveal batch | constant in code | 4 | [[web/src/prototype/PricingScreen.tsx]] `web/src/prototype/PricingScreen.tsx:20` | none |

### Security and abuse limits

| ID | Requirement | Measure | Threshold | Source | Checked by |
|---|---|---|---|---|---|
| SEC-1 | Session limit | constant in code | 120 | [[web/src/prototype/data.ts]] `web/src/prototype/data.ts:744` | none |

22 requirements were read from CI files, configuration and constants; 20 have no test that mentions them.
%% generated:requirements end %%
