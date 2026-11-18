---
code: UC-01
primary_actor: Dashboard developer
actors:
  - Dashboard developer
tags:
  - ba/use-case
maturity: approved
---
# Compare a dashboard screen with its reference

## Description

A [[Dashboard developer]] opens the [[Prototype]] page to see how one of the four screens, or a design system part, should look against [[Mock data]], then reads the matching [[Reference screen]] before changing the shipped screen.

## Preconditions

The Vite development server is running.

## Postconditions

Nothing is stored; the developer knows the target layout.

## Main flow

1. 1. The developer opens /prototype.html, which loads the prototype entry script. `web/prototype.html:25`
2. 2. The entry script mounts the Prototype shell. `web/src/prototype/main.tsx:9`
3. 3. The developer picks a tab: Overview, Sessions, Sources, Models and pricing, or Design system. `web/src/prototype/Prototype.tsx:16`
4. 4. The shell renders the Design system page for the gallery tab and the Screens component for every other tab. `web/src/prototype/Prototype.tsx:98-107`
5. 5. Screens renders the chosen reference screen from mock data. `web/src/prototype/Screens.tsx:360-368`
6. 6. In Sessions, the developer opens a row to see the session drawer. `web/src/prototype/Screens.tsx:375`

## Alternative flows

4a. For the gallery tab the Filters button is hidden. `web/src/prototype/Prototype.tsx:70-79`

## Special requirements

The prototype is served only by the development server and is not in the production build.

## Acceptance criteria

No test covers the prototype. Criteria come from the code: the page offers five tabs, the Rescan logs button reads no logs, and filters do not change the screens.

## Sources

- [[Code of localtokenomics]] @ implemented-by -> web/src/prototype/Prototype.tsx | inferred
  > export default function Prototype() {
