---
code: BR-122
tags:
  - ba/rule
maturity: draft
---
# Drawer trace blocks show the same sample data for every traced session

## Statement

The context window, trace, insights and capability blocks of the session drawer are read from fixed sample arrays and are not derived from the chosen session, so they are identical for every session whose traced flag is true.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/prototype/Screens.tsx | confirmed
  > spans={TRACE_SPANS.map((span) => ({
- [[Code of localtokenomics]] @ enforced-by -> web/src/prototype/Screens.tsx | confirmed
  > points={CONTEXT_SNAPSHOTS}
