# ai-usage-cost dashboard

React 19 + TypeScript + Vite. This is the source for the SPA that `ai-usage-cost serve`
hosts.

Styling comes from the vendored Agentic AI Library design system under `src/ds/` rather
than a utility framework: colors, type, spacing, and the core/forms/patterns component
sheets are copied in as plain CSS, and the app's own local classes sit alongside them in
`src/index.css`. The design system's content, data-viz, and auth sheets are deliberately
left out, since this dashboard uses none of their classes and vendoring them would only
add dead weight to every build.

Charts are hand-rolled SVG, not a charting library: the stacked bar chart's geometry
(bar layout, the mean line, the peak callout) is a direct port of the design's own chart
math in `src/chart.ts`, driven by real data instead of the design's synthetic sample.

Fonts (Lexend, Inter, Geist Mono) are self-hosted as `.woff2` files under `src/ds/fonts/`
and loaded with `@font-face`, not from a CDN, so the running dashboard makes no network
requests of any kind, matching the tool's offline, read-only design.

## Develop

Run the Python API first, then Vite:

```sh
# terminal 1: the backend on the port the dev proxy expects
ai-usage-cost serve --no-open --port 8420

# terminal 2
cd web
npm install
npm run dev          # http://localhost:5173, /api proxied to 127.0.0.1:8420
```

## Build

```sh
npm run build        # tsc --noEmit, then vite build
```

`npm run build` writes into the Python package at `../src/ai_usage_cost/web/dist/`
(`emptyOutDir` is on). `create_app()` mounts that directory at `/`, so the dashboard
ships inside the wheel. Rebuild it before packaging, or the server falls back to a
"bundle not built" message.

`npm run typecheck` runs `tsc --noEmit` on its own.

## Layout

| Path | Holds |
|---|---|
| `src/ds/` | the vendored design system: tokens, core/forms/patterns component CSS, self-hosted fonts |
| `src/api.ts` | fetch helpers and the TypeScript mirror of the FastAPI response models |
| `src/format.ts` | money, token, count, and date formatting |
| `src/theme.ts` | the `data-theme` light/dark store (persisted to `localStorage`) and the chart color constants |
| `src/chart.ts` | the pure, JSX-free time-chart and sparkline geometry |
| `src/App.tsx` | app shell: all state, the tab switch, the filter rail and main layout, the drawer |
| `src/Header.tsx`, `src/FilterRail.tsx` | the sticky header and the filter rail |
| `src/Overview.tsx`, `src/Sessions.tsx`, `src/Sources.tsx`, `src/Pricing.tsx` | the four dashboard tabs |
| `src/SessionWorkspace.tsx` | the session workspace: summary, trace, economics and context tabs, and the outcome control |
| `src/TraceTab.tsx` | the chronological timeline and agent tree |
| `src/EconomicsTab.tsx` | tokens, cost and time per turn, model and tool |
| `src/ContextTab.tsx` | context-window occupancy per model call |

Colors live as CSS custom properties from the design system, defined once for light and
once under `[data-theme="dark"]`. Series colors and per-state colors are named constants
in `theme.ts` that reference those custom properties directly, so a value stays in sync
with the active theme without any JavaScript recomputation.
