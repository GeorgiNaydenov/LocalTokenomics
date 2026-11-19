---
title: Privacy and retention Rules
aliases: []
tags: [business, generated, rules, spec]
area: business
status: generated
audience: internal
maturity: draft
confidence: confirmed
covers: [src/ai_usage_cost/api.py, src/ai_usage_cost/pipeline.py, src/ai_usage_cost/privacy.py,
  src/ai_usage_cost/store.py]
generated: true
anchors: true
---

# Privacy and retention Rules

> [!info] What this is
> The business rules of the [[Privacy and retention]] subdomain, as the code enforces them. Each rule is a heading, so a use case links straight to it, and each names the line of code that enforces it.

## BR-121 Unreadable span text answers 404

The content route answers 404 when the span is not in the session, and also when its text is not released or cannot be read. [[src/ai_usage_cost/api.py|src/ai_usage_cost/api.py:382]]

- **Category:** interface
- **Used in:** [[UC-22 Forget a session]], [[UC-23 Read the text of one span]]

Source:
- `create_app.span_content`: `raise HTTPException(404, f"no readable content for span {span_id!r}") from exc`

## BR-73 A forgotten session is not stored again

After a person forgets a session its spans and rating are deleted and an exclusion row keeps its spans out of later scans. Its requests stay. [[src/ai_usage_cost/store.py|src/ai_usage_cost/store.py:273]]

- **Category:** privacy
- **Used in:** [[UC-22 Forget a session]]

Source:
- `ingest`: `if (span.source, span.session_id) in excluded_sessions:`

## BR-74 An excluded project drops its spans

A span whose project equals an excluded entry, or whose working directory starts with it, is not stored. [[src/ai_usage_cost/store.py|src/ai_usage_cost/store.py:314]]

- **Category:** privacy
- **Used in:** [[UC-22 Forget a session]]

Source:
- `_in_excluded_project`: `directory.startswith(entry)`

## BR-75 Span text is refused in metadata only mode

While metadata only is on, or when a span has no content path, reading its text raises content unavailable and the API answers 404. [[src/ai_usage_cost/privacy.py|src/ai_usage_cost/privacy.py:87]]

- **Category:** privacy
- **Used in:** [[UC-23 Read the text of one span]]

Source:
- `read_content`: `if config.metadata_only or span.content_path is None:`

## BR-76 Released text is cut and then redacted

Text that is released is truncated to the configured byte limit and then has secrets replaced by a marker that names the kind. [[src/ai_usage_cost/privacy.py|src/ai_usage_cost/privacy.py:97]]

- **Category:** privacy
- **Used in:** [[UC-23 Read the text of one span]]

Source:
- `read_content`: `text, truncated = truncate(text, config.max_content_bytes)`

## BR-77 A bad configuration file gives the defaults

A missing, unreadable or invalid config.json is replaced by the defaults, which keep metadata only on. [[src/ai_usage_cost/privacy.py|src/ai_usage_cost/privacy.py:63]]

- **Category:** privacy
- **Used in:** [[UC-23 Read the text of one span]]

Source:
- `load_config`: `except (OSError, ValueError):`

## BR-83 Content retention is inert

Setting content retention days only adds a warning, because no content is stored. [[src/ai_usage_cost/pipeline.py|src/ai_usage_cost/pipeline.py:242]]

- **Category:** privacy

Source:
- `analyze`: `content_retention_days is set but inert`
