---
title: App Screen
aliases: []
tags: [ui, reference, screen-map]
area: application
status: draft
audience: internal
maturity: draft
confidence: inferred
covers: [web/src/*, web/src/design-system/*]
verified-against: 5796e68c0471
chunk: ch-localtokenomics-web-src
---

# App Screen

The application shell (web/src/App.tsx with web/src/Header.tsx and web/src/FilterRail.tsx): header, filter rail, the active view and the session workspace. Its map is [[App Screen Map]]; each numbered badge in the image is one row below.

## Screen map

| # | Element | What it does | Handler or target | State it depends on | Citation |
|---|---|---|---|---|---|
| 1 | `isOffline` error section | Replaces the whole page with the offline card when the server cannot be reached. | - | error: `isOffline` | [[web/src/App.tsx]] `web/src/App.tsx:253-253` |
| 2 | `<OfflineCard` Retry | Offline card with the command to start the server and a retry button. | `setReload` | - | [[web/src/App.tsx]] `web/src/App.tsx:255-258` |
| 3 | `if (loading)` loading section | Shows a loading line until the first report has settled. | - | loading: `if (loading)` | [[web/src/App.tsx]] `web/src/App.tsx:263-263` |
| 4 | `if (error)` error section | Replaces the whole page with an error card for any other failure. | - | error: `if (error)` | [[web/src/App.tsx]] `web/src/App.tsx:271-271` |
| 5 | `<button` Overview, Sessions, Sources, Models and pricing | Tab strip that switches the active view. | `onSelectView` | - | [[web/src/Header.tsx]] `web/src/Header.tsx:79-84` |
| 6 | `<Button` Filters | Opens the filter sheet on screens narrower than the large breakpoint. | `onOpenRail` | - | [[web/src/Header.tsx]] `web/src/Header.tsx:98-98` |
| 7 | `<button` stale.text | Rate age notice that opens Models and pricing. | `onSelectView` | shown only while the rates are old | [[web/src/Header.tsx]] `web/src/Header.tsx:105-107` |
| 8 | `<Button` Rescan logs | Asks the server to rescan the log files. | `onRescan` | - | [[web/src/Header.tsx]] `web/src/Header.tsx:128-128` |
| 9 | `<Button` Switch theme | Toggles light and dark mode. | `onToggleTheme` | - | [[web/src/Header.tsx]] `web/src/Header.tsx:131-131` |
| 10 | `<SearchField` Search sessions, models, repos | Free text search over the slice. | `onChange` | - | [[web/src/FilterRail.tsx]] `web/src/FilterRail.tsx:298-300` |
| 11 | `<button` Saved views | Chips that apply a preset patch to the query. | `onApply` | - | [[web/src/FilterRail.tsx]] `web/src/FilterRail.tsx:190-194` |
| 12 | `<ChipRow` Range presets | Preset date ranges ending today. | `onChange` | - | [[web/src/FilterRail.tsx]] `web/src/FilterRail.tsx:311-317` |
| 13 | `<DateRange` since, until | Exact start and end day, bounded by the first and last logged day. | `onChange` | - | [[web/src/FilterRail.tsx]] `web/src/FilterRail.tsx:320-325` |
| 14 | `<FacetGroup` Cost state | Toggles cost states in the query. | `onToggleFacet` | - | [[web/src/FilterRail.tsx]] `web/src/FilterRail.tsx:334-338` |
| 15 | `<FacetGroup` Outcome | Toggles outcome ratings in the query. | `toggleOutcome` | - | [[web/src/FilterRail.tsx]] `web/src/FilterRail.tsx:342-346` |
| 16 | `<FacetGroup` Clients | Toggles clients, the most recently active first. | `onToggleFacet` | - | [[web/src/FilterRail.tsx]] `web/src/FilterRail.tsx:354-358` |
| 17 | `<FacetGroup` Models | Toggles models used in the recency window. | `onToggleFacet` | - | [[web/src/FilterRail.tsx]] `web/src/FilterRail.tsx:380-384` |
| 18 | `<FacetGroup` Projects | Toggles projects used in the recency window. | `onToggleFacet` | - | [[web/src/FilterRail.tsx]] `web/src/FilterRail.tsx:406-410` |
| 19 | `<SwitchRow` Include subagent requests | Switch that keeps or drops sidechain requests. | `onChange` | - | [[web/src/FilterRail.tsx]] `web/src/FilterRail.tsx:431-434` |
| 20 | `<SwitchRow` Traced only | Switch that keeps only traced sessions. | `onChange` | - | [[web/src/FilterRail.tsx]] `web/src/FilterRail.tsx:436-439` |
| 21 | `<SwitchRow` Errors only | Switch that keeps only sessions with errors. | `onChange` | - | [[web/src/FilterRail.tsx]] `web/src/FilterRail.tsx:441-444` |
| 22 | `<Button` Clear all filters | Resets the query to the whole logged range. | `onReset` | shown only while a filter differs from the reset | [[web/src/FilterRail.tsx]] `web/src/FilterRail.tsx:449-449` |
| 23 | `<Sheet` Filters | The same rail as a sheet from the left on narrow screens. | `onClose` | - | [[web/src/FilterRail.tsx]] `web/src/FilterRail.tsx:486-489` |
| 24 | `<FilterChips` active filters | One removable chip per active filter. | `activeChips` | - | [[web/src/App.tsx]] `web/src/App.tsx:327-327` |
| 25 | `view === 'overview' && report && meta` view section | Shows the Overview view. | - | view: `view === 'overview' && report && meta` | [[web/src/App.tsx]] `web/src/App.tsx:330-330` |
| 26 | `view === 'sessions' && report` view section | Shows the Sessions view. | - | view: `view === 'sessions' && report` | [[web/src/App.tsx]] `web/src/App.tsx:333-333` |
| 27 | `view === 'sources' && report && meta` view section | Shows the Sources view. | - | view: `view === 'sources' && report && meta` | [[web/src/App.tsx]] `web/src/App.tsx:336-336` |
| 28 | `view === 'pricing' && report && rates` view section | Shows the Models and pricing view. | - | view: `view === 'pricing' && report && rates` | [[web/src/App.tsx]] `web/src/App.tsx:337-337` |
| 29 | `<SessionWorkspace` open session | Session workspace docked at the right or as a sheet. | `closeWorkspace` | shown while a session is open and still in the report | [[web/src/App.tsx]] `web/src/App.tsx:343-351` |

### Conditional sections

- error: `isOffline`, callout 1, [[web/src/App.tsx]] `web/src/App.tsx:253-253`
- loading: `if (loading)`, callout 3, [[web/src/App.tsx]] `web/src/App.tsx:263-263`
- error: `if (error)`, callout 4, [[web/src/App.tsx]] `web/src/App.tsx:271-271`
- view: `view === 'overview' && report && meta`, callout 25, [[web/src/App.tsx]] `web/src/App.tsx:330-330`
- view: `view === 'sessions' && report`, callout 26, [[web/src/App.tsx]] `web/src/App.tsx:333-333`
- view: `view === 'sources' && report && meta`, callout 27, [[web/src/App.tsx]] `web/src/App.tsx:336-336`
- view: `view === 'pricing' && report && rates`, callout 28, [[web/src/App.tsx]] `web/src/App.tsx:337-337`

## Diagnosis

The reader picks a view, narrows the slice and opens sessions here. Every filter change patches one query object, and each new query fetches a new report while the previous request is aborted `web/src/App.tsx:147-149` `web/src/App.tsx:183-201`.

What can go wrong:

- Any failed report request after the first load sets the same error that the full page error card reads, so a single failed refetch replaces the whole dashboard and the card is rendered with no retry action `web/src/App.tsx:191-194` `web/src/App.tsx:271-276`.
- The rescan button stays enabled while a scan runs; only its label changes, so a second press starts a second refresh `web/src/Header.tsx:128-130` `web/src/App.tsx:211-222`.
- Opening a session from the table looks the row up by session id alone, so two sources that share a session id open the first match `web/src/App.tsx:284-288`.
- On a large screen the rail is hidden while a workspace is open and the Filters button is hidden at that breakpoint too, so the filters cannot be reached until the workspace is closed `web/src/App.tsx:317` `web/src/FilterRail.tsx:477-481` `web/src/Header.tsx:98`.

States not handled: a workspace whose session drops out of the report after a filter change disappears without a message while its key stays set `web/src/App.tsx:280-282` `web/src/App.tsx:342`.
