# ai-usage-cost dashboard

React 19 + TypeScript + Vite + Tailwind CSS 4 + Recharts. This is the source for the
SPA that `ai-usage-cost serve` hosts.

## Develop

Run the Python API first, then Vite:

```sh
# terminal 1 -- the backend on the port the dev proxy expects
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

`npm run build` writes into the Python package at
`../src/ai_usage_cost/web/dist/` (`emptyOutDir` is on). `create_app()` mounts that
directory at `/`, so the dashboard ships inside the wheel — rebuild it before
packaging or the server falls back to a "bundle not built" message.

`npm run typecheck` runs `tsc --noEmit` on its own.

## Layout

| Path | Holds |
|---|---|
| `src/api.ts` | fetch helpers and the TypeScript mirror of the FastAPI response models |
| `src/format.ts` | money / token / date formatting |
| `src/theme.ts` | light-dark mode (persisted to `localStorage`) and the chart palette |
| `src/components/` | card system, header, filter bar, KPI tiles, tables |
| `src/charts/` | Recharts wrappers and the shared tooltip/legend kit |

Colours live as CSS custom properties in `src/index.css`, defined once for light and
once under `.dark`; Tailwind utilities read them through `@theme inline`. Chart series
colours are handed out by a model's position in the unfiltered `/api/meta` list, so a
model keeps the same colour in every chart and filtering never repaints a series.
