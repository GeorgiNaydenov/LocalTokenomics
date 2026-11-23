---
code: BR-26
category: display
tags:
  - ba/rule
maturity: approved
---
# A missing value is shown as unavailable, never as zero

## Statement

Meters, bucket bars, comparison bars, token cells and session cards show the unavailable marker when a value is null or a total is not positive, and draw no bar.

## Enforced in

- [[UC-01 Compare a dashboard screen with its reference]]
- [[UC-05 Read usage and cost for a period]]
- [[UC-06 Inspect one session]]
- [[UC-07 Rate a session outcome]]
- [[UC-08 Check list prices]]
- [[UC-09 Read a figure and see how far to trust it]]
- [[UC-12 Review a session's spans and context use]]
- [[UC-28 Sort the session list and open one session in the prototype]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/components/status.tsx::Meter | confirmed
  >   if (value === null) {
- [[Code of localtokenomics]] @ enforced-by -> web/src/components/status.tsx::BucketBar | confirmed
  >   if (total <= 0) {
- [[Code of localtokenomics]] @ enforced-by -> web/src/components/session.tsx::TokenCell | confirmed
  >   if (label === null) {
