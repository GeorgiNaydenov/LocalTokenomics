---
code: SM-01
entity: RateState
tags:
  - ba/state-machine
maturity: approved
---
# RateState lifecycle

## States

free
priced
unused

## Transitions

From any state to priced: Gallery sets state at `web/src/prototype/Gallery.tsx:584`
From any state to priced: (module) sets state at `web/src/prototype/data.ts:41`
From any state to priced: (module) sets state at `web/src/prototype/data.ts:54`
From any state to priced: (module) sets state at `web/src/prototype/data.ts:67`
From any state to priced: (module) sets state at `web/src/prototype/data.ts:80`
From any state to priced: (module) sets state at `web/src/prototype/data.ts:93`
From any state to free: (module) sets state at `web/src/prototype/data.ts:119`
From any state to priced: (module) sets state at `web/src/prototype/data.ts:216`
From any state to priced: (module) sets state at `web/src/prototype/data.ts:240`
From any state to priced: (module) sets state at `web/src/prototype/data.ts:264`
From any state to priced: (module) sets state at `web/src/prototype/data.ts:288`
From any state to free: (module) sets state at `web/src/prototype/data.ts:336`
From any state to priced: (module) sets state at `web/src/prototype/data.ts:384`

## Sources

- [[Code of localtokenomics]] @ implemented-by -> web/src/Pricing.tsx::RateState | inferred
  > type RateState = 'free' | 'priced' | 'unused'
- [[Code of localtokenomics]] @ implemented-by -> web/src/prototype/Gallery.tsx::Gallery | inferred
  > session={{ id: '9f3c1a44', state: 'priced', model: 'Claude Opus 5', extraModels: 1, client: 'Claude Code', project: 'ai-usage-cost', started
- [[Code of localtokenomics]] @ implemented-by -> web/src/prototype/data.ts | inferred
  > state: 'priced',
- [[Code of localtokenomics]] @ implemented-by -> web/src/prototype/data.ts | inferred
  > state: 'priced',
- [[Code of localtokenomics]] @ implemented-by -> web/src/prototype/data.ts | inferred
  > state: 'priced',
- [[Code of localtokenomics]] @ implemented-by -> web/src/prototype/data.ts | inferred
  > state: 'priced',
- [[Code of localtokenomics]] @ implemented-by -> web/src/prototype/data.ts | inferred
  > state: 'priced',
- [[Code of localtokenomics]] @ implemented-by -> web/src/prototype/data.ts | inferred
  > state: 'free',
- [[Code of localtokenomics]] @ implemented-by -> web/src/prototype/data.ts | inferred
  > state: 'priced',
- [[Code of localtokenomics]] @ implemented-by -> web/src/prototype/data.ts | inferred
  > state: 'priced',
- [[Code of localtokenomics]] @ implemented-by -> web/src/prototype/data.ts | inferred
  > state: 'priced',
- [[Code of localtokenomics]] @ implemented-by -> web/src/prototype/data.ts | inferred
  > state: 'priced',
- [[Code of localtokenomics]] @ implemented-by -> web/src/prototype/data.ts | inferred
  > state: 'free',
