---
code: BR-14
category: guard
tags:
  - ba/rule
maturity: approved
---
# useChart refuses when !context

## Statement

In useChart, when !context: the code throws Error, message "useChart must be used within a <ChartContainer />". Located at web/src/components/ui/chart.tsx lines 32-33.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/components/ui/chart.tsx::useChart | inferred
  > if (!context) {
