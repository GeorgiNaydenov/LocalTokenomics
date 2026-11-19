---
code: UC-23
primary_actor: Person using the tool
subdomain: Privacy and retention
level: goal
actors:
  - Person using the tool
models:
  - Span
  - Config
rules:
  - Span text is refused in metadata only mode
  - Released text is cut and then redacted
tags:
  - ba/use-case
maturity: approved
---
# Read the text of one span

## Description

The person reads the text of one step of a session, safely, when they have allowed it.

## Preconditions

Metadata only is off in the settings and the span has a content path.

## Postconditions

The text is returned cut and redacted, with counts.

## Main flow

1. The person asks for the content of a span. `src/ai_usage_cost/api.py:374`
2. The interface finds the span in the session. `src/ai_usage_cost/api.py:376`
3. The privacy module reads the record from the log at the stored offset. `src/ai_usage_cost/privacy.py:91`
4. The text is truncated and then redacted. `src/ai_usage_cost/privacy.py:98`

## Alternative flows

- In metadata only mode the answer is 404. `src/ai_usage_cost/api.py:382`
- An unknown span answers 404. `src/ai_usage_cost/api.py:378`

## Acceptance criteria

- Content is unavailable while metadata only is on. `tests/test_api.py:568`
- Content is redacted when capture is allowed. `tests/test_api.py:574`
- Each secret pattern is replaced. `tests/test_privacy.py:56`

## Sources

- [[Code of localtokenomics]] @ implemented-by -> src/ai_usage_cost/api.py::create_app | inferred
  > def span_content(source: str, session_id: str, span_id: str)
