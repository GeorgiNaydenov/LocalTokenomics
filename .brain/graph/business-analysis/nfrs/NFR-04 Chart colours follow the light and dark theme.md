---
code: NFR-04
category: usability
target: Both themes covered by ChartStyle
tags:
  - ba/nfr
maturity: approved
---
# Chart colours follow the light and dark theme

## Statement

A chart writes one set of colour variables for the light theme and one scoped to the dark selector, so series colours change with the theme.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/components/ui/chart.tsx::THEMES | confirmed
  > const THEMES = { light: "", dark: ".dark" } as const
