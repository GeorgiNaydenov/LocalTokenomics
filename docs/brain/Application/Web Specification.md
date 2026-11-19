---
title: Web Specification
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

# Web Specification

The specification entities reverse-engineered from the Web module.

%% generated:spec-links start (do not edit; run brain docs generate) %%
| Kind | Notes | Count |
|---|---|---|
| actor | [[Actors#Dashboard reader]] | 1 |
| glossary-term | Cost state, Estimated rate, Provenance, Reported cost, Session outcome, Sidechain, Unattributed turn | 7 |
| open-question | Question 11: Should filters stay reachable on a large screen while a session is open?, Question 12: Which warnings should the Flagged figure count?, Question 13: Should failed tabs and span texts offer a retry?, Question 14: Should the heaviest sessions on the overview open their session?, Question 3: Does the DELETE session endpoint remove the, Question 4: Is deleteSession reachable from any screen in | 6 |
| risk | Risk 10: Session rows cannot be opened from the keyboard, Risk 1: The dashboard client can write to the, Risk 2: Most files in this chunk have no, Risk 5: Sessions are identified by session id alone in the table and when opened, Risk 6: One failed report refetch hides the whole dashboard, Risk 7: Outcome saves are not sequenced, Risk 8: A missing span text is recognised by message wording, Risk 9: Rescan can be started twice | 8 |
| rule | [[General Rules#BR-124 A workspace tab loads its data only when first opened]], [[General Rules#BR-25 Automatic rescan every five minutes]], [[General Rules#BR-19 Cache price derivation]], [[General Rules#BR-24 Outcome notes are saved only when changed]], [[General Rules#BR-18 Rate age notice thresholds]], [[General Rules#BR-20 Rate row state]], [[General Rules#BR-17 Reported cost divergence threshold]], [[General Rules#BR-23 Session table row limit]], [[General Rules#BR-125 Span text is fetched once per span]], [[General Rules#BR-21 Sub cent money keeps four decimals]], [[General Rules#BR-22 Unattributed turn is excluded from rankings]], [[General Rules#BR-15 Unavailable is never shown as zero]], [[General Rules#BR-16 Unpriced cost stays out of totals]], [[General Rules#BR-13 getJson refuses when !response.ok]], [[General Rules#BR-14 useChart refuses when !context]] | 15 |
| state-machine | [[State Machines#CostState lifecycle]], [[State Machines#MatchKind lifecycle]], [[State Machines#RateState lifecycle]], [[State Machines#RateStatus lifecycle]], [[State Machines#SpanKind lifecycle]], [[State Machines#SpanStatus lifecycle]], [[State Machines#TokenDataKind lifecycle]], [[State Machines#Workspace tab data]] | 8 |
| use-case | [[UC-08 Check list prices]], [[UC-06 Inspect one session]], [[UC-07 Rate a session outcome]], [[UC-05 Read usage and cost for a period]] | 4 |

These notes are drafts until the chunk ch-localtokenomics-web-src is approved. They are written to the spec graph and cite the code they describe. A name without a link has no note yet; brain docs generate links it once the note is written.
%% generated:spec-links end %%
