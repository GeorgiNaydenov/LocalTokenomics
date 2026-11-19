---
title: UC-23 Read the text of one span
aliases: [UC-23, Read the text of one span]
tags: [generated, spec, use-case]
area: business
status: generated
audience: internal
maturity: approved
confidence: confirmed
covers: [src/ai_usage_cost/api.py, src/ai_usage_cost/privacy.py, tests/test_api.py,
  tests/test_privacy.py]
generated: true
use-cases: [UC-23]
subdomain: Privacy and retention
---

# UC-23 Read the text of one span

> [!info] What this is
> A use case of the [[Privacy and retention]] subdomain, written from the code. Every step cites the line that does it, so a reader can check the claim in one click.

> [!tip] How to use it
> Read the main flow first, then the alternative flows. The rules, terms and diagrams at the end are the ones this use case relies on.

- **Subdomain:** [[Privacy and retention]]
- **Actors:** [[Actors|Config]], [[Actors#Person using the tool|Person using the tool]], [[Actors|Released text is cut and then redacted]], [[Actors|Span]], [[Actors|Span text is refused in metadata only mode]]
- **Maturity:** approved

## Description

The person reads the text of one step of a session, safely, when they have allowed it.

## Preconditions

Metadata only is off in the settings and the span has a content path.

## Main flow

1. The person asks for the content of a span. [[src/ai_usage_cost/api.py|src/ai_usage_cost/api.py:374]]
2. The interface finds the span in the session. [[src/ai_usage_cost/api.py|src/ai_usage_cost/api.py:376]]
3. The privacy module reads the record from the log at the stored offset. [[src/ai_usage_cost/privacy.py|src/ai_usage_cost/privacy.py:91]]
4. The text is truncated and then redacted. [[src/ai_usage_cost/privacy.py|src/ai_usage_cost/privacy.py:98]]

## Alternative flows

- In metadata only mode the answer is 404. [[src/ai_usage_cost/api.py|src/ai_usage_cost/api.py:382]]
- An unknown span answers 404. [[src/ai_usage_cost/api.py|src/ai_usage_cost/api.py:378]]

## Postconditions

The text is returned cut and redacted, with counts.

## Acceptance criteria

- Content is unavailable while metadata only is on. [[tests/test_api.py|tests/test_api.py:568]]
- Content is redacted when capture is allowed. [[tests/test_api.py|tests/test_api.py:574]]
- Each secret pattern is replaced. [[tests/test_privacy.py|tests/test_privacy.py:56]]

## Business rules

- [[Privacy and retention Rules#BR-121 Unreadable span text answers 404|BR-121 Unreadable span text answers 404]]
- [[Privacy and retention Rules#BR-75 Span text is refused in metadata only mode|BR-75 Span text is refused in metadata only mode]]
- [[Privacy and retention Rules#BR-76 Released text is cut and then redacted|BR-76 Released text is cut and then redacted]]
- [[Privacy and retention Rules#BR-77 A bad configuration file gives the defaults|BR-77 A bad configuration file gives the defaults]]

## Code

- [[src/ai_usage_cost/api.py]]
- [[src/ai_usage_cost/privacy.py]]
- [[tests/test_api.py]]
- [[tests/test_privacy.py]]
