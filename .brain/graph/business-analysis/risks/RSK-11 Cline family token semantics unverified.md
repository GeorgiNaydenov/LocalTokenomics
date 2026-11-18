---
code: RSK-11
tags:
  - ba/risk
maturity: approved
---
# Cline family token semantics unverified

## Risk

Cline family token semantics are unverified: it is not known whether input tokens include cache buckets, so cost may be off.

## Mitigation

The policy is held per source in one table and the module header says to flip it when a real log shows otherwise.
