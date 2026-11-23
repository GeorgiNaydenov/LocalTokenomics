---
code: BR-122
tags:
  - ba/rule
maturity: draft
---
# Drawer trace blocks show the same sample data for every traced session

## Statement

The context window, trace, insights and capability blocks of the session drawer are read from fixed sample arrays and are not derived from the chosen session, so they are identical for every session whose traced flag is true.

## Enforced in

- [[UC-01 Compare a dashboard screen with its reference]]
- [[UC-09 Read a figure and see how far to trust it]]
- [[UC-10 Narrow a list and choose its columns]]
- [[UC-12 Review a session's spans and context use]]
- [[UC-28 Sort the session list and open one session in the prototype]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/prototype/Screens.tsx | confirmed
  > spans={TRACE_SPANS.map((span) => ({
- [[Code of localtokenomics]] @ enforced-by -> web/src/prototype/Screens.tsx | confirmed
  > points={CONTEXT_SNAPSHOTS}
