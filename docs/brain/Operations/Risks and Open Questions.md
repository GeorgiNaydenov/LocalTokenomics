---
title: Risks and Open Questions
aliases: []
tags: [generated, open-question, risks, spec]
area: operations
status: generated
audience: internal
maturity: draft
confidence: confirmed
covers: []
generated: true
anchors: true
---

# Risks and Open Questions

> [!info] What this is
> What could go wrong and what is not yet known, each with the code that raises it.

## RSK-01 Prototype looks live but is staged

Filters, the rescan button and the scanned 2 min ago text suggest real behaviour but do nothing, so a reader may take the prototype for working product.

Notes state the staged parts; the migration guide marks the folder read only.


## RSK-02 Design system README and migration guide are out of date

The README says the shipped dashboard still runs on the old src/ds CSS system, but the shipped entry point already imports the new theme and the ds folder is absent.

Open question for the owner of the web folder; this chunk does not edit those files.


## RSK-03 No tests cover the prototype

No test file imports or lives inside the prototype folder, so a change to a reference screen is unchecked except by typecheck and lint.

Accepted: the folder is read only reference code.


## OQ-01 Is the prototype still wanted once every screen is ported？

The migration guide treats the folder as a working reference during the port. Should it be deleted or kept after the port, and should the README and guide be updated to say the port is done? Checked web/src/design-system/MIGRATION.md and README.md.
