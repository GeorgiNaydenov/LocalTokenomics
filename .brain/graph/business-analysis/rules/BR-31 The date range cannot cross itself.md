---
code: BR-31
category: validation
tags:
  - ba/rule
maturity: approved
---
# The date range cannot cross itself

## Statement

The from date cannot be later than the to date, and the to date cannot be earlier than the from date.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/components/filters.tsx::DateRange | confirmed
  >         max={until ?? max}
- [[Code of localtokenomics]] @ enforced-by -> web/src/components/filters.tsx::DateRange | confirmed
  >         min={since ?? min}
