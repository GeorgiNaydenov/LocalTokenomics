---
tags:
  - ba/glossary-term
maturity: draft
---
# Resume hook

## Definition

An optional function of a reader, named parse_resume, that reads a log again only from the byte offset an earlier scan reached, so a log that only grew is not parsed from the start.
