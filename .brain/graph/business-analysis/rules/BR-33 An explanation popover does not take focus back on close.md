---
code: BR-33
category: behaviour
tags:
  - ba/rule
maturity: approved
---
# An explanation popover does not take focus back on close

## Statement

Closing the metric explanation popover does not return focus to its trigger, because focusing the trigger opens the popover again.

## Enforced in

- [[UC-06 Inspect one session]]
- [[UC-07 Rate a session outcome]]
- [[UC-08 Check list prices]]
- [[UC-09 Read a figure and see how far to trust it]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/components/metric-info.tsx::MetricInfo | confirmed
  >         onCloseAutoFocus={(event) => event.preventDefault()}
