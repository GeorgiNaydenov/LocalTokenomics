---
title: Diagram Notation Guide
aliases: [Diagram Legend, Notation Glossary]
tags: [diagram, overview]
area: diagrams
status: active
audience: internal
maturity: approved
confidence: confirmed
covers: []
---

# Diagram Notation Guide

> [!info] What this is
> How to read every diagram in the vault: the shapes, the line styles, and the one color vocabulary all of them share. Each diagram also carries its own legend inside the image, so this note is the long form of those legends. The list of diagrams is [[Diagram Index]] and the entry point is [[Architecture Diagram Hub]].

## One color vocabulary

A color means the same thing in every diagram. Color is never the only carrier of meaning: the shape, the border style, or a text line says the same thing, so the diagrams still read in grayscale.

| Color | Meaning | Also marked by |
|---|---|---|
| Blue | A part of this system, or something open to every visitor | Rounded box; "Access: anyone" line on the capability map |
| Purple | A security control, or something that needs an account for some or all of it | Rounded box; an "Access" line that names an account |
| Orange | Run by the administrator, the maintainer, or a schedule | The word "run by" or "Starts" in the box text; a clock or plain start circle |
| Green | A data store | Cylinder shape |
| Yellow | A person or role | Stick figure, or a stadium (pill) shape in flowcharts |
| Grey with a dashed border | A system the project does not control | Dashed border |
| Grey band | A family of capabilities or a group of processes | Header strip with a label |

BPMN renders are black and white on a white card on purpose: BPMN carries its meaning in the shape. The white card keeps them legible in a dark theme.

## Flowcharts and C4

- Rectangle: a component or a step. Stadium (pill): a person, a bot, or an external party. Cylinder: a data store. Diamond: a decision.
- Solid arrow: a flow or a required call. Dashed arrow: optional, asynchronous, consent-gated, or best effort.
- C4 views use the C4 shapes: a person, the system in focus, an external system, a container, a database container, and a component. Each box shows its name, its type, and its technology. A legend box in each C4 view repeats this.

## Decision flowcharts

A pill with a yellow fill is the start, a pill with a green fill is an exit that succeeds, and a pill with a red fill is an exit that refuses or fails. A rounded blue box is a step, a purple box is a guard (a security check), and a white diamond is a decision whose outgoing arrows are all labelled. Each exit names what the caller sees, such as an HTTP status. Read them from the top. See Decision Logic Flowcharts.

## Data flow diagrams

Gane-Sarson style. A rounded box with a number such as 2.0 is a process, and a purple one is a security control. A box open on its right side and labelled D1, D2 and so on is a data store. A plain rectangle is an external entity: yellow for a person, grey and dashed for a system the project does not control. Every arrow carries the data that moves, not the action. A dashed purple rectangle is a trust boundary, and an arrow that crosses it is a crossing worth reviewing. See Data Flow Diagrams and Trust Boundary Views.

## Sequence diagrams

Boxes and stick figures along the top are participants. Time runs downward. A solid arrow is a request or call, numbered in order, and a dashed arrow is a reply. A thin bar on a lifeline is an activation, the time that participant is working. A framed block labelled alt, else or opt is a branch, and a note is a rule that applies to the span it covers.

## State diagrams

A rounded box is a state. An arrow is a transition labelled with its trigger, and a condition in brackets is a guard. The filled dot is the start and the ringed dot is the end. A note beside a state records a rule that holds in that state.

## Entity relationship diagrams

One box is one table or entity, coloured by domain role. A line is a relationship with crow foot ends: three prongs mean many, a bar means one, and a ring means optional. `PK`, `FK`, `UK` and `LK` mark primary, foreign, unique and logical keys. A logical link (`LK`) is drawn dashed: the value points at another row but the database does not enforce it. A slim dashed grey box is an entity owned by another diagram or by an external auth provider. The domain views are in `ER Data Model`; the complete schema is the generated `Schema ERD`.

## BPMN

- Circles are events: a thin circle starts a process, a thick circle ends it. A clock inside a start circle means a schedule starts it. An envelope means a message starts it.
- A rounded box is a task. A small person marker is a user task, done by a person. A small double circle on a task border is a boundary event, here an error.
- A diamond is a gateway. A cross inside means exactly one outgoing branch is taken, and every outgoing branch is labelled. A plus means the branches run in parallel.
- A pool or lane is a person or a system. A pool with no steps is an external participant.
- A solid arrow is sequence flow inside a pool. A dashed arrow with an open circle at its start is a message flow between participants. A dotted line is an association with a data store.
- A rounded box with a plus marker at the bottom is a collapsed sub-process, used on the landscape views.

## Draw.io views

The views under `docs/architecture/drawio/` use nested boxes for capability maps, stick figures and cylinders for the landscape, collapsed sub-process boxes for the process landscape, and the notations described above for flowcharts, data flows, entities, sequences and states. They are ordinary draw.io files: edit them in the draw.io desktop application, then render them with `brain docs diagram render`. The landscape views are described in Capability and Landscape Views. The render pipeline and the opaque light background are the same as for BPMN.

## Layout rules for every diagram

- A label sits where nothing else is: not over a shape, a flow, another label, and never on the title strip of a pool or lane. The title strip is 30 px wide, so start shapes at least 36 px to its right.
- Give every gateway and event label explicit bounds, on the side its flows do not use. Leaving it to the renderer puts it on a flow.
- A flow never passes through a shape it does not connect: route around it. Two shapes never overlap.
- Text fits its shape: about 6.4 px per character and 14 px per line. Enlarge the shape or shorten the name.
- Keep the number of links in an automatically laid out diagram (Mermaid ER, flowchart) low and the labels short, so two labels cannot stack. If two collide in the render, remove a link or shorten a label; do not accept the collision.
- `brain docs diagram check` enforces these (B8 to B15 for BPMN). Fix the source, never the rule.

## Mermaid grammar traps

- ER: the only key markers are `PK`, `FK` and `UK`, and Mermaid reads those words as markers wherever they stand, so no attribute may be named `PK`, `FK` or `UK`. A logical link is a comment, `TEXT source_file "LK"`, drawn with a dashed line (`..`); a solid line (`--`) is an enforced foreign key.
- Sequence: a semicolon ends the statement, in messages, notes and frame labels. A note over one participant is only that participant wide: span two or more.
- This Mermaid build cannot colour single ER entities (`classDef` and `style` fail). Set one colour for the whole diagram with an init directive, or author the ER in draw.io when colour per entity carries meaning.
- `brain docs diagram check` runs Mermaid's own parser (rule M0), so a source that draws nothing is reported before anyone looks for it.

## Colour and contrast

- The fill carries the meaning, from the palette above. The outline is dark (`#222222`).
- Text must reach a contrast of 4.5 against its fill (rules B16, D8 and M8). bpmn-js draws a task's text in its stroke colour, so a pastel stroke makes text unreadable: never use one.
- BPMN: set `bioc:fill` and `bioc:stroke="#222222"` on the shape; the rendered legend names every colour used. Mermaid flowchart: `classDef`. Mermaid sequence: `box rgb(...)` per group (yellow person, blue system, green data). Mermaid ER: one init theme for the whole diagram.

## Wrapper notes

Every authored diagram or process gets a wrapper note with this shape, in this order. `brain docs check` enforces it (D21 to D23).

1. Title, then straight after it an introduction of two to four sentences in plain B2 business English: what this makes possible for the stakeholder and why it matters. No code, paths, identifiers or backticks. Sentences average under 22 words and none runs past 32. There is no "What this unlocks" heading and no "who does what" opening.
2. `## What the diagram shows`: the mechanics step by step, each sentence ending with the code it came from as a backticked path:start-end.
3. `## Capability and related functionality`: the capability the diagram realises and how it relates to the routes, screens, use cases, rules and sibling diagrams around it, as wiki-links.
5. Frontmatter `use-cases: [UC-01]` (or `brain docs diagram new ... --use-case UC-01`) lists the use cases the diagram relates to. The workbench shows the diagram beside each of those use cases, expandable, with a link to its page. A use case with no related diagram shows nothing.
4. The code behind the diagram, as a table inside a folded callout (`> [!example]- Code references`). It is collapsed by default and the reader opens it on purpose.

## Adding a diagram

Pick the notation that matches the content: a capability map is nested boxes, a process with several actors is BPMN, a request across services is a sequence diagram, a lifecycle is a state diagram. Give it a legend that explains each shape, line style, and color it uses, then add it to a wrapper note and run `brain docs generate`; the entry point is [[Architecture Diagram Hub]]. Names of capabilities and actors come from the Capability Glossary.
