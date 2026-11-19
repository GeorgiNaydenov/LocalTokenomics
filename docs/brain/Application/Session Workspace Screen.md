---
title: Session Workspace Screen
aliases: []
tags: [ui, reference, screen-map]
area: application
status: active
audience: internal
maturity: approved
confidence: inferred
covers: [web/src/*, web/src/design-system/*]
verified-against: 02d21a1926f6
chunk: ch-localtokenomics-web-src
approved-by: human
approved-at: '2026-11-19T07:31:30+00:00'
---

# Session Workspace Screen

The session workspace (web/src/SessionWorkspace.tsx): the session header with the outcome control, and the Summary, Trace, Economics and Context tabs. Its map is [[Session Workspace Screen Map]]; each numbered badge in the image is one row below.

## Screen map

| # | Element | What it does | Handler or target | State it depends on | Citation |
|---|---|---|---|---|---|
| 1 | `<h2` session name | Session name, or the sheet title when not docked. | - | - | [[web/src/SessionWorkspace.tsx]] `web/src/SessionWorkspace.tsx:502-502` |
| 2 | `<Button` Fullscreen | Toggles the docked panel to full screen. | `toggleFullscreen` | docked only | [[web/src/SessionWorkspace.tsx]] `web/src/SessionWorkspace.tsx:518-523` |
| 3 | `<Button` Close session | Closes the workspace. | `onClose` | docked only | [[web/src/SessionWorkspace.tsx]] `web/src/SessionWorkspace.tsx:527-527` |
| 4 | `<ToggleGroup` successful, partial, failed, abandoned, unrated | Picks the outcome and saves it at once. | `save` | - | [[web/src/SessionWorkspace.tsx]] `web/src/SessionWorkspace.tsx:306-312` |
| 5 | `<MetricInfo` rating meanings | Explains each outcome rating. | - | - | [[web/src/SessionWorkspace.tsx]] `web/src/SessionWorkspace.tsx:321-321` |
| 6 | `<Button` Notes and tags | Opens the notes and tags fields. | `setOpen` | - | [[web/src/SessionWorkspace.tsx]] `web/src/SessionWorkspace.tsx:330-330` |
| 7 | `<span` status | Saving, error, rated time or not rated yet, with the signals. | - | - | [[web/src/SessionWorkspace.tsx]] `web/src/SessionWorkspace.tsx:333-333` |
| 8 | `<Textarea` Notes | Notes saved when the field loses focus. | `saveEdited` | - | [[web/src/SessionWorkspace.tsx]] `web/src/SessionWorkspace.tsx:342-346` |
| 9 | `<Input` Tags, comma separated | Tags saved when the field loses focus. | `saveEdited` | - | [[web/src/SessionWorkspace.tsx]] `web/src/SessionWorkspace.tsx:352-356` |
| 10 | `<TabsTrigger` Summary, Trace, Economics, Context | Switches the tab; the Tabs value change marks it requested so its data loads. | - | - | [[web/src/SessionWorkspace.tsx]] `web/src/SessionWorkspace.tsx:547-547` |
| 11 | `<SummaryTab` Summary | Cost, token buckets, origin and raw log files. | - | - | [[web/src/SessionWorkspace.tsx]] `web/src/SessionWorkspace.tsx:555-555` |
| 12 | `if (!tokens) {` empty section | Summary shows an empty state when the client logs no tokens. | - | empty: `if (!tokens) {` | [[web/src/SessionWorkspace.tsx]] `web/src/SessionWorkspace.tsx:134-134` |
| 13 | `case 'loading':` loading section | A requested tab shows Loading until its data arrives. | - | loading: `case 'loading':` | [[web/src/SessionWorkspace.tsx]] `web/src/SessionWorkspace.tsx:387-387` |
| 14 | `case 'error':` error section | A failed tab shows the endpoint note and the error text. | - | error: `case 'error':` | [[web/src/SessionWorkspace.tsx]] `web/src/SessionWorkspace.tsx:389-389` |
| 15 | `<ResizeHandle` resize | Drag or arrow keys change the docked width. | `setWidth` | docked and not fullscreen | [[web/src/SessionWorkspace.tsx]] `web/src/SessionWorkspace.tsx:613-613` |
| 16 | `<Sheet` workspace sheet | The workspace as a sheet from the right when not docked. | `onClose` | - | [[web/src/SessionWorkspace.tsx]] `web/src/SessionWorkspace.tsx:620-620` |

### Conditional sections

- empty: `if (!tokens) {`, callout 12, [[web/src/SessionWorkspace.tsx]] `web/src/SessionWorkspace.tsx:134-134`
- loading: `case 'loading':`, callout 13, [[web/src/SessionWorkspace.tsx]] `web/src/SessionWorkspace.tsx:387-387`
- error: `case 'error':`, callout 14, [[web/src/SessionWorkspace.tsx]] `web/src/SessionWorkspace.tsx:389-389`

## Diagnosis

The reader rates the session, writes notes and tags, and switches tabs. A rating is saved the moment it is picked; notes and tags are saved on blur and only when changed `web/src/SessionWorkspace.tsx:312` `web/src/SessionWorkspace.tsx:291-294`.

What can go wrong:

- Saves are not sequenced: the toggle group stays enabled while saving, and a rating change and a notes blur can send two requests whose answers arrive in either order `web/src/SessionWorkspace.tsx:274-289` `web/src/SessionWorkspace.tsx:306-312`.
- A failed save keeps the draft and shows the error, but offers no retry other than editing again `web/src/SessionWorkspace.tsx:287` `web/src/SessionWorkspace.tsx:298`.
- A tab whose endpoint failed shows the error text with no retry; the load runs again only when the session changes `web/src/SessionWorkspace.tsx:389-390` `web/src/SessionWorkspace.tsx:95-108`.
- Escape closes the workspace only when docked; in the sheet the sheet handles closing `web/src/SessionWorkspace.tsx:486-493` `web/src/SessionWorkspace.tsx:620`.

States not handled: the status line shows a load error of the stored outcome, but the toggle still shows the fallback rating from the report as if it were stored `web/src/SessionWorkspace.tsx:270-272` `web/src/SessionWorkspace.tsx:299`.
