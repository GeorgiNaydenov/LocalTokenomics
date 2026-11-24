---
tags:
  - ba/glossary-term
maturity: draft
---
# Token bucket

## Definition

One of the four counted kinds of tokens in a session: uncached input, cache read, cache write and output. The drawer splits a session cost across them with fixed weights.

## Sources

- [[Code of localtokenomics]] @ web/src/components/series.ts:7 | inferred
  > export interface TokenBucket {
