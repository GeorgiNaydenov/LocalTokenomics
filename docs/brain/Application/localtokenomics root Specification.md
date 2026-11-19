---
title: localtokenomics root Specification
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

# localtokenomics root Specification

The specification entities reverse-engineered from the localtokenomics root module.

%% generated:spec-links start (do not edit; run brain docs generate) %%
| Kind | Notes | Count |
|---|---|---|
| actor | [[Actors#GitHub workflow runner]], [[Actors#Maintainer]], [[Actors#User of localtokenomics root]] | 3 |
| glossary-term | API-equivalent cost, Dashboard bundle, Dev proxy | 3 |
| nfr | [[Non-Functional Requirements#NFR-01 Python version support]] | 1 |
| open-question | [[Risks and Open Questions#OQ-02 Is Node 20 tested for the dashboard build]], [[Risks and Open Questions#OQ-16 Should local checks and the workflow lint the same folders]], [[Risks and Open Questions#OQ-15 Should the README list content_retention_days]] | 3 |
| risk | [[Risks and Open Questions#RSK-21 A mistyped settings file silently drops the project exclusions]], [[Risks and Open Questions#RSK-22 Bandit is configured but no workflow or hook runs it]], [[Risks and Open Questions#RSK-05 Bandit security scanning skips the web folder, so dashboard]], [[Risks and Open Questions#RSK-04 Mypy is a manual pre-commit stage, so type errors in the Pyt]] | 4 |
| rule | [[General Rules#BR-09 A production build replaces the committed bundle]], [[General Rules#BR-114 A settings file that cannot be loaded is ignored as a whole]], [[General Rules#BR-08 A type error stops the dashboard build]], [[General Rules#BR-10 Lint skips build output]], [[General Rules#BR-11 Python code must keep a pylint score of 9.0]], [[General Rules#BR-12 Web dependencies are installed from the lockfile]], [[General Rules#BR-13 getJson refuses when !response.ok]], [[General Rules#BR-14 useChart refuses when !context]] | 8 |
| state-machine | [[State Machines#CostState lifecycle]], [[State Machines#MatchKind lifecycle]], [[State Machines#RateState lifecycle]], [[State Machines#RateStatus lifecycle]], [[State Machines#SpanKind lifecycle]], [[State Machines#SpanStatus lifecycle]], [[State Machines#TokenDataKind lifecycle]] | 7 |
| use-case | [[UC-04 Check a change before merge]], [[UC-03 Develop the dashboard against live data]], [[UC-02 Rebuild the dashboard bundle]] | 3 |

These notes are drafts until the chunk ch-localtokenomics-root is approved. They are written to the spec graph and cite the code they describe. A name without a link has no note yet; brain docs generate links it once the note is written.
%% generated:spec-links end %%
