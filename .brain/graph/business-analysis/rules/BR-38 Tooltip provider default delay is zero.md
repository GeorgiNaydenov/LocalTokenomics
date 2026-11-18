---
code: BR-38
category: design system
tags:
  - ba/rule
maturity: approved
---
# Tooltip provider default delay is zero

## Statement

The tooltip provider shows tooltips without a hover delay unless the app gives a delayDuration, and the dashboard roots give 200 milliseconds.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/components/ui/tooltip.tsx::TooltipProvider | confirmed
  > delayDuration = 0,
