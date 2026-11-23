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

## Enforced in

- [[UC-01 Compare a dashboard screen with its reference]]
- [[UC-09 Read a figure and see how far to trust it]]
- [[UC-12 Review a session's spans and context use]]
- [[UC-28 Sort the session list and open one session in the prototype]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/components/ui/tooltip.tsx::TooltipProvider | confirmed
  > delayDuration = 0,
