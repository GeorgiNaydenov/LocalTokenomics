---
code: NFR-08
category: privacy
target: At most 65,536 bytes of span text per request by default
applies_to:
  - Privacy and retention
tags:
  - ba/nfr
maturity: approved
---
# Released text size limit

## Statement

Span text is cut to a byte limit before it is returned: `src/ai_usage_cost/privacy.py:11`.
