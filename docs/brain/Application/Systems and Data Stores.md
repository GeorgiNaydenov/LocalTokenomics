---
title: Systems and Data Stores
aliases: []
tags: [application, generated, spec, systems]
area: application
status: generated
audience: internal
maturity: draft
confidence: confirmed
covers: [src/ai_usage_cost/pipeline.py, src/ai_usage_cost/pricing.py, src/ai_usage_cost/privacy.py]
generated: true
anchors: true
---

# Systems and Data Stores

> [!info] What this is
> The parts the application is built from and the places it keeps data.

## Ai usage cost

The python component src/ai_usage_cost with 13 files and 5069 lines. Its documentation lives in the chunk ch-localtokenomics-src-ai-usage-cost.

Source:
- [[src/ai_usage_cost/__init__.py|src/ai_usage_cost/__init__.py:1-1]]: `__version__ = "0.2.0"`

## Ai usage cost render

The python component src/ai_usage_cost/render with 3 files and 187 lines. Its documentation lives in the chunk ch-localtokenomics-src-ai-usage-cost-render.

Source:
- [[src/ai_usage_cost/render/__init__.py|src/ai_usage_cost/render/__init__.py:1-1]]

## Ai usage cost sources

The python component src/ai_usage_cost/sources with 22 files and 4722 lines. Its documentation lives in the chunk ch-localtokenomics-src-ai-usage-cost-sources.

Source:
- [[src/ai_usage_cost/sources/__init__.py|src/ai_usage_cost/sources/__init__.py:1-5]]: `from __future__ import annotations`

## localtokenomics root

The python component localtokenomics root with 2 files and 1668 lines. Its documentation lives in the chunk ch-localtokenomics-root.

Source:
- [[scripts/demo_logs.py|scripts/demo_logs.py:1-5]]: `"""Generate synthetic Claude Code, Codex, Jan and Dyad logs for developing the dashboard.`

## Web

The typescript component web/src with 20 files and 7127 lines. Its documentation lives in the chunk ch-localtokenomics-web-src.

Source:
- [[web/src/App.tsx|web/src/App.tsx:1-5]]: `import { useCallback, useEffect, useState } from 'react'`

## Web prototype

The typescript component web/src/prototype with 10 files and 3215 lines. Its documentation lives in the chunk ch-localtokenomics-web-src-prototype.

Source:
- [[web/src/prototype/Gallery.tsx|web/src/prototype/Gallery.tsx:1-5]]: `import { useState } from 'react'`

## Web UI components

The typescript component web/src/components with 18 files and 3024 lines. Its documentation lives in the chunk ch-localtokenomics-web-src-components.

Source:
- [[web/src/components/chart-hover.tsx|web/src/components/chart-hover.tsx:1-5]]: `import * as React from 'react'`

## Web ui UI components

The typescript component web/src/components/ui with 25 files and 2083 lines. Its documentation lives in the chunk ch-localtokenomics-web-src-components-ui.

Source:
- [[web/src/components/ui/accordion.tsx|web/src/components/ui/accordion.tsx:1-5]]: `"use client"`

## Data of Ai usage cost

The 51 entities declared in the Ai usage cost module, stored in the tables apps, chats, files, messages, outcomes, requests.


## Data of Ai usage cost sources

The 2 entities declared in the Ai usage cost sources module.


## Privacy configuration file

An optional config.json in the store folder. When it is missing or invalid the defaults apply: [[src/ai_usage_cost/privacy.py|src/ai_usage_cost/privacy.py:12]].

Source:
- `DEFAULT_CONFIG_PATH`: `DEFAULT_CONFIG_PATH = Path.home()`

## Rate table file

The shipped rates.json beside the pricing code, replaceable with the rates option: [[src/ai_usage_cost/pricing.py|src/ai_usage_cost/pricing.py:22]].

Source:
- `DEFAULT_RATES_PATH`: `DEFAULT_RATES_PATH = Path(__file__)`

## Usage store

A SQLite file in the home folder that holds requests, files, trace events, outcomes, exclusions and GPU samples: [[src/ai_usage_cost/pipeline.py|src/ai_usage_cost/pipeline.py:28]].

Source:
- `DEFAULT_DB_PATH`: `DEFAULT_DB_PATH = Path.home()`
