---
code: BR-34
category: design system
tags:
  - ba/rule
maturity: approved
---
# Caller class names override primitive defaults

## Statement

Every primitive merges its default Tailwind classes with the caller className through cn, so a caller override replaces a conflicting default instead of stacking with it.

## Enforced in

- [[UC-01 Compare a dashboard screen with its reference]]
- [[UC-05 Read usage and cost for a period]]
- [[UC-06 Inspect one session]]
- [[UC-07 Rate a session outcome]]
- [[UC-08 Check list prices]]
- [[UC-09 Read a figure and see how far to trust it]]
- [[UC-10 Narrow a list and choose its columns]]
- [[UC-11 Inspect a chart point]]
- [[UC-12 Review a session's spans and context use]]
- [[UC-28 Sort the session list and open one session in the prototype]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/design-system/cn.ts::cn | confirmed
  > return twMerge(clsx(inputs))
