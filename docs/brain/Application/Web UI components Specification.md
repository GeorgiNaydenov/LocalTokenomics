---
title: Web UI components Specification
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

# Web UI components Specification

The specification entities reverse-engineered from the Web UI components module.

%% generated:spec-links start (do not edit; run brain docs generate) %%
| Kind | Notes | Count |
|---|---|---|
| actor | [[Actors#Dashboard reader]] | 1 |
| glossary-term | Context occupancy, Cost state, Provenance, Session outcome, Unavailable marker | 5 |
| nfr | [[Non-Functional Requirements#NFR-02 Keyboard and screen reader access to charts and timelines]], [[Non-Functional Requirements#NFR-03 Reduced motion is respected]] | 2 |
| open-question | [[Risks and Open Questions#OQ-24 Is the offline card matched by message text on purpose]], [[Risks and Open Questions#OQ-23 Should a retry on the offline card show progress]], [[Risks and Open Questions#OQ-05 Why the Other series limit is twelve]] | 3 |
| risk | [[Risks and Open Questions#RSK-36 A failed copy of the start command gives no feedback]], [[Risks and Open Questions#RSK-39 A test title says the opposite of what it checks]], [[Risks and Open Questions#RSK-37 Empty warnings and empty charts draw nothing]], [[Risks and Open Questions#RSK-38 Every info box keeps a timer and one global pointer listener]], [[Risks and Open Questions#RSK-35 Hidden columns and shown columns can disagree]], [[Risks and Open Questions#RSK-08 Most shared components have no tests]], [[Risks and Open Questions#RSK-09 Popover timing depends on a polling interval]] | 7 |
| rule | [[General Rules#BR-26 A missing value is shown as unavailable, never as zero]], [[General Rules#BR-27 A rollup shows its least trustworthy cost state and provenance]], [[General Rules#BR-30 A table always keeps at least one column]], [[General Rules#BR-28 An estimated price is marked next to the cost state]], [[General Rules#BR-33 An explanation popover does not take focus back on close]], [[General Rules#BR-29 The daily chart names at most twelve series]], [[General Rules#BR-31 The date range cannot cross itself]], [[General Rules#BR-32 The side panel width is bounded]], [[General Rules#BR-14 useChart refuses when !context]] | 9 |
| state-machine | [[State Machines#Info box open state]], [[State Machines#Warnings list view]] | 2 |
| use-case | [[UC-11 Inspect a chart point]], [[UC-10 Narrow a list and choose its columns]], [[UC-09 Read a figure and see how far to trust it]], [[UC-12 Review a session's spans and context use]] | 4 |

These notes are drafts until the chunk ch-localtokenomics-web-src-components is approved. They are written to the spec graph and cite the code they describe. A name without a link has no note yet; brain docs generate links it once the note is written.
%% generated:spec-links end %%
