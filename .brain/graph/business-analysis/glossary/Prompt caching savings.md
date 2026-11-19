---
tags:
  - ba/glossary-term
maturity: draft
---
# Prompt caching savings

## Definition

The difference between the cost without caching and the cost with it, shown only when positive.

## Sources

- [[Code of localtokenomics]] @ declared-in -> src/ai_usage_cost/models.py::cache_savings | confirmed
  > return self.no_cache_equivalent - self.total
