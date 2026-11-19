---
title: Usage cost terms
aliases: []
tags: [diagram, glossary-map, mermaid]
area: diagrams
status: active
audience: internal
maturity: approved
confidence: inferred
covers: [src/ai_usage_cost/*]
verified-against: 1445ea834ab7
sources: [docs/brain/architecture/diagrams/usage-cost-terms.mmd]
chunk: ch-localtokenomics-src-ai-usage-cost
authored: true
node_citations:
  usage-cost-terms:
    source: ['src/ai_usage_cost/sources/base.py:18-21']
    client: ['src/ai_usage_cost/models.py:51']
    session: ['src/ai_usage_cost/models.py:55']
    request: ['src/ai_usage_cost/models.py:49-72']
    tokens: ['src/ai_usage_cost/models.py:12-33']
    tier: ['src/ai_usage_cost/models.py:59']
    sidechain: ['src/ai_usage_cost/models.py:58']
    rate: ['src/ai_usage_cost/pricing.py:126-129']
    state: ['src/ai_usage_cost/models.py:8']
    cost: ['src/ai_usage_cost/models.py:75-98']
    span: ['src/ai_usage_cost/trace.py:55-71']
    outcome: ['src/ai_usage_cost/trace.py:141-151']
    bucket: ['src/ai_usage_cost/models.py:123-130']
    warning: ['src/ai_usage_cost/aggregate.py:115-128']
    severity: ['src/ai_usage_cost/aggregate.py:83-90']
approved-by: human
approved-at: '2026-11-19T06:39:06+00:00'
---

# Usage cost terms

This view places the words the tool uses next to each other and names how they relate. It helps a new reader, and anyone writing a report or a story, use the same words the code uses. The terms are defined one by one in the glossary of this chunk.

## What the diagram shows

- A request records the source it came from, the client, the session it belongs to, its token counts and its service tier, which is standard unless the log says otherwise. `src/ai_usage_cost/models.py:49-59`
- A sidechain is a request made by a subagent, kept as a flag on the request so reports can leave it out. `src/ai_usage_cost/models.py:58` `src/ai_usage_cost/cli.py:79` `src/ai_usage_cost/pipeline.py:277`
- A source is one supported AI coding tool reader, and it maps the client names it writes for. `src/ai_usage_cost/sources/base.py:18-21`
- Token usage has six counted fields and derives the cache write, input and overall totals. `src/ai_usage_cost/models.py:12-33`
- A rate row matches a model id prefix for one provider. `src/ai_usage_cost/pricing.py:126-129`
- Every priced request ends in one of four cost states, and only some states carry a cost breakdown. `src/ai_usage_cost/models.py:8` `src/ai_usage_cost/models.py:117-120`
- A span is one step of a session trace, and an outcome is the rating a person gives a session. `src/ai_usage_cost/trace.py:55-71` `src/ai_usage_cost/trace.py:141-151`
- A bucket sums the tokens and the cost breakdown of the requests that share one key. `src/ai_usage_cost/models.py:123-130`
- A warning group gathers warnings of one kind and carries the worst severity among them: info, caution or critical. `src/ai_usage_cost/aggregate.py:83-90` `src/ai_usage_cost/aggregate.py:115-128`

## Capability and related functionality

- The glossary entries, with one cited definition each, are in [[Ai usage cost Specification]].
- The same terms as stored records are in [[Usage cost conceptual model]] and as in memory types in [[Usage cost types]].
- The cost state is drawn as a lifecycle in [[Cost state of a request]].

## Usage cost terms

%% generated:diagram-usage-cost-terms start (do not edit; run brain docs generate) %%
%% generated:diagram-usage-cost-terms end %%

> [!example]- Code references
> | Code | What it shows |
> |---|---|
> | `src/ai_usage_cost/models.py:8-130` | Request, tokens, cost state, cost breakdown, bucket |
> | `src/ai_usage_cost/pricing.py:126-145` | Rate row |
> | `src/ai_usage_cost/trace.py:55-151` | Span and outcome |
> | `src/ai_usage_cost/aggregate.py:83-128` | Warning severity and group |
