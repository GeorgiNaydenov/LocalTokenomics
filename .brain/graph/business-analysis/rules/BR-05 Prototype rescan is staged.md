---
code: BR-05
tags:
  - ba/rule
maturity: approved
---
# Prototype rescan is staged

## Statement

The Rescan logs button only shows a scanning state for 900 milliseconds and reads no logs.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/prototype/Prototype.tsx | confirmed
  > setTimeout(() => setScanning(false), 900)
