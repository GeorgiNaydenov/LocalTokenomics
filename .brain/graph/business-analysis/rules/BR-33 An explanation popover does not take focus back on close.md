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

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/components/metric-info.tsx::MetricInfo | confirmed
  >         onCloseAutoFocus={(event) => event.preventDefault()}
