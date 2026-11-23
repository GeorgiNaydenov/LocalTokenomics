---
code: BR-25
tags:
  - ba/rule
maturity: approved
---
# Automatic rescan every five minutes

## Statement

While the tab is visible the dashboard asks the server to rescan logs every five minutes.

## Enforced in

- [[UC-05 Read usage and cost for a period]]
- [[UC-06 Inspect one session]]
- [[UC-07 Rate a session outcome]]
- [[UC-08 Check list prices]]
- [[UC-09 Read a figure and see how far to trust it]]
- [[UC-10 Narrow a list and choose its columns]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/App.tsx | confirmed
  > const FIVE_MINUTES = 5 * 60 * 1000
- [[Code of localtokenomics]] @ enforced-by -> web/src/App.tsx | confirmed
  > if (interval === null) interval = setInterval(doRefresh, FIVE_MINUTES)
