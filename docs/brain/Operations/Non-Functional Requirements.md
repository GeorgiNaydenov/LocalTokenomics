---
title: Non-Functional Requirements
aliases: []
tags: [generated, nfr, requirements, spec]
area: operations
status: generated
audience: internal
maturity: draft
confidence: confirmed
covers: [src/ai_usage_cost/cli.py, src/ai_usage_cost/collect.py, src/ai_usage_cost/pricing.py,
  src/ai_usage_cost/privacy.py, src/ai_usage_cost/store.py, web/src/components/chart-hover.tsx,
  web/src/components/stat.tsx]
generated: true
anchors: true
---

# Non-Functional Requirements

> [!info] What this is
> What the application must keep true while it works: safety, privacy, performance and quality targets, each with the code that keeps it.

## NFR-01 Python version support

The package supports Python 3.11 or newer and the workflow tests 3.11, 3.12 and 3.13 on Ubuntu and Windows.

- **Target:** 3 Python versions on 2 operating systems
Source:
- `.github/workflows/python.yml`: `python-version: ["3.11", "3.12", "3.13"]`

## NFR-02 Keyboard and screen reader access to charts and timelines

Charts with hover detail and the span timeline can be operated with the keyboard, and the selected point is announced.

- **Target:** Arrow, Home, End and Escape keys, and a polite live region. `web/src/components/chart-hover.tsx:61`

## NFR-03 Reduced motion is respected

Animated numbers skip their animation when the reader prefers reduced motion.

- **Target:** No animation under the reduced motion media query. `web/src/components/stat.tsx:10`

## NFR-04 Chart colours follow the light and dark theme

A chart writes one set of colour variables for the light theme and one scoped to the dark selector, so series colours change with the theme.

- **Target:** Both themes covered by ChartStyle
Source:
- `THEMES`: `const THEMES = { light: "", dark: ".dark" } as const`

## NFR-05 PNG export runs without a display

The picture writer selects the non interactive Agg backend before importing pyplot.

- **Target:** no display server required
Source:
- `write_png`: `matplotlib.use("Agg")`

## NFR-06 Incremental ingest

Ingest avoids reparsing work: it skips unchanged files [[src/ai_usage_cost/store.py|src/ai_usage_cost/store.py:229]] and hashes a fixed window of [[src/ai_usage_cost/store.py|src/ai_usage_cost/store.py:19]] bytes to check a resumed file.

- **Target:** An unchanged file is skipped and a grown file is read from its old end when its source allows

## NFR-07 Rate lookup is cached

Rate lookups are cached by the raw model id because a session calls them tens of thousands of times: [[src/ai_usage_cost/pricing.py|src/ai_usage_cost/pricing.py:267]].

- **Target:** One prefix scan per distinct model id

## NFR-08 Released text size limit

Span text is cut to a byte limit before it is returned: [[src/ai_usage_cost/privacy.py|src/ai_usage_cost/privacy.py:11]].

- **Target:** At most 65,536 bytes of span text per request by default

## NFR-09 Store uses write ahead logging

The store opens in WAL mode and applies pending migrations in order: [[src/ai_usage_cost/store.py|src/ai_usage_cost/store.py:144]] and [[src/ai_usage_cost/store.py|src/ai_usage_cost/store.py:146]].

- **Target:** Journal mode WAL and migrations by user version

## NFR-10 GPU sampler command timeouts

Each external sampler call has a timeout: [[src/ai_usage_cost/collect.py|src/ai_usage_cost/collect.py:214]], [[src/ai_usage_cost/collect.py|src/ai_usage_cost/collect.py:183]] and [[src/ai_usage_cost/collect.py|src/ai_usage_cost/collect.py:197]].

- **Target:** 10 seconds for nvidia-smi and rocm-smi, 30 seconds for PowerShell counters, 0.5 seconds for Ollama

## NFR-11 Server binds to loopback by default

The serve and sql commands listen on the loopback address unless told otherwise: [[src/ai_usage_cost/cli.py|src/ai_usage_cost/cli.py:110]].

- **Target:** Host 127.0.0.1

## NFR-12 GPU sampling interval

The collect command samples at a default interval of two seconds and sleeps between readings. [[src/ai_usage_cost/cli.py|src/ai_usage_cost/cli.py:201]] [[src/ai_usage_cost/collect.py|src/ai_usage_cost/collect.py:277]]

- **Target:** One reading every 2 seconds by default, until stopped or a duration ends
