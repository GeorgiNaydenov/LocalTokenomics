---
code: SM-12
entity: Workspace tab
tags:
  - ba/state-machine
maturity: draft
---
# Workspace tab data

## States

| Name |
| --- |
| idle |
| loading |
| ready |
| error |

## Transitions

| Name |
| --- |
| idle to loading: the tab is selected for the first time `web/src/SessionWorkspace.tsx:453` |
| loading to ready: the endpoint answers `web/src/SessionWorkspace.tsx:101` |
| loading to error: the endpoint fails and the request was not aborted `web/src/SessionWorkspace.tsx:105` |
| error to loading: not found; only a new session or a remount runs the load again |

## Sources

- [[Code of localtokenomics]] | confirmed
  > function useLazyResource<T>(enabled: boolean, load: (signal: AbortSignal) => Promise<T>): Loadable<T> {
