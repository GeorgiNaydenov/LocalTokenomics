---
code: UC-28
primary_actor: User of Web prototype
subdomain: Web prototype area
no_models_reason: No model of the specification is declared in the code this use case cites or in a file that code imports directly.
rules:
  - A missing value is shown as unavailable, never as zero
  - An estimated price is marked next to the cost state
  - Caller class names override primitive defaults
  - Drawer trace blocks show the same sample data for every traced session
  - Prototype figures are invented
  - Prototype filters do not filter the screens
  - Prototype rescan is staged
  - Prototype session table shows at most 120 rows
  - Prototype splits session cost across token buckets by fixed weights
  - Screens stay mounted across the four screen tabs but not across the gallery
  - Sheet opens from the right by default
  - Sub cent money keeps four decimals
  - The daily chart names at most twelve series
  - The date range cannot cross itself
  - Tooltip provider default delay is zero
tags:
  - ba/use-case
maturity: draft
---
# Sort the session list and open one session in the prototype

## Description

A developer who ports the Sessions screen sorts the sample session table, opens one session and reads the drawer, to see the target layout and the states the screen has to cover.

## Preconditions

- The prototype page is open on the Sessions tab.

## Postconditions

- Nothing is stored; the chosen session is only kept as component state until the drawer is closed.

## Main flow

1. 1. The developer picks the Sessions tab. `web/src/prototype/Prototype.tsx:54`
2. 2. The screen sorts a copy of all sample sessions, by cost high to low at first. `web/src/prototype/SessionsScreen.tsx:83`
3. 3. A header press sorts by that column, and a second press flips the direction. `web/src/prototype/SessionsScreen.tsx:99`
4. 4. The first rows up to the row limit are shown. `web/src/prototype/SessionsScreen.tsx:96`
5. 5. A click on a row calls the open callback with the session. `web/src/prototype/SessionsScreen.tsx:170`
6. 6. The Screens component keeps it as the active session and the drawer opens. `web/src/prototype/Screens.tsx:363`
7. 7. The drawer shows the cost, then token buckets or an empty state, then trace blocks or an explanation. `web/src/prototype/Screens.tsx:94`

## Alternative flows

- 2a. On a phone width the table is replaced by cards. `web/src/prototype/SessionsScreen.tsx:127` 7a. A session without token counts shows an empty state in place of the buckets. `web/src/prototype/Screens.tsx:166` 7b. A session that is not traced shows a text that it was recorded before span capture. `web/src/prototype/Screens.tsx:219`

## Special requirements

The row limit is 120 sessions. The drawer reads fixed sample arrays for its trace blocks.

## Acceptance criteria

- No test covers the prototype. From the code: the table is sorted by cost high to low at first, at most the row limit of sessions are shown, a row click opens the drawer, and the drawer closes through its close control.
- 2a: On a phone width the table is replaced by cards. `web/src/prototype/SessionsScreen.tsx:127` 7a. A session without token counts shows an empty state in place of the buckets. `web/src/prototype/Screens.tsx:166` 7b. A session that is not traced shows a text that it was recorded before span capture. `web/src/prototype/Screens.tsx:219`

## Glossary

- [[Prototype]]
- [[Session]]
- Span

## Sources

- [[Code of localtokenomics]] @ implemented-by -> web/src/prototype/SessionsScreen.tsx::SessionsScreen | inferred
  > export function SessionsScreen({ onOpen }: { onOpen: (session: PrototypeSession) => void }) {
- [[Code of localtokenomics]] @ implemented-by -> web/src/prototype/Screens.tsx::SessionDrawer | inferred
  > function SessionDrawer({
