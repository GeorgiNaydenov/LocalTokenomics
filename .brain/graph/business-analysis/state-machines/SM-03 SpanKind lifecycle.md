---
code: SM-03
entity: SpanKind
tags:
  - ba/state-machine
maturity: approved
---
# SpanKind lifecycle

## States

turn
user
assistant
reasoning
model_call
tool_call
tool_result
retrieval
compaction
error
subagent

## Transitions

From any state to error: useLazyResource sets status at `web/src/SessionWorkspace.tsx:105`
From any state to error: toggleContent sets status at `web/src/TraceTab.tsx:796`
From any state to error: (module) sets status at `web/src/prototype/data.ts:809`

## Sources

- [[Code of localtokenomics]] @ implemented-by -> web/src/api.ts::SpanKind | inferred
  > export type SpanKind =
- [[Code of localtokenomics]] @ implemented-by -> web/src/SessionWorkspace.tsx::useLazyResource | inferred
  > setSettled({ load, result: { status: 'error', message: messageOf(cause) } })
- [[Code of localtokenomics]] @ implemented-by -> web/src/TraceTab.tsx::toggleContent | inferred
  > const next: ContentState = isMissing(cause) ? { status: 'off' } : { status: 'error', message: messageOf(cause) }
- [[Code of localtokenomics]] @ implemented-by -> web/src/prototype/data.ts | inferred
  > { spanId: 's8', kind: 'error', name: 'File changed on disk, retrying', status: 'error', depth: 2, durationMs: null, tokens: null },
