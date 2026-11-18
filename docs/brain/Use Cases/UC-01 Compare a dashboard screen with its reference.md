---
title: UC-01 Compare a dashboard screen with its reference
aliases: [UC-01, Compare a dashboard screen with its reference]
tags: [generated, spec, use-case]
area: business
status: generated
audience: internal
maturity: approved
confidence: confirmed
covers: [web/prototype.html, web/src/prototype/main.tsx, web/src/prototype/Prototype.tsx,
  web/src/prototype/Screens.tsx]
generated: true
use-cases: [UC-01]
subdomain: ''
---

# UC-01 Compare a dashboard screen with its reference

> [!info] What this is
> A use case of the subdomain, written from the code. Every step cites the line that does it, so a reader can check the claim in one click.

> [!tip] How to use it
> Read the main flow first, then the alternative flows. The rules, terms and diagrams at the end are the ones this use case relies on.

- **Actors:** [[Actors#Dashboard developer|Dashboard developer]]
- **Maturity:** approved

## Description

A [[Actors#Dashboard developer|Dashboard developer]] opens the [[Prototype]] page to see how one of the four screens, or a design system part, should look against [[Mock data]], then reads the matching [[Reference screen]] before changing the shipped screen.

## Preconditions

The Vite development server is running.

## Main flow

1. 1. The developer opens /prototype.html, which loads the prototype entry script. [[web/prototype.html|web/prototype.html:25]]
2. 2. The entry script mounts the Prototype shell. [[web/src/prototype/main.tsx|web/src/prototype/main.tsx:9]]
3. 3. The developer picks a tab: Overview, Sessions, Sources, Models and pricing, or Design system. [[web/src/prototype/Prototype.tsx|web/src/prototype/Prototype.tsx:16]]
4. 4. The shell renders the Design system page for the gallery tab and the Screens component for every other tab. [[web/src/prototype/Prototype.tsx|web/src/prototype/Prototype.tsx:98-107]]
5. 5. Screens renders the chosen reference screen from mock data. [[web/src/prototype/Screens.tsx|web/src/prototype/Screens.tsx:360-368]]
6. 6. In Sessions, the developer opens a row to see the session drawer. [[web/src/prototype/Screens.tsx|web/src/prototype/Screens.tsx:375]]

## Alternative flows

4a. For the gallery tab the Filters button is hidden. [[web/src/prototype/Prototype.tsx|web/src/prototype/Prototype.tsx:70-79]]

## Postconditions

Nothing is stored; the developer knows the target layout.

## Acceptance criteria

No test covers the prototype. Criteria come from the code: the page offers five tabs, the Rescan logs button reads no logs, and filters do not change the screens.

## Business rules

- [[General Rules#BR-02 Prototype filters do not filter the screens|BR-02 Prototype filters do not filter the screens]]
- [[General Rules#BR-04 Prototype splits session cost across token buckets by fixed weights|BR-04 Prototype splits session cost across token buckets by fixed weights]]
- [[General Rules#BR-05 Prototype rescan is staged|BR-05 Prototype rescan is staged]]

## Code

- [[web/prototype.html]]
- [[web/src/prototype/main.tsx]]
- [[web/src/prototype/Prototype.tsx]]
- [[web/src/prototype/Screens.tsx]]
