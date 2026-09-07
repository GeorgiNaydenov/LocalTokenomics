import { useMemo, useState } from 'react'
import type { Report, SessionRow } from '../api'
import { formatCount, formatExact, formatMoney, formatTimestamp, formatTokens } from '../format'
import type { ThemeMode } from '../theme'
import { seriesColor } from '../theme'
import { Button, Swatch } from './Controls'

type SortKey = 'cost' | 'tokens' | 'started' | 'requests'

interface SessionsTableProps {
  report: Report
  clientLabel: (id: string) => string
  clientIndex: (id: string) => number
  providerLabel: (id: string) => string
  providerIndex: (id: string) => number
  modelLabel: (model: string) => string
  modelIndex: (model: string) => number
  mode: ThemeMode
}

const VISIBLE = 50

const COLUMNS: { key: SortKey | null; label: string; align: 'left' | 'right' }[] = [
  { key: null, label: 'Project', align: 'left' },
  { key: null, label: 'Client', align: 'left' },
  { key: null, label: 'Provider', align: 'left' },
  { key: null, label: 'Models', align: 'left' },
  { key: 'started', label: 'Started', align: 'left' },
  { key: 'requests', label: 'Requests', align: 'right' },
  { key: 'tokens', label: 'Tokens', align: 'right' },
  { key: 'cost', label: 'Cost', align: 'right' },
]

function totalTokens(row: SessionRow): number | null {
  if (row.input_tokens === null && row.output_tokens === null) return null
  return (row.input_tokens ?? 0) + (row.output_tokens ?? 0)
}

function compare(a: SessionRow, b: SessionRow, key: SortKey): number {
  if (key === 'started') return a.start_time < b.start_time ? -1 : a.start_time > b.start_time ? 1 : 0
  if (key === 'requests') return a.request_count - b.request_count
  if (key === 'cost') return (a.cost ?? -1) - (b.cost ?? -1)
  return (totalTokens(a) ?? -1) - (totalTokens(b) ?? -1)
}

function CostCell({ row }: { row: SessionRow }) {
  if (row.cost_state === 'priced' && row.cost !== null) {
    return <span className="font-semibold text-ink">{formatMoney(row.cost)}</span>
  }
  if (row.cost_state === 'free') {
    return <span className="text-ink-2">Free (local)</span>
  }
  if (row.cost_state === 'unpriced') {
    return (
      <span className="text-ink-2" title="No rate entry for this model">
        unpriced
      </span>
    )
  }
  return <span className="text-muted">no usage data</span>
}

export function SessionsTable({
  report,
  clientLabel,
  clientIndex,
  providerLabel,
  providerIndex,
  modelLabel,
  modelIndex,
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
        <table className="w-full min-w-[900px] border-collapse text-[13px]">
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
              <tr key={`${session.source}:${session.session_id}`} className="border-b border-border last:border-0">
                <td
                  className="max-w-[180px] truncate px-3 py-2.5 font-medium text-ink"
                  title={session.project ?? 'unattributed'}
                >
                  {session.project ?? <span className="text-muted">—</span>}
                </td>
                <td className="px-3 py-2.5 whitespace-nowrap text-ink-2">
                  <span className="inline-flex items-center gap-1.5">
                    <Swatch color={seriesColor(clientIndex(session.client), mode)} />
                    {clientLabel(session.client)}
                  </span>
                </td>
                <td className="px-3 py-2.5 whitespace-nowrap text-ink-2">
                  <span className="inline-flex items-center gap-1.5">
                    <Swatch color={seriesColor(providerIndex(session.provider), mode)} />
                    {providerLabel(session.provider)}
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
                  {formatTimestamp(session.start_time)}
                </td>
                <td className="tnum px-3 py-2.5 text-right text-ink-2">
                  {formatCount(session.request_count)}
                </td>
                <td
                  className="tnum px-3 py-2.5 text-right text-ink-2"
                  title={totalTokens(session) !== null ? formatExact(totalTokens(session) as number) : undefined}
                >
                  {totalTokens(session) !== null ? (
                    formatTokens(totalTokens(session) as number)
                  ) : (
                    <span className="text-muted">—</span>
                  )}
                </td>
                <td className="tnum px-3 py-2.5 text-right">
                  <CostCell row={session} />
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
