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

## Sources

- [[Code of localtokenomics]] @ enforced-by -> web/src/components/status.tsx::Meter | confirmed
  >   if (value === null) {
- [[Code of localtokenomics]] @ enforced-by -> web/src/components/status.tsx::BucketBar | confirmed
  >   if (total <= 0) {
- [[Code of localtokenomics]] @ enforced-by -> web/src/components/session.tsx::TokenCell | confirmed
  >   if (label === null) {
