---
title: Web ui UI components Specification
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

# Web ui UI components Specification

The specification entities reverse-engineered from the Web ui UI components module.

%% generated:spec-links start (do not edit; run brain docs generate) %%
| Kind | Notes | Count |
|---|---|---|
| glossary-term | Chart config, Slot attribute, UI primitive | 3 |
| nfr | [[Non-Functional Requirements#NFR-04 Chart colours follow the light and dark theme]] | 1 |
| open-question | [[Risks and Open Questions#OQ-22 Are the chart legend parts still needed]], [[Risks and Open Questions#OQ-21 Should the toast host ship in the main app]], [[Risks and Open Questions#OQ-06 Which primitives are unused]] | 3 |
| risk | [[Risks and Open Questions#RSK-34 A chart legend label is empty for a series with no config entry]], [[Risks and Open Questions#RSK-33 A chart part outside its container throws with no error boundary above it]], [[Risks and Open Questions#RSK-32 Chart style text is built from config keys without escaping]], [[Risks and Open Questions#RSK-10 Primitives have no tests of their own]] | 4 |
| rule | [[General Rules#BR-34 Caller class names override primitive defaults]], [[General Rules#BR-36 Chart parts require a chart container]], [[General Rules#BR-37 Sheet opens from the right by default]], [[General Rules#BR-35 Toggle group settings win over item settings]], [[General Rules#BR-38 Tooltip provider default delay is zero]], [[General Rules#BR-14 useChart refuses when !context]] | 6 |

These notes are drafts until the chunk ch-localtokenomics-web-src-components-ui is approved. They are written to the spec graph and cite the code they describe. A name without a link has no note yet; brain docs generate links it once the note is written.
%% generated:spec-links end %%
