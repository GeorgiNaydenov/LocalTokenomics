---
code: SM-02
entity: CostState
tags:
  - ba/state-machine
maturity: approved
---
# CostState lifecycle

## States

priced
free
unpriced
unavailable

## Transitions

From any state to priced: Gallery sets state at `web/src/prototype/Gallery.tsx:584`
From any state to priced: (module) sets state at `web/src/prototype/data.ts:41`
From any state to priced: (module) sets state at `web/src/prototype/data.ts:54`
From any state to priced: (module) sets state at `web/src/prototype/data.ts:67`
From any state to priced: (module) sets state at `web/src/prototype/data.ts:80`
From any state to priced: (module) sets state at `web/src/prototype/data.ts:93`
From any state to unpriced: (module) sets state at `web/src/prototype/data.ts:106`
From any state to free: (module) sets state at `web/src/prototype/data.ts:119`
From any state to priced: (module) sets state at `web/src/prototype/data.ts:216`
From any state to priced: (module) sets state at `web/src/prototype/data.ts:240`
From any state to priced: (module) sets state at `web/src/prototype/data.ts:264`
From any state to priced: (module) sets state at `web/src/prototype/data.ts:288`
From any state to unavailable: (module) sets state at `web/src/prototype/data.ts:312`
From any state to free: (module) sets state at `web/src/prototype/data.ts:336`
From any state to unpriced: (module) sets state at `web/src/prototype/data.ts:360`
From any state to priced: (module) sets state at `web/src/prototype/data.ts:384`
From any state to unavailable: (module) sets state at `web/src/prototype/data.ts:408`

## Sources

- [[Code of localtokenomics]] @ implemented-by -> web/src/api.ts::CostState | inferred
  > export type CostState = 'priced' | 'free' | 'unpriced' | 'unavailable'
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
  > state: 'unpriced',
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
