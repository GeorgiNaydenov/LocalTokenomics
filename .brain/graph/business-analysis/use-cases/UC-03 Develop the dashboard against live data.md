---
code: UC-03
primary_actor: Maintainer
subdomain: localtokenomics root area
actors:
  - Maintainer
no_models_reason: No model of the specification is declared in the code this use case cites or in a file that code imports directly.
rules:
  - A production build replaces the committed bundle
  - A type error stops the dashboard build
  - The prototype is excluded from the production build
tags:
  - ba/use-case
maturity: approved
---
# Develop the dashboard against live data

## Description

A maintainer runs the dashboard dev server, which forwards API requests to the Python server.

## Preconditions

- The Python server is running on port 8420.

## Postconditions

- The dev server shows the dashboard with live data.

## Main flow

1. 1. The maintainer starts the dev server with the dev script. `web/package.json:7`
2. 2. The dev server listens on port 5173. `web/vite.config.ts:19`
3. 3. Requests starting with /api are forwarded to the Python server. `web/vite.config.ts:22`

## Alternative flows

- 3a. The proxy target is the local server only, so with no Python server running the API requests get no answer. `web/vite.config.ts:22`

## Acceptance criteria

- The dev server answers on its own port and proxies the API path. `web/vite.config.ts:23`
- 3a: The proxy target is the local server only, so with no Python server running the API requests get no answer. `web/vite.config.ts:22`

## Sources

- [[Code of localtokenomics]] @ implemented-by -> web/package.json | inferred
  > "dev": "vite",
