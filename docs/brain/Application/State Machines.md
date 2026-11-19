---
title: State Machines
aliases: []
tags: [application, generated, spec, state-machine]
area: application
status: generated
audience: internal
maturity: draft
confidence: confirmed
covers: [src/ai_usage_cost/models.py, src/ai_usage_cost/pricing.py, web/src/SessionWorkspace.tsx,
  web/src/TraceTab.tsx, web/src/components/metric-info.tsx, web/src/components/states.tsx,
  web/src/prototype/Gallery.tsx, web/src/prototype/data.ts]
generated: true
anchors: true
---

# State Machines

> [!info] What this is
> The values that move through states, the states they can take and the code that moves them.

## RateState lifecycle

- `free`
- `priced`
- `unused`

From any state to priced: Gallery sets state at [[web/src/prototype/Gallery.tsx|web/src/prototype/Gallery.tsx:584]]
From any state to priced: (module) sets state at [[web/src/prototype/data.ts|web/src/prototype/data.ts:41]]
From any state to priced: (module) sets state at [[web/src/prototype/data.ts|web/src/prototype/data.ts:54]]
From any state to priced: (module) sets state at [[web/src/prototype/data.ts|web/src/prototype/data.ts:67]]
From any state to priced: (module) sets state at [[web/src/prototype/data.ts|web/src/prototype/data.ts:80]]
From any state to priced: (module) sets state at [[web/src/prototype/data.ts|web/src/prototype/data.ts:93]]
From any state to free: (module) sets state at [[web/src/prototype/data.ts|web/src/prototype/data.ts:119]]
From any state to priced: (module) sets state at [[web/src/prototype/data.ts|web/src/prototype/data.ts:216]]
From any state to priced: (module) sets state at [[web/src/prototype/data.ts|web/src/prototype/data.ts:240]]
From any state to priced: (module) sets state at [[web/src/prototype/data.ts|web/src/prototype/data.ts:264]]
From any state to priced: (module) sets state at [[web/src/prototype/data.ts|web/src/prototype/data.ts:288]]
From any state to free: (module) sets state at [[web/src/prototype/data.ts|web/src/prototype/data.ts:336]]
From any state to priced: (module) sets state at [[web/src/prototype/data.ts|web/src/prototype/data.ts:384]]

Source:
- `RateState`: `type RateState = 'free' | 'priced' | 'unused'`
- `Gallery`: `session={{ id: '9f3c1a44', state: 'priced', model: 'Claude Opus 5', extraModels: 1, client: 'Claude Code', project: 'ai-usage-cost', started`
- [[web/src/prototype/data.ts|web/src/prototype/data.ts]]: `state: 'priced',`
- [[web/src/prototype/data.ts|web/src/prototype/data.ts]]: `state: 'free',`

## CostState lifecycle

- `priced`
- `free`
- `unpriced`
- `unavailable`

From any state to priced: Gallery sets state at [[web/src/prototype/Gallery.tsx|web/src/prototype/Gallery.tsx:584]]
From any state to priced: (module) sets state at [[web/src/prototype/data.ts|web/src/prototype/data.ts:41]]
From any state to priced: (module) sets state at [[web/src/prototype/data.ts|web/src/prototype/data.ts:54]]
From any state to priced: (module) sets state at [[web/src/prototype/data.ts|web/src/prototype/data.ts:67]]
From any state to priced: (module) sets state at [[web/src/prototype/data.ts|web/src/prototype/data.ts:80]]
From any state to priced: (module) sets state at [[web/src/prototype/data.ts|web/src/prototype/data.ts:93]]
From any state to unpriced: (module) sets state at [[web/src/prototype/data.ts|web/src/prototype/data.ts:106]]
From any state to free: (module) sets state at [[web/src/prototype/data.ts|web/src/prototype/data.ts:119]]
From any state to priced: (module) sets state at [[web/src/prototype/data.ts|web/src/prototype/data.ts:216]]
From any state to priced: (module) sets state at [[web/src/prototype/data.ts|web/src/prototype/data.ts:240]]
From any state to priced: (module) sets state at [[web/src/prototype/data.ts|web/src/prototype/data.ts:264]]
From any state to priced: (module) sets state at [[web/src/prototype/data.ts|web/src/prototype/data.ts:288]]
From any state to unavailable: (module) sets state at [[web/src/prototype/data.ts|web/src/prototype/data.ts:312]]
From any state to free: (module) sets state at [[web/src/prototype/data.ts|web/src/prototype/data.ts:336]]
From any state to unpriced: (module) sets state at [[web/src/prototype/data.ts|web/src/prototype/data.ts:360]]
From any state to priced: (module) sets state at [[web/src/prototype/data.ts|web/src/prototype/data.ts:384]]
From any state to unavailable: (module) sets state at [[web/src/prototype/data.ts|web/src/prototype/data.ts:408]]

Source:
- `CostState`: `export type CostState = 'priced' | 'free' | 'unpriced' | 'unavailable'`
- `Gallery`: `session={{ id: '9f3c1a44', state: 'priced', model: 'Claude Opus 5', extraModels: 1, client: 'Claude Code', project: 'ai-usage-cost', started`
- [[web/src/prototype/data.ts|web/src/prototype/data.ts]]: `state: 'priced',`
- [[web/src/prototype/data.ts|web/src/prototype/data.ts]]: `state: 'unpriced',`
- [[web/src/prototype/data.ts|web/src/prototype/data.ts]]: `state: 'free',`

## SpanKind lifecycle

- `turn`
- `user`
- `assistant`
- `reasoning`
- `model_call`
- `tool_call`
- `tool_result`
- `retrieval`
- `compaction`
- `error`
- `subagent`

From any state to error: useLazyResource sets status at [[web/src/SessionWorkspace.tsx|web/src/SessionWorkspace.tsx:105]]
From any state to error: toggleContent sets status at [[web/src/TraceTab.tsx|web/src/TraceTab.tsx:796]]
From any state to error: (module) sets status at [[web/src/prototype/data.ts|web/src/prototype/data.ts:809]]

Source:
- `SpanKind`: `export type SpanKind =`
- `useLazyResource`: `setSettled({ load, result: { status: 'error', message: messageOf(cause) } })`
- `toggleContent`: `const next: ContentState = isMissing(cause) ? { status: 'off' } : { status: 'error', message: messageOf(cause) }`
- [[web/src/prototype/data.ts|web/src/prototype/data.ts]]: `{ spanId: 's8', kind: 'error', name: 'File changed on disk, retrying', status: 'error', depth: 2, durationMs: null, tokens: null },`

## SpanStatus lifecycle

- `ok`
- `error`
- `interrupted`
- `aborted`
- `running`
- `unknown`

From any state to error: useLazyResource sets status at [[web/src/SessionWorkspace.tsx|web/src/SessionWorkspace.tsx:105]]
From any state to error: toggleContent sets status at [[web/src/TraceTab.tsx|web/src/TraceTab.tsx:796]]
From any state to ok: (module) sets status at [[web/src/prototype/data.ts|web/src/prototype/data.ts:802]]
From any state to ok: (module) sets status at [[web/src/prototype/data.ts|web/src/prototype/data.ts:803]]
From any state to ok: (module) sets status at [[web/src/prototype/data.ts|web/src/prototype/data.ts:804]]
From any state to ok: (module) sets status at [[web/src/prototype/data.ts|web/src/prototype/data.ts:805]]
From any state to ok: (module) sets status at [[web/src/prototype/data.ts|web/src/prototype/data.ts:806]]
From any state to ok: (module) sets status at [[web/src/prototype/data.ts|web/src/prototype/data.ts:807]]
From any state to interrupted: (module) sets status at [[web/src/prototype/data.ts|web/src/prototype/data.ts:808]]
From any state to error: (module) sets status at [[web/src/prototype/data.ts|web/src/prototype/data.ts:809]]
From any state to ok: (module) sets status at [[web/src/prototype/data.ts|web/src/prototype/data.ts:810]]
From any state to ok: (module) sets status at [[web/src/prototype/data.ts|web/src/prototype/data.ts:811]]
From any state to ok: (module) sets status at [[web/src/prototype/data.ts|web/src/prototype/data.ts:812]]

Source:
- `SpanStatus`: `export type SpanStatus = 'ok' | 'error' | 'interrupted' | 'aborted' | 'running' | 'unknown'`
- `useLazyResource`: `setSettled({ load, result: { status: 'error', message: messageOf(cause) } })`
- `toggleContent`: `const next: ContentState = isMissing(cause) ? { status: 'off' } : { status: 'error', message: messageOf(cause) }`
- [[web/src/prototype/data.ts|web/src/prototype/data.ts]]: `{ spanId: 's1', kind: 'turn', name: 'Turn 14 — rebuild the design system', status: 'ok', depth: 0, durationMs: 184_000, tokens: 412_004 },`
- [[web/src/prototype/data.ts|web/src/prototype/data.ts]]: `{ spanId: 's2', kind: 'user', name: 'User message', status: 'ok', depth: 1, durationMs: null, tokens: 1_204 },`
- [[web/src/prototype/data.ts|web/src/prototype/data.ts]]: `{ spanId: 's3', kind: 'model_call', name: 'claude-opus-5', status: 'ok', depth: 1, durationMs: 21_400, tokens: 188_320 },`
- [[web/src/prototype/data.ts|web/src/prototype/data.ts]]: `{ spanId: 's4', kind: 'reasoning', name: 'Reasoning', status: 'ok', depth: 2, durationMs: 8_200, tokens: 42_110 },`
- [[web/src/prototype/data.ts|web/src/prototype/data.ts]]: `{ spanId: 's5', kind: 'tool_call', name: 'Read web/src/Overview.tsx', status: 'ok', depth: 2, durationMs: 140, tokens: null },`
- [[web/src/prototype/data.ts|web/src/prototype/data.ts]]: `{ spanId: 's6', kind: 'tool_result', name: '633 lines', status: 'ok', depth: 3, durationMs: null, tokens: 18_902 },`
- [[web/src/prototype/data.ts|web/src/prototype/data.ts]]: `{ spanId: 's7', kind: 'tool_call', name: 'Edit web/src/components/status.tsx', status: 'interrupted', depth: 2, durationMs: 90, tokens: null`
- [[web/src/prototype/data.ts|web/src/prototype/data.ts]]: `{ spanId: 's8', kind: 'error', name: 'File changed on disk, retrying', status: 'error', depth: 2, durationMs: null, tokens: null },`
- [[web/src/prototype/data.ts|web/src/prototype/data.ts]]: `{ spanId: 's9', kind: 'subagent', name: 'Explore — find chart callers', status: 'ok', depth: 1, durationMs: 46_000, tokens: 94_220 },`
- [[web/src/prototype/data.ts|web/src/prototype/data.ts]]: `{ spanId: 's10', kind: 'compaction', name: 'Context compacted', status: 'ok', depth: 1, durationMs: 3_100, tokens: null },`

## MatchKind lifecycle

- `exact`
- `suffix`
- `estimated`
- `none`

No assignment of these values was found in the code of this module.

Source:
- `MatchKind`: `export type MatchKind = 'exact' | 'suffix' | 'estimated' | 'none'`

## TokenDataKind lifecycle

- `full`
- `session`

No assignment of these values was found in the code of this module.

Source:
- `TokenDataKind`: `export type TokenDataKind = 'full' | 'session'`

## RateStatus lifecycle

- `ga`
- `preview`
- `retired`

No assignment of these values was found in the code of this module.

Source:
- `RateStatus`: `export type RateStatus = 'ga' | 'preview' | 'retired'`

## Request cost state

- `priced`
- `free`
- `unpriced`
- `unavailable`

Each request ends in exactly one state. The estimated flag is a mark on priced, not a state. [[src/ai_usage_cost/models.py|src/ai_usage_cost/models.py:8]]

| From | To | Trigger | Code |
|---|---|---|---|
| loaded | unavailable | the request has no token counts | [[src/ai_usage_cost/pricing.py|src/ai_usage_cost/pricing.py:421]] |
| loaded | free | the provider rules say free | [[src/ai_usage_cost/pricing.py|src/ai_usage_cost/pricing.py:422]] |
| loaded | unpriced | no rate row matches the model | [[src/ai_usage_cost/pricing.py|src/ai_usage_cost/pricing.py:425]] |
| loaded | priced | a rate row matches | [[src/ai_usage_cost/pricing.py|src/ai_usage_cost/pricing.py:426]] |

Transitions out of a state are not found: the state is recomputed on every analysis and never changes in place.

Source:
- `cost_state_of`: `def cost_state_of(`

## RowStatus lifecycle

- `ga`
- `preview`
- `retired`

No assignment of these values was found in the code of this module.

Source:
- `RowStatus`: `RowStatus = Literal["ga", "preview", "retired"]`

## Warnings list view

- `ShowingAll, Filtered, NothingShown, NoGroups. A separate machine per group row has Collapsed, Expanded, AlwaysOpen and Stuck.`

Mount to ShowingAll while no kind is picked [[web/src/components/states.tsx|web/src/components/states.tsx:248]]. ShowingAll to Filtered when a kind toggle is picked [[web/src/components/states.tsx|web/src/components/states.tsx:260]]. Filtered to ShowingAll when the last kind is cleared [[web/src/components/states.tsx|web/src/components/states.tsx:249]]. A row goes from Collapsed to Expanded on the Show files button, which exists only when its count is above one [[web/src/components/states.tsx|web/src/components/states.tsx:224]]. A row with a count of exactly one is always open [[web/src/components/states.tsx|web/src/components/states.tsx:230]].

Source:
- `WarningsList`: `const shown = kinds.length === 0 ? groups : groups.filter((group) => kinds.includes(group.kind))`
- `WarningGroupRow`: `{(expanded || group.count === 1) && (`

## Info box open state

- `Closed, Open.`

Closed to Open when the pointer has stayed on the trigger or the box for 400 ms [[web/src/components/metric-info.tsx|web/src/components/metric-info.tsx:92]], when the trigger gets keyboard focus [[web/src/components/metric-info.tsx|web/src/components/metric-info.tsx:134]], or on a click [[web/src/components/metric-info.tsx|web/src/components/metric-info.tsx:143]]. Open to Closed when the pointer has been outside both for 250 ms and the trigger is not focused [[web/src/components/metric-info.tsx|web/src/components/metric-info.tsx:105]], on a second click, or on any close request of the popover [[web/src/components/metric-info.tsx|web/src/components/metric-info.tsx:116]].

Source:
- `MetricInfo`: `const [open, setOpen] = useState(false)`

## Workspace tab data

- `idle`
- `loading`
- `ready`
- `error`

idle to loading: the tab is selected for the first time [[web/src/SessionWorkspace.tsx|web/src/SessionWorkspace.tsx:453]]
loading to ready: the endpoint answers [[web/src/SessionWorkspace.tsx|web/src/SessionWorkspace.tsx:101]]
loading to error: the endpoint fails and the request was not aborted [[web/src/SessionWorkspace.tsx|web/src/SessionWorkspace.tsx:105]]
error to loading: not found; only a new session or a remount runs the load again

Source:
- `useLazyResource`: `function useLazyResource<T>(enabled: boolean, load: (signal: AbortSignal) => Promise<T>): Loadable<T> {`
