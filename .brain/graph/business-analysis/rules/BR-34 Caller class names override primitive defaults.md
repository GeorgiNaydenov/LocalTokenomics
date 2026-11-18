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

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/design-system/cn.ts::cn | confirmed
  > return twMerge(clsx(inputs))
