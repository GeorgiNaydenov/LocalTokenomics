---
code: BR-05
tags:
  - ba/rule
maturity: approved
---
# Prototype rescan is staged

## Statement

The Rescan logs button only shows a scanning state for 900 milliseconds and reads no logs.

## Enforced in

- [[UC-01 Compare a dashboard screen with its reference]]
- [[UC-28 Sort the session list and open one session in the prototype]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/prototype/Prototype.tsx | confirmed
  > setTimeout(() => setScanning(false), 900)
