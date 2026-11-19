---
title: UC-02 Rebuild the dashboard bundle
aliases: [UC-02, Rebuild the dashboard bundle]
tags: [generated, spec, use-case]
area: business
status: generated
audience: internal
maturity: approved
confidence: confirmed
covers: [web/package.json, web/vite.config.ts]
generated: true
use-cases: [UC-02]
subdomain: ''
---

# UC-02 Rebuild the dashboard bundle

> [!info] What this is
> A use case of the subdomain, written from the code. Every step cites the line that does it, so a reader can check the claim in one click.

> [!tip] How to use it
> Read the main flow first, then the alternative flows. The rules, terms and diagrams at the end are the ones this use case relies on.

- **Actors:** [[Actors|A production build replaces the committed bundle]], [[Actors|A type error stops the dashboard build]], [[Actors#Maintainer|Maintainer]]
- **Maturity:** approved

## Description

A maintainer changes the dashboard source and rebuilds the bundle that the Python package serves.

## Preconditions

Node.js and npm are installed and dependencies are installed in the web folder.

## Main flow

1. 1. The maintainer runs the build script from the web folder. [[web/package.json|web/package.json:8]]
2. 2. The TypeScript check runs first and a type error stops the build. [[web/package.json|web/package.json:8]]
3. 3. Vite writes the bundle into the Python package folder after emptying it. [[web/vite.config.ts|web/vite.config.ts:16]]

## Alternative flows

2a. A type error stops the build and no bundle is written. [[web/package.json|web/package.json:8]]

## Postconditions

The output folder inside the Python package holds the new bundle.

## Acceptance criteria

The bundle is written to the folder the package ships. [[web/vite.config.ts|web/vite.config.ts:15]]

## Business rules

- [[General Rules#BR-01 The prototype is excluded from the production build|BR-01 The prototype is excluded from the production build]]
- [[General Rules#BR-08 A type error stops the dashboard build|BR-08 A type error stops the dashboard build]]
- [[General Rules#BR-09 A production build replaces the committed bundle|BR-09 A production build replaces the committed bundle]]

## Code

- [[web/package.json]]
- [[web/vite.config.ts]]
