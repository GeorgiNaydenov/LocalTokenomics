---
title: Ai usage cost render Specification
aliases: []
tags: [generated, index, reference]
area: application
status: generated
audience: internal
maturity: approved
confidence: confirmed
covers: []
generated: true
---

# Ai usage cost render Specification

The specification entities reverse-engineered from the Ai usage cost render module.

%% generated:spec-links start (do not edit; run brain docs generate) %%
| Kind | Notes | Count |
|---|---|---|
| actor | [[Actors#CLI user]] | 1 |
| glossary-term | API-equivalent cost, [[Domain Models#Bucket]], Group by, Prompt caching savings, [[Domain Models#Report]], Unpriced model | 6 |
| nfr | [[Non-Functional Requirements#NFR-05 PNG export runs without a display]] | 1 |
| open-question | [[Risks and Open Questions#OQ-10 Does the PNG chart need a group by option]], Should the four chart colours keep one meaning across panels?, [[Risks and Open Questions#OQ-09 Where is the dashboard data produced]] | 3 |
| risk | [[Risks and Open Questions#RSK-23 Export writes a chart for a report with no events]], [[Risks and Open Questions#RSK-13 Render layer has no tests of its own]], [[Risks and Open Questions#RSK-14 Silent row truncation in terminal tables]] | 3 |
| rule | [[General Rules#BR-115 Chart colours follow position, not meaning]], [[General Rules#BR-47 Day breakdown is listed oldest first]], [[General Rules#BR-52 Empty project panel is left blank]], [[General Rules#BR-53 Export accepts only json and png]], [[General Rules#BR-51 PNG charts are limited to the top buckets]], [[General Rules#BR-46 Terminal table shows at most 30 rows]], [[General Rules#BR-48 Unknown grouping falls back to model]], [[General Rules#BR-50 Unpriced models are shown but not totalled]], [[General Rules#BR-49 Warnings are summarised unless verbose]] | 9 |
| use-case | [[UC-16 Export a usage and cost chart as a PNG image]], [[UC-15 Print a usage and cost summary in the terminal]] | 2 |

These notes are drafts until the chunk ch-localtokenomics-src-ai-usage-cost-render is approved. They are written to the spec graph and cite the code they describe. A name without a link has no note yet; brain docs generate links it once the note is written.
%% generated:spec-links end %%
