---
code: BR-114
category: privacy
tags:
  - ba/rule
maturity: draft
---
# A settings file that cannot be loaded is ignored as a whole

## Statement

When the optional settings file is missing, unreadable, not valid JSON or fails validation, every setting takes its default at once, not only the faulty one, and no warning is raised.

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/privacy.py | confirmed
  > except (OSError, ValueError):
- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/privacy.py | confirmed
  > except ValidationError:
