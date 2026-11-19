---
title: Alert comparison windows
aliases: []
tags: [diagram, gantt, mermaid]
area: diagrams
status: active
audience: internal
maturity: approved
confidence: inferred
covers: [src/ai_usage_cost/*]
verified-against: 1445ea834ab7
sources: [docs/brain/architecture/diagrams/alert-windows.mmd]
chunk: ch-localtokenomics-src-ai-usage-cost
authored: true
approved-by: human
approved-at: '2026-11-19T06:39:06+00:00'
---

# Alert comparison windows

This view puts the two periods the spend alert compares on a calendar. It makes clear that the current period always includes today and that the earlier period has the same length and ends the day before. Anyone setting a rise limit can see exactly which days are being compared.

## What the diagram shows

- The dates are an example: a run on 10 August 2026 with a rise limit and a three day window. The code computes the same shape for any run date and length. `src/ai_usage_cost/cli.py:314` `src/ai_usage_cost/cli.py:329-330`
- The current window ends today and starts the window length minus one day before, so today is one of its days. `src/ai_usage_cost/cli.py:329-330`
- Only with the rise limit, the previous window starts the window length before the current start and ends the day before it. `src/ai_usage_cost/cli.py:333-337`
- Both ends of a window are included, because the report keeps every request whose local day is on or after the start and on or before the end. `src/ai_usage_cost/pipeline.py:269-270`
- The day of a request is its local calendar day on this machine, whatever offset the log wrote. `src/ai_usage_cost/models.py:137-146`
- With the total limit only the current window is reported and compared. `src/ai_usage_cost/cli.py:261-264`

## Capability and related functionality

- Part of the use case be alerted when spend rises; the whole run is drawn in [[Spend alert run]].
- The local day rule is shared with every day filter of the dashboard, described in [[Ai usage cost Overview]].
- No schedule is in the code: the alert runs only when the person or their own scheduler starts it (`src/ai_usage_cost/cli.py:298-299`).

## Alert comparison windows

%% generated:diagram-alert-windows start (do not edit; run brain docs generate) %%
%% generated:diagram-alert-windows end %%

> [!example]- Code references
> | Code | What it shows |
> |---|---|
> | `src/ai_usage_cost/cli.py:329-337` | The two windows |
> | `src/ai_usage_cost/pipeline.py:248-279` | The inclusive day filter |
> | `src/ai_usage_cost/models.py:137-146` | The local day of a request |
