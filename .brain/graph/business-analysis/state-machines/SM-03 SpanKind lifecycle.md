---
code: SM-03
entity: SpanKind
tags:
  - ba/state-machine
maturity: approved
---
# SpanKind lifecycle

## States

| Name |
| --- |
| turn |
| user |
| assistant |
| reasoning |
| model_call |
| tool_call |
| tool_result |
| retrieval |
| compaction |
| error |
| subagent |

## Transitions

| Name |
| --- |
| From any state to error: useLazyResource sets status at `web/src/SessionWorkspace.tsx:105` |
| From any state to error: toggleContent sets status at `web/src/TraceTab.tsx:796` |
| From any state to error: (module) sets status at `web/src/prototype/data.ts:809` |

## Sources

- [[Code of localtokenomics]] | inferred
  > export type SpanKind =
- [[Code of localtokenomics]] | inferred
  > setSettled({ load, result: { status: 'error', message: messageOf(cause) } })
- [[Code of localtokenomics]] | inferred
  > const next: ContentState = isMissing(cause) ? { status: 'off' } : { status: 'error', message: messageOf(cause) }
- [[Code of localtokenomics]] | inferred
  > { spanId: 's8', kind: 'error', name: 'File changed on disk, retrying', status: 'error', depth: 2, durationMs: null, tokens: null },
