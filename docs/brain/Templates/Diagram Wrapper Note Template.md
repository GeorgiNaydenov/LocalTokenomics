---
title: <title>
aliases: []
tags:
  - diagram
  - mermaid
area: diagrams
status: draft
audience: internal
covers: []
sources:
  - docs/architecture/diagrams/<name>.mmd
---

# <title>

> [!info] What this is
> One-paragraph explanation of what the diagrams depict.

> [!tip] Why it matters
> Explain who needs it and what decision it supports.

> [!example] How to read this
> Explain notation, direction, lanes, shapes, or state transitions.

Each entry in `sources` is a vault-root-relative `.mmd` or `.bpmn` path. Add one `##` section per entry, in the same order.

## <Diagram title>

For a Mermaid source, keep the marker pair below. Its id is `diagram-` plus the file name without the extension (`docs/architecture/diagrams/<name>.mmd` gives `diagram-<name>`), and the sync script fills it from that file.

%% generated:diagram-<name> start (do not edit; run npm run docs:vault) %%
%% generated:diagram-<name> end %%

## <BPMN diagram title>

For a BPMN source, list the `.bpmn` path in `sources`, add the `bpmn` tag, omit the marker pair (BPMN entries are never synced), and embed the render by hand with `![[docs/architecture/rendered/<name>.svg]]`.

## Decisions Encoded

- Decision and ADR link.

## Source Anchors

- `README.md`, or the code file the note explains, written as a full-path wiki-link with its extension
