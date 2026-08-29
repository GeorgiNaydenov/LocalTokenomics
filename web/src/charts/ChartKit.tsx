import type { ReactNode } from 'react'

export interface TooltipRow {
  color: string
  label: string
  value: string
  title?: string
}

interface TooltipShellProps {
  title: string
  rows: TooltipRow[]
  footer?: ReactNode
}

/** Tooltip styled as a miniature of the card system, never the Recharts default. */
export function TooltipShell({ title, rows, footer }: TooltipShellProps) {
  return (
    <div className="pointer-events-none min-w-[168px] rounded-lg border border-border bg-popover p-2.5 text-[12.5px] shadow-lg">
      <p className="mb-1.5 font-semibold text-ink">{title}</p>
      <ul className="space-y-1">
        {rows.map((row) => (
          <li key={row.label} className="flex items-center gap-2">
            <span
              aria-hidden
              className="h-2.5 w-2.5 shrink-0 rounded-[3px]"
              style={{ background: row.color }}
            />
            <span className="min-w-0 flex-1 truncate text-ink-2">{row.label}</span>
            <span className="tnum shrink-0 font-medium text-ink" title={row.title}>
              {row.value}
            </span>
          </li>
        ))}
      </ul>
      {footer ? (
        <div className="mt-2 border-t border-border pt-1.5 text-[12px] text-ink-2">{footer}</div>
      ) : null}
    </div>
  )
}

export interface LegendItem {
  key: string
  label: string
  color: string
}

export function ChartLegend({ items }: { items: LegendItem[] }) {
  if (items.length < 2) return null
  return (
    <ul className="mb-3 flex flex-wrap gap-x-4 gap-y-1.5">
      {items.map((item) => (
        <li key={item.key} className="flex items-center gap-1.5 text-[12px] text-ink-2">
          <span
            aria-hidden
            className="h-2.5 w-2.5 shrink-0 rounded-[3px]"
            style={{ background: item.color }}
          />
          <span className="whitespace-nowrap">{item.label}</span>
        </li>
      ))}
    </ul>
  )
}

export function ChartEmpty({ height, message }: { height: number; message: string }) {
  return (
    <div
      className="flex items-center justify-center rounded-lg border border-dashed border-border text-[13px] text-muted"
      style={{ height }}
    >
      {message}
    </div>
  )
}
