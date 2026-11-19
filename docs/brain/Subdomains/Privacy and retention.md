---
title: Privacy and retention
aliases: []
tags: [generated, spec, subdomain]
area: business
status: generated
audience: internal
maturity: draft
confidence: confirmed
covers: [src/ai_usage_cost/api.py, src/ai_usage_cost/pipeline.py, src/ai_usage_cost/privacy.py,
  src/ai_usage_cost/store.py, tests/test_api.py, tests/test_privacy.py, tests/test_store.py]
generated: true
---

# Privacy and retention

> [!info] What this is
> A subdomain: one area of the business that the application serves. This note lists its use cases, the rules it enforces and the terms it uses.

- **Type:** supporting

## Description

Decides whether span text may be shown, cuts and redacts it, and applies project exclusion and trace retention. Main code: [[src/ai_usage_cost/privacy.py|src/ai_usage_cost/privacy.py:86]] and [[src/ai_usage_cost/privacy.py|src/ai_usage_cost/privacy.py:52]].

## Use cases (2)

- [[UC-22 Forget a session]]
- [[UC-23 Read the text of one span]]

## Business rules (7)

All of them, with the code that enforces each one: [[Privacy and retention Rules]].

- [[Privacy and retention Rules#BR-121 Unreadable span text answers 404|BR-121 Unreadable span text answers 404]]
- [[Privacy and retention Rules#BR-73 A forgotten session is not stored again|BR-73 A forgotten session is not stored again]]
- [[Privacy and retention Rules#BR-74 An excluded project drops its spans|BR-74 An excluded project drops its spans]]
- [[Privacy and retention Rules#BR-75 Span text is refused in metadata only mode|BR-75 Span text is refused in metadata only mode]]
- [[Privacy and retention Rules#BR-76 Released text is cut and then redacted|BR-76 Released text is cut and then redacted]]
- [[Privacy and retention Rules#BR-77 A bad configuration file gives the defaults|BR-77 A bad configuration file gives the defaults]]
- [[Privacy and retention Rules#BR-83 Content retention is inert|BR-83 Content retention is inert]]
