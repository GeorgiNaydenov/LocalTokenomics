---
title: General Rules
aliases: []
tags: [business, generated, rules, spec]
area: business
status: generated
audience: internal
maturity: draft
confidence: confirmed
covers: [web/src/design-system/MIGRATION.md, web/src/prototype/Prototype.tsx, web/src/prototype/Screens.tsx,
  web/src/prototype/SessionsScreen.tsx, web/src/prototype/data.ts, web/vite.config.ts]
generated: true
anchors: true
---

# General Rules

> [!info] What this is
> Business rules that belong to no single subdomain. Each rule is a heading, so a use case links straight to it, and each names the line of code that enforces it.

## BR-01 The prototype is excluded from the production build

The production build writes to the Python package folder from a single page, and the repository guide states the prototype page is deliberately left out of it.


Source:
- [[web/vite.config.ts|web/vite.config.ts]]: `outDir: '../src/ai_usage_cost/web/dist',`
- [[web/src/design-system/MIGRATION.md|web/src/design-system/MIGRATION.md]]

## BR-02 Prototype filters do not filter the screens

The filter rail in the prototype changes its own state and chips, but the screens are rendered without any filter value, so the figures on screen never change.

- **Used in:** [[UC-01 Compare a dashboard screen with its reference]]

Source:
- [[web/src/prototype/Screens.tsx|web/src/prototype/Screens.tsx]]: `const [filters, setFilters] = useState<FilterState>(INITIAL_FILTERS)`
- [[web/src/prototype/Screens.tsx|web/src/prototype/Screens.tsx]]: `<SessionsScreen onOpen={setActive} />`

## BR-03 Prototype session table shows at most 120 rows

The prototype sorts all sessions and then displays only the first 120.


Source:
- [[web/src/prototype/data.ts|web/src/prototype/data.ts]]: `export const SESSION_LIMIT = 120`
- [[web/src/prototype/SessionsScreen.tsx|web/src/prototype/SessionsScreen.tsx]]: `const shown = sorted.slice(0, SESSION_LIMIT)`

## BR-04 Prototype splits session cost across token buckets by fixed weights

The session drawer apportions a session's cost across the four token buckets with constant weights, not with real rates.

- **Used in:** [[UC-01 Compare a dashboard screen with its reference]]

Source:
- [[web/src/prototype/Screens.tsx|web/src/prototype/Screens.tsx]]: `const BUCKET_WEIGHT: Record<string, number> = {`
- [[web/src/prototype/Screens.tsx|web/src/prototype/Screens.tsx]]: `total > 0 ? (weighted[index] / total) * session.cost! : 0,`

## BR-05 Prototype rescan is staged

The Rescan logs button only shows a scanning state for 900 milliseconds and reads no logs.

- **Used in:** [[UC-01 Compare a dashboard screen with its reference]]

Source:
- [[web/src/prototype/Prototype.tsx|web/src/prototype/Prototype.tsx]]: `setTimeout(() => setScanning(false), 900)`

## BR-06 Prototype figures are invented

The headline totals are literal numbers and the session list is generated from a few seed sessions.


Source:
- [[web/src/prototype/data.ts|web/src/prototype/data.ts]]: `cost: 3_431.96,`
- [[web/src/prototype/data.ts|web/src/prototype/data.ts]]: `for (let index = 0; generated.length + seeded.length < 184; index++) {`

## BR-07 Do not import from the prototype folder

The migration guide tells porters to copy the composition of a prototype screen and never to import from the prototype folder.


Source:
- [[web/src/design-system/MIGRATION.md|web/src/design-system/MIGRATION.md]]
