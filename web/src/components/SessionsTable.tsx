import { useMemo, useState } from 'react'
import type { Report, SessionRow } from '../api'
import { formatCount, formatExact, formatMoney, formatTimestamp, formatTokens } from '../format'
import type { ThemeMode } from '../theme'
import { seriesColor } from '../theme'
import { Button, Swatch } from './Controls'

type SortKey = 'cost' | 'tokens' | 'started' | 'events'

interface SessionsTableProps {
  report: Report
  toolLabel: (id: string) => string
  modelLabel: (model: string) => string
  modelIndex: (model: string) => number
  toolIndex: (tool: string) => number
  mode: ThemeMode
}

const VISIBLE = 50

const COLUMNS: { key: SortKey | null; label: string; align: 'left' | 'right' }[] = [
  { key: null, label: 'Project', align: 'left' },
  { key: null, label: 'Tool', align: 'left' },
  { key: null, label: 'Models', align: 'left' },
  { key: 'started', label: 'Started', align: 'left' },
  { key: 'events', label: 'Requests', align: 'right' },
  { key: 'tokens', label: 'Tokens', align: 'right' },
  { key: 'cost', label: 'Cost', align: 'right' },
]

export function SessionsTable({
  report,
  toolLabel,
  modelLabel,
  modelIndex,
  toolIndex,
  mode,
}: SessionsTableProps) {
  const [sort, setSort] = useState<SortKey>('cost')
  const [descending, setDescending] = useState(true)
  const [showAll, setShowAll] = useState(false)

  const sorted = useMemo(() => {
    const rows = [...report.sessions]
    rows.sort((a, b) => compare(a, b, sort) * (descending ? -1 : 1))
    return rows
  }, [report.sessions, sort, descending])

  const visible = showAll ? sorted : sorted.slice(0, VISIBLE)

  if (sorted.length === 0) {
    return (
      <p className="rounded-lg border border-dashed border-border px-4 py-8 text-center text-[13px] text-muted">
        No sessions match these filters.
      </p>
    )
  }

  const onSort = (key: SortKey) => {
    if (key === sort) setDescending((value) => !value)
    else {
      setSort(key)
      setDescending(true)
    }
  }

  return (
    <>
      <div className="thin-scroll max-h-[520px] overflow-auto rounded-lg border border-border">
        <table className="w-full min-w-[820px] border-collapse text-[13px]">
          <thead className="sticky top-0 z-10 bg-surface-2">
            <tr className="text-[11px] tracking-wide text-muted uppercase">
              {COLUMNS.map((column) => (
                <th
                  key={column.label}
                  scope="col"
                  aria-sort={
                    column.key === sort ? (descending ? 'descending' : 'ascending') : undefined
                  }
                  className={`border-b border-border px-3 py-2.5 font-medium ${
                    column.align === 'right' ? 'text-right' : 'text-left'
                  }`}
                >
                  {column.key ? (
                    <button
                      type="button"
                      onClick={() => onSort(column.key as SortKey)}
                      className={`inline-flex items-center gap-1 hover:text-ink ${
                        column.key === sort ? 'text-ink' : ''
                      }`}
                    >
                      {column.label}
                      <span aria-hidden className={column.key === sort ? '' : 'opacity-0'}>
                        {descending ? '▾' : '▴'}
                      </span>
                    </button>
                  ) : (
                    column.label
                  )}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {visible.map((session) => (
              <tr key={session.session_id} className="border-b border-border last:border-0">
                <td
                  className="max-w-[180px] truncate px-3 py-2.5 font-medium text-ink"
                  title={session.project ?? 'unattributed'}
                >
                  {session.project ?? <span className="text-muted">—</span>}
                </td>
                <td className="px-3 py-2.5 whitespace-nowrap text-ink-2">
                  <span className="inline-flex items-center gap-1.5">
                    <Swatch color={seriesColor(toolIndex(session.tool), mode)} />
                    {toolLabel(session.tool)}
                  </span>
                </td>
                <td className="px-3 py-2.5">
                  <span className="flex flex-wrap items-center gap-x-2.5 gap-y-1">
                    {session.models.map((model) => (
                      <span
                        key={model}
                        className="inline-flex items-center gap-1.5 whitespace-nowrap text-ink-2"
                      >
                        <Swatch color={seriesColor(modelIndex(model), mode)} />
                        {modelLabel(model)}
                      </span>
                    ))}
                  </span>
                </td>
                <td className="tnum px-3 py-2.5 whitespace-nowrap text-ink-2">
                  {formatTimestamp(session.started)}
                </td>
                <td className="tnum px-3 py-2.5 text-right text-ink-2">
                  {formatCount(session.events)}
                </td>
                <td
                  className="tnum px-3 py-2.5 text-right text-ink-2"
                  title={formatExact(session.tokens)}
                >
                  {formatTokens(session.tokens)}
                </td>
                <td className="tnum px-3 py-2.5 text-right font-semibold text-ink">
                  {formatMoney(session.cost)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {sorted.length > VISIBLE ? (
        <div className="mt-3 flex items-center gap-3">
          <Button onClick={() => setShowAll((value) => !value)}>
            {showAll ? `Show top ${VISIBLE}` : `Show all ${formatCount(sorted.length)} sessions`}
          </Button>
          <span className="text-[12px] text-muted">
            Showing {formatCount(visible.length)} of {formatCount(sorted.length)}.
          </span>
        </div>
      ) : null}
    </>
  )
}

function compare(a: SessionRow, b: SessionRow, key: SortKey): number {
  if (key === 'started') return a.started < b.started ? -1 : a.started > b.started ? 1 : 0
  return a[key] - b[key]
}
