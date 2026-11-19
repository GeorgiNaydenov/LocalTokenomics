---
title: UC-03 Develop the dashboard against live data
aliases: [UC-03, Develop the dashboard against live data]
tags: [generated, spec, use-case]
area: business
status: generated
audience: internal
maturity: approved
confidence: confirmed
covers: [web/package.json, web/vite.config.ts]
generated: true
use-cases: [UC-03]
subdomain: ''
---

# UC-03 Develop the dashboard against live data

> [!info] What this is
> A use case of the subdomain, written from the code. Every step cites the line that does it, so a reader can check the claim in one click.

> [!tip] How to use it
> Read the main flow first, then the alternative flows. The rules, terms and diagrams at the end are the ones this use case relies on.

- **Actors:** [[Actors#Maintainer|Maintainer]]
- **Maturity:** approved

## Description

A maintainer runs the dashboard dev server, which forwards API requests to the Python server.

## Preconditions

The Python server is running on port 8420.

## Main flow

1. 1. The maintainer starts the dev server with the dev script. [[web/package.json|web/package.json:7]]
2. 2. The dev server listens on port 5173. [[web/vite.config.ts|web/vite.config.ts:19]]
3. 3. Requests starting with /api are forwarded to the Python server. [[web/vite.config.ts|web/vite.config.ts:22]]

## Alternative flows

3a. The proxy target is the local server only, so with no Python server running the API requests get no answer. [[web/vite.config.ts|web/vite.config.ts:22]]

## Postconditions

The dev server shows the dashboard with live data.

## Acceptance criteria

The dev server answers on its own port and proxies the API path. [[web/vite.config.ts|web/vite.config.ts:23]]

## Business rules

- [[General Rules#BR-01 The prototype is excluded from the production build|BR-01 The prototype is excluded from the production build]]
- [[General Rules#BR-08 A type error stops the dashboard build|BR-08 A type error stops the dashboard build]]
- [[General Rules#BR-09 A production build replaces the committed bundle|BR-09 A production build replaces the committed bundle]]

## Code

- [[web/package.json]]
- [[web/vite.config.ts]]
