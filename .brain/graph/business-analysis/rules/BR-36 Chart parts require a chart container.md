---
code: BR-36
category: design system
unlinked_reason: No use case cites the file this is declared in, a file it imports directly or a file that imports it.
tags:
  - ba/rule
maturity: approved
---
# Chart parts require a chart container

## Statement

The chart tooltip and legend content read the chart config through a context, and using them outside a chart container throws an error.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/components/ui/chart.tsx::useChart | confirmed
  > throw new Error("useChart must be used within a <ChartContainer />")
