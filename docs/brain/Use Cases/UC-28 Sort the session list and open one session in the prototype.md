---
title: UC-28 Sort the session list and open one session in the prototype
aliases: [UC-28, Sort the session list and open one session in the prototype]
tags: [generated, spec, use-case]
area: business
status: generated
audience: internal
maturity: draft
confidence: confirmed
covers: [web/src/prototype/Prototype.tsx, web/src/prototype/SessionsScreen.tsx, web/src/prototype/Screens.tsx]
generated: true
use-cases: [UC-28]
subdomain: ''
---

# UC-28 Sort the session list and open one session in the prototype

> [!info] What this is
> A use case of the subdomain, written from the code. Every step cites the line that does it, so a reader can check the claim in one click.

> [!tip] How to use it
> Read the main flow first, then the alternative flows. The rules, terms and diagrams at the end are the ones this use case relies on.

- **Maturity:** draft

## Description

A developer who ports the Sessions screen sorts the sample session table, opens one session and reads the drawer, to see the target layout and the states the screen has to cover.

## Preconditions

The prototype page is open on the Sessions tab.

## Main flow

1. 1. The developer picks the Sessions tab. [[web/src/prototype/Prototype.tsx|web/src/prototype/Prototype.tsx:54]]
2. 2. The screen sorts a copy of all sample sessions, by cost high to low at first. [[web/src/prototype/SessionsScreen.tsx|web/src/prototype/SessionsScreen.tsx:83]]
3. 3. A header press sorts by that column, and a second press flips the direction. [[web/src/prototype/SessionsScreen.tsx|web/src/prototype/SessionsScreen.tsx:99]]
4. 4. The first rows up to the row limit are shown. [[web/src/prototype/SessionsScreen.tsx|web/src/prototype/SessionsScreen.tsx:96]]
5. 5. A click on a row calls the open callback with the session. [[web/src/prototype/SessionsScreen.tsx|web/src/prototype/SessionsScreen.tsx:170]]
6. 6. The Screens component keeps it as the active session and the drawer opens. [[web/src/prototype/Screens.tsx|web/src/prototype/Screens.tsx:363]]
7. 7. The drawer shows the cost, then token buckets or an empty state, then trace blocks or an explanation. [[web/src/prototype/Screens.tsx|web/src/prototype/Screens.tsx:94]]

## Alternative flows

2a. On a phone width the table is replaced by cards. [[web/src/prototype/SessionsScreen.tsx|web/src/prototype/SessionsScreen.tsx:127]] 7a. A session without token counts shows an empty state in place of the buckets. [[web/src/prototype/Screens.tsx|web/src/prototype/Screens.tsx:166]] 7b. A session that is not traced shows a text that it was recorded before span capture. [[web/src/prototype/Screens.tsx|web/src/prototype/Screens.tsx:219]]

## Postconditions

Nothing is stored; the chosen session is only kept as component state until the drawer is closed.

## Acceptance criteria

No test covers the prototype. From the code: the table is sorted by cost high to low at first, at most the row limit of sessions are shown, a row click opens the drawer, and the drawer closes through its close control.

## Business rules

- [[General Rules#BR-02 Prototype filters do not filter the screens|BR-02 Prototype filters do not filter the screens]]
- [[General Rules#BR-03 Prototype session table shows at most 120 rows|BR-03 Prototype session table shows at most 120 rows]]
- [[General Rules#BR-04 Prototype splits session cost across token buckets by fixed weights|BR-04 Prototype splits session cost across token buckets by fixed weights]]
- [[General Rules#BR-05 Prototype rescan is staged|BR-05 Prototype rescan is staged]]
- [[General Rules#BR-122 Drawer trace blocks show the same sample data for every traced session|BR-122 Drawer trace blocks show the same sample data for every traced session]]
- [[General Rules#BR-123 Screens stay mounted across the four screen tabs but not across the gallery|BR-123 Screens stay mounted across the four screen tabs but not across the gallery]]

## Code

- [[web/src/prototype/Prototype.tsx]]
- [[web/src/prototype/SessionsScreen.tsx]]
- [[web/src/prototype/Screens.tsx]]
