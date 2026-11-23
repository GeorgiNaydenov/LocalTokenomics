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

## Enforced in

- [[UC-17 See what my AI usage would cost]]
- [[UC-18 Explore spend in the dashboard]]
- [[UC-21 Inspect and rate one session]]
- [[UC-22 Forget a session]]
- [[UC-23 Read the text of one span]]

## Sources

- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/privacy.py | confirmed
  > except (OSError, ValueError):
- [[Code of localtokenomics]] @ enforced-by -> src/ai_usage_cost/privacy.py | confirmed
  > except ValidationError:
