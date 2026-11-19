---
code: OQ-22
priority: low
tags:
  - ba/open-question
maturity: draft
---
# Are the chart legend parts still needed

## Question

The wrapper exports a legend and a legend content part, but the time chart draws its own key list instead. Does any screen plan to use these two, or can they go? `web/src/components/ui/chart.tsx:270` `web/src/components/chart-time.tsx:174`
