---
code: BR-25
tags:
  - ba/rule
maturity: approved
---
# Automatic rescan every five minutes

## Statement

While the tab is visible the dashboard asks the server to rescan logs every five minutes.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/App.tsx | confirmed
  > const FIVE_MINUTES = 5 * 60 * 1000
- [[Code of localtokenomics]] @ enforced-by -> web/src/App.tsx | confirmed
  > if (interval === null) interval = setInterval(doRefresh, FIVE_MINUTES)
