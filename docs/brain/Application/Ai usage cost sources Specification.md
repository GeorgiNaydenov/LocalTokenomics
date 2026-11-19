---
title: Ai usage cost sources Specification
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

# Ai usage cost sources Specification

The specification entities reverse-engineered from the Ai usage cost sources module.

%% generated:spec-links start (do not edit; run brain docs generate) %%
| Kind | Notes | Count |
|---|---|---|
| data-store | [[Systems and Data Stores#Data of Ai usage cost sources]] | 1 |
| glossary-term | [[Domain Models#Capabilities]], Experimental reader, Reader, Resume hook, Root, [[Domain Models#Span]], Token data, Usage event | 8 |
| model | [[Domain Models#Source]], [[Domain Models#Spec]] | 2 |
| open-question | Experimental readers verified?, [[Risks and Open Questions#OQ-18 Is the scan helper in the shared module still needed]], [[Risks and Open Questions#OQ-08 Muse Code cache write tokens]] | 3 |
| risk | [[Risks and Open Questions#RSK-24 A missing timestamp is stamped with the scan time]], [[Risks and Open Questions#RSK-11 Cline family token semantics unverified]], [[Risks and Open Questions#RSK-12 Copilot CLI and Muse Code unchecked against real logs]], [[Risks and Open Questions#RSK-25 One broken reader module stops the registry]], [[Risks and Open Questions#RSK-26 Two readers import a private name from the Cline module]] | 5 |
| rule | [[General Rules#BR-40 A reader is found by its SOURCE value]], [[General Rules#BR-45 Experimental readers carry a flag]], [[General Rules#BR-44 Muse Code control folders are skipped]], [[General Rules#BR-39 Readers only read]], [[General Rules#BR-43 Repeated Codex token totals are not counted twice]], [[General Rules#BR-42 Synthetic Claude Code records are not usage]], [[General Rules#BR-41 Unparsable lines are skipped and counted]] | 7 |
| use-case | [[UC-13 Discover AI tool usage from local files]], [[UC-14 Read a tool's SQLite store without a token count]] | 2 |

These notes are drafts until the chunk ch-localtokenomics-src-ai-usage-cost-sources is approved. They are written to the spec graph and cite the code they describe. A name without a link has no note yet; brain docs generate links it once the note is written.
%% generated:spec-links end %%
