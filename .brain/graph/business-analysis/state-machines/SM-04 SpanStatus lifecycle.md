---
code: SM-04
entity: SpanStatus
tags:
  - ba/state-machine
maturity: approved
---
# SpanStatus lifecycle

## States

| Name |
| --- |
| ok |
| error |
| interrupted |
| aborted |
| running |
| unknown |

## Transitions

| Name |
| --- |
| From any state to error: useLazyResource sets status at `web/src/SessionWorkspace.tsx:105` |
| From any state to error: toggleContent sets status at `web/src/TraceTab.tsx:796` |
| From any state to ok: (module) sets status at `web/src/prototype/data.ts:802` |
| From any state to ok: (module) sets status at `web/src/prototype/data.ts:803` |
| From any state to ok: (module) sets status at `web/src/prototype/data.ts:804` |
| From any state to ok: (module) sets status at `web/src/prototype/data.ts:805` |
| From any state to ok: (module) sets status at `web/src/prototype/data.ts:806` |
| From any state to ok: (module) sets status at `web/src/prototype/data.ts:807` |
| From any state to interrupted: (module) sets status at `web/src/prototype/data.ts:808` |
| From any state to error: (module) sets status at `web/src/prototype/data.ts:809` |
| From any state to ok: (module) sets status at `web/src/prototype/data.ts:810` |
| From any state to ok: (module) sets status at `web/src/prototype/data.ts:811` |
| From any state to ok: (module) sets status at `web/src/prototype/data.ts:812` |

## Sources

- [[Code of localtokenomics]] | inferred
  > export type SpanStatus = 'ok' | 'error' | 'interrupted' | 'aborted' | 'running' | 'unknown'
- [[Code of localtokenomics]] | inferred
  > setSettled({ load, result: { status: 'error', message: messageOf(cause) } })
- [[Code of localtokenomics]] | inferred
  > const next: ContentState = isMissing(cause) ? { status: 'off' } : { status: 'error', message: messageOf(cause) }
- [[Code of localtokenomics]] | inferred
  > { spanId: 's1', kind: 'turn', name: 'Turn 14 — rebuild the design system', status: 'ok', depth: 0, durationMs: 184_000, tokens: 412_004 },
- [[Code of localtokenomics]] | inferred
  > { spanId: 's2', kind: 'user', name: 'User message', status: 'ok', depth: 1, durationMs: null, tokens: 1_204 },
- [[Code of localtokenomics]] | inferred
  > { spanId: 's3', kind: 'model_call', name: 'claude-opus-5', status: 'ok', depth: 1, durationMs: 21_400, tokens: 188_320 },
- [[Code of localtokenomics]] | inferred
  > { spanId: 's4', kind: 'reasoning', name: 'Reasoning', status: 'ok', depth: 2, durationMs: 8_200, tokens: 42_110 },
- [[Code of localtokenomics]] | inferred
  > { spanId: 's5', kind: 'tool_call', name: 'Read web/src/Overview.tsx', status: 'ok', depth: 2, durationMs: 140, tokens: null },
- [[Code of localtokenomics]] | inferred
  > { spanId: 's6', kind: 'tool_result', name: '633 lines', status: 'ok', depth: 3, durationMs: null, tokens: 18_902 },
- [[Code of localtokenomics]] | inferred
  > { spanId: 's7', kind: 'tool_call', name: 'Edit web/src/components/status.tsx', status: 'interrupted', depth: 2, durationMs: 90, tokens: null
- [[Code of localtokenomics]] | inferred
  > { spanId: 's8', kind: 'error', name: 'File changed on disk, retrying', status: 'error', depth: 2, durationMs: null, tokens: null },
- [[Code of localtokenomics]] | inferred
  > { spanId: 's9', kind: 'subagent', name: 'Explore — find chart callers', status: 'ok', depth: 1, durationMs: 46_000, tokens: 94_220 },
- [[Code of localtokenomics]] | inferred
  > { spanId: 's10', kind: 'compaction', name: 'Context compacted', status: 'ok', depth: 1, durationMs: 3_100, tokens: null },
