---
title: Offline card Screen
aliases: []
tags: [ui, reference, screen-map]
area: application
status: draft
audience: internal
maturity: draft
confidence: inferred
covers: [web/src/components/states.tsx]
chunk: ch-localtokenomics-web-src-components
---

# Offline card Screen

The full page card that the app shows when the local reader does not answer (`web/src/components/states.tsx:280-328`). Its map is [[Offline card screen map]]; each numbered badge in the image is one row below.

## Screen map

%% generated:screen-callouts start (do not edit; run brain docs generate) %%
| # | Element | What it does | Handler or target | State it depends on | Citation |
|---|---|---|---|---|---|
| 1 | `<p` No server on {host} | Eyebrow line in the destructive colour that names the host that did not answer. | - | `host` prop | `web/src/components/states.tsx:307-308` |
| 2 | `<h1` The dashboard lost the local reader. | Headline of the screen. It is the only heading, and the card sits alone in a full height grid. | - | - | `web/src/components/states.tsx:310-311` |
| 3 | `<p` Nothing was uploaded and nothing was lost | Reassures the reader that the last scan is still in the local SQLite store and that the view reconnects once the reader runs again. | - | - | `web/src/components/states.tsx:313-315` |
| 4 | `<CodeBlock` start command | Shows the command passed in as a prop, in a bordered block that wraps long lines. | `command` prop | `command` prop | `web/src/components/states.tsx:317-317` |
| 5 | `<Button` Retry connection | Asks the page to try the connection again by calling the function the page passed in. | `onRetry` | `onRetry` prop | `web/src/components/states.tsx:319-319` |
| 6 | `<Button` Copy command | Writes the command to the clipboard and, when that succeeds, flips the label to Copied for two seconds. | `copy` | `copied` state | `web/src/components/states.tsx:320-322` |
| 7 | `copied ? 'Copied' : 'Copy command'` copy feedback section | Switches the label of the copy button between its two texts. | - | copy feedback: `copied` | `web/src/components/states.tsx:321-321` |
%% generated:screen-callouts end %%

### Conditional sections

%% generated:screen-conditionals start (do not edit; run brain docs generate) %%
- copy feedback: `copied ? 'Copied' : 'Copy command'`, callout 7, `web/src/components/states.tsx:321-321`
%% generated:screen-conditionals end %%

## Diagnosis

The reader of this screen cannot do much: they can press Retry connection to ask the page to reconnect, or press Copy command to put the start command on the clipboard and then run it in a terminal by hand `web/src/components/states.tsx:319-322`.

What can go wrong: the clipboard write is wrapped in a promise whose rejection is swallowed, so on a browser that refuses clipboard access the button silently stays at Copy command and the reader gets no sign that nothing was copied `web/src/components/states.tsx:294-300`.

The reset timer of the Copied label is started with a bare timeout that is never cleared, so unmounting the card inside the two seconds leaves a state update pending `web/src/components/states.tsx:298-298`.

States the code does not handle: there is no loading or in progress state while a retry runs, so pressing Retry connection twice sends two reloads, and no state tells the reader that a retry just failed again `web/src/components/states.tsx:319-319`.

The text states that the last scan is still in the local SQLite store; that is a fixed sentence in the markup and the component never checks it `web/src/components/states.tsx:313-315`.

The page decides when this card shows, by looking for a fixed sentence in the error text, so a reworded error message would show the plain error card instead `web/src/App.tsx:251-251`.
