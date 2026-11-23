---
code: SM-10
entity: WarningsList
tags:
  - ba/state-machine
maturity: draft
---
# Warnings list view

## States

| Name |
| --- |
| ShowingAll, Filtered, NothingShown, NoGroups. A separate machine per group row has Collapsed, Expanded, AlwaysOpen and Stuck. |

## Transitions

| Name |
| --- |
| Mount to ShowingAll while no kind is picked `web/src/components/states.tsx:248`. ShowingAll to Filtered when a kind toggle is picked `web/src/components/states.tsx:260`. Filtered to ShowingAll when the last kind is cleared `web/src/components/states.tsx:249`. A row goes from Collapsed to Expanded on the Show files button, which exists only when its count is above one `web/src/components/states.tsx:224`. A row with a count of exactly one is always open `web/src/components/states.tsx:230`. |

## Sources

- [[Code of localtokenomics]] | confirmed
  > const shown = kinds.length === 0 ? groups : groups.filter((group) => kinds.includes(group.kind))
- [[Code of localtokenomics]] | confirmed
  > {(expanded || group.count === 1) && (
