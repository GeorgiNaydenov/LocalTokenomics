---
code: UC-02
primary_actor: Maintainer
actors:
  - Maintainer
rules:
  - A type error stops the dashboard build
  - A production build replaces the committed bundle
tags:
  - ba/use-case
maturity: approved
---
# Rebuild the dashboard bundle

## Description

A maintainer changes the dashboard source and rebuilds the bundle that the Python package serves.

## Preconditions

Node.js and npm are installed and dependencies are installed in the web folder.

## Postconditions

The output folder inside the Python package holds the new bundle.

## Main flow

1. 1. The maintainer runs the build script from the web folder. `web/package.json:8`
2. 2. The TypeScript check runs first and a type error stops the build. `web/package.json:8`
3. 3. Vite writes the bundle into the Python package folder after emptying it. `web/vite.config.ts:16`

## Alternative flows

2a. A type error stops the build and no bundle is written. `web/package.json:8`

## Special requirements

Asset paths are relative so the bundle loads from whatever URL the server mounts it on. `web/vite.config.ts:7`

## Acceptance criteria

The bundle is written to the folder the package ships. `web/vite.config.ts:15`

## Sources

- [[Code of localtokenomics]] @ implemented-by -> web/package.json | inferred
  > "build": "tsc --noEmit && vite build",
