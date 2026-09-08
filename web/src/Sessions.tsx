import { useMemo, useState, useSyncExternalStore } from 'react'
import type { ChangeEvent, JSX } from 'react'
import type { OutcomeLabel, Report, SessionRow } from './api'
import { formatClock, formatCount, formatDayShort, formatMoney, formatTokens, toDayString } from './format'
import { STATE_COLOR } from './theme'

type SortKey =
  | 'state'
  | 'outcome'
  | 'id'
  | 'client'
  | 'model'
  | 'project'
  | 'start'
  | 'requests'
  | 'errors'
  | 'tokens'
  | 'cost'
type SortDir = 'asc' | 'desc'

const SHOWN_LIMIT = 120

const COLUMNS: { key: SortKey; label: string; align: 'left' | 'right' }[] = [
  { key: 'state', label: 'State', align: 'left' },
  { key: 'outcome', label: 'Outcome', align: 'left' },
  { key: 'id', label: 'Session', align: 'left' },
  { key: 'client', label: 'Client', align: 'left' },
  { key: 'model', label: 'Model', align: 'left' },
  { key: 'project', label: 'Project', align: 'left' },
  { key: 'start', label: 'Started', align: 'left' },
  { key: 'requests', label: 'Req', align: 'right' },
  { key: 'errors', label: 'Errors', align: 'right' },
  { key: 'tokens', label: 'Tokens', align: 'right' },
  { key: 'cost', label: 'Cost', align: 'right' },
]

const OUTCOME_COLOR: Record<OutcomeLabel, string> = {
  successful: 'var(--success)',
  partial: 'var(--bubble-c-3)',
  failed: 'var(--rose)',
  abandoned: 'var(--bubble-c-4)',
  unrated: 'var(--fg-faint)',
}

const SORT_OPTIONS: { value: string; key: SortKey; dir: SortDir; label: string }[] = [
  { value: 'cost:desc', key: 'cost', dir: 'desc', label: 'Cost, high to low' },
  { value: 'cost:asc', key: 'cost', dir: 'asc', label: 'Cost, low to high' },
  { value: 'tokens:desc', key: 'tokens', dir: 'desc', label: 'Tokens, high to low' },
  { value: 'start:desc', key: 'start', dir: 'desc', label: 'Newest first' },
  { value: 'start:asc', key: 'start', dir: 'asc', label: 'Oldest first' },
  { value: 'requests:desc', key: 'requests', dir: 'desc', label: 'Most requests' },
  { value: 'errors:desc', key: 'errors', dir: 'desc', label: 'Most errors' },
  { value: 'state:asc', key: 'state', dir: 'asc', label: 'Cost state' },
  { value: 'outcome:asc', key: 'outcome', dir: 'asc', label: 'Outcome A to Z' },
  { value: 'project:asc', key: 'project', dir: 'asc', label: 'Project A to Z' },
]

const PHONE_QUERY = '(max-width: 639px)'

function subscribeToPhoneWidth(listener: () => void): () => void {
  const media = window.matchMedia(PHONE_QUERY)
  media.addEventListener('change', listener)
  return () => media.removeEventListener('change', listener)
}

function isPhoneWidth(): boolean {
  return window.matchMedia(PHONE_QUERY).matches
}

function useIsPhone(): boolean {
  return useSyncExternalStore(subscribeToPhoneWidth, isPhoneWidth, () => false)
}

function modelLabel(modelId: string, report: Report): string {
  return report.by_model.find((bucket) => bucket.key === modelId)?.label ?? modelId
}

function startLabel(startTime: string): string {
  return `${formatDayShort(toDayString(startTime) ?? startTime)} ${formatClock(startTime)}`
}

function sortValue(row: SessionRow, key: SortKey, report: Report): string | number {
  switch (key) {
    case 'state':
      return row.cost_state
    case 'outcome':
      return row.outcome
    case 'errors':
      return row.error_count
    case 'id':
      return row.session_id
    case 'client':
      return row.client
    case 'model':
      return modelLabel(row.models[0], report)
    case 'project':
      return row.project ?? ''
    case 'start':
      return row.start_time
    case 'requests':
      return row.request_count
    case 'tokens':
      return row.tokens ? row.tokens.total : -1
    case 'cost':
      return row.cost ? row.cost.total : -1
  }
}

function compare(a: string | number, b: string | number): number {
  if (typeof a === 'string' || typeof b === 'string') return String(a).localeCompare(String(b))
  return a - b
}

function TracedDot({ traced }: { traced: boolean }) {
  return (
    <span
      title={traced ? 'trace spans captured for this session' : 'no trace spans captured for this session'}
      style={{
        width: 7,
        height: 7,
        flex: 'none',
        borderRadius: '50%',
        boxSizing: 'border-box',
        background: traced ? 'var(--accent)' : 'transparent',
        border: traced ? 'none' : '1px solid var(--border-strong)',
      }}
    />
  )
}

function StateCell({ row }: { row: SessionRow }) {
  return (
    <span style={{ display: 'inline-flex', alignItems: 'center', gap: 6 }}>
      <span style={{ width: 7, height: 7, flex: 'none', background: STATE_COLOR[row.cost_state] }} />
      <span className="num" style={{ fontSize: 10, color: 'var(--fg-muted)' }}>
        {row.cost_state}
      </span>
      <TracedDot traced={row.traced} />
    </span>
  )
}

function OutcomeCell({ outcome }: { outcome: OutcomeLabel }) {
  return (
    <span className="num" style={{ fontSize: 10, color: OUTCOME_COLOR[outcome] }}>
      {outcome}
    </span>
  )
}

function ModelCell({ row, report }: { row: SessionRow; report: Report }) {
  const extra = row.models.length - 1
  return (
    <span title={row.models.join(', ')}>
      {modelLabel(row.models[0], report)}
      {extra > 0 && (
        <span style={{ marginLeft: 6, fontSize: 10, color: 'var(--fg-faint)' }} className="num">
          +{extra}
        </span>
      )}
    </span>
  )
}

function TokensCell({ row, maxTokens }: { row: SessionRow; maxTokens: number }) {
  if (!row.tokens) {
    return (
      <span className="num" style={{ display: 'block', textAlign: 'right', color: 'var(--fg-faint)' }}>
        n/a
      </span>
    )
  }
  const pct = (row.tokens.total / maxTokens) * 100
  return (
    <span style={{ display: 'flex', alignItems: 'center', gap: 7, justifyContent: 'flex-end' }}>
      <span className="num" style={{ color: 'var(--fg-muted)' }}>
        {formatTokens(row.tokens.total)}
      </span>
      <span style={{ width: 52, height: 8, background: 'var(--bg-muted)', flex: 'none', display: 'inline-block' }}>
        <span style={{ display: 'block', height: '100%', width: `${pct}%`, background: STATE_COLOR[row.cost_state] }} />
      </span>
    </span>
  )
}

function SessionCard({
  row,
  report,
  onOpen,
}: {
  row: SessionRow
  report: Report
  onOpen: () => void
}) {
  const extra = row.models.length - 1
  return (
    <div className="row-card" onClick={onOpen} style={{ cursor: 'pointer' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
        <StateCell row={row} />
        <span className="num" style={{ marginLeft: 'auto', color: 'var(--fg-strong)' }}>
          {row.session_id}
        </span>
      </div>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 8 }}>
        <OutcomeCell outcome={row.outcome} />
        <span className="num" style={{ fontSize: 10, color: row.error_count > 0 ? 'var(--rose)' : 'var(--fg-faint)' }}>
          {`${formatCount(row.error_count)} errors`}
        </span>
      </div>
      <div style={{ fontSize: 11.5, color: 'var(--fg-strong)' }} title={row.models.join(', ')}>
        {modelLabel(row.models[0], report)}
        {extra > 0 && ` +${extra}`}
      </div>
      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 11, color: 'var(--fg-muted)' }}>
        <span>{row.client}</span>
        <span>{row.project ?? '(no project)'}</span>
      </div>
      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 10.5, color: 'var(--fg-faint)' }}>
        <span className="num">{startLabel(row.start_time)}</span>
        <span className="num">{formatCount(row.request_count)} req</span>
      </div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span className="num" style={{ fontSize: 11, color: 'var(--fg-muted)' }}>
          {row.tokens ? formatTokens(row.tokens.total) : 'n/a'}
        </span>
        <span
          className="num"
          style={{ fontWeight: 600, color: row.cost ? 'var(--fg-strong)' : 'var(--fg-faint)' }}
        >
          {row.cost ? formatMoney(row.cost.total) : 'n/a'}
        </span>
      </div>
    </div>
  )
}

export default function Sessions(props: {
  report: Report
  onOpenSession: (sessionId: string) => void
}): JSX.Element {
  const { report } = props
  const [sortKey, setSortKey] = useState<SortKey>('cost')
  const [sortDir, setSortDir] = useState<SortDir>('desc')
  const isPhone = useIsPhone()

  const sorted = useMemo(() => {
    const copy = [...report.sessions]
    copy.sort((a, b) => {
      const cmp = compare(sortValue(a, sortKey, report), sortValue(b, sortKey, report))
      return sortDir === 'desc' ? -cmp : cmp
    })
    return copy
  }, [report, sortKey, sortDir])

  const shown = sorted.slice(0, SHOWN_LIMIT)
  const maxTokens = Math.max(...shown.map((row) => (row.tokens ? row.tokens.total : 0)), 1)

  const onHeaderSort = (key: SortKey) => {
    if (sortKey === key) {
      setSortDir(sortDir === 'desc' ? 'asc' : 'desc')
    } else {
      setSortKey(key)
      setSortDir('desc')
    }
  }

  const onSortSelect = (e: ChangeEvent<HTMLSelectElement>) => {
    const option = SORT_OPTIONS.find((o) => o.value === e.target.value)
    if (!option) return
    setSortKey(option.key)
    setSortDir(option.dir)
  }

  const title = `${formatCount(report.sessions.length)} sessions, sorted by ${sortKey} ${
    sortDir === 'desc' ? 'high to low' : 'low to high'
  }`

  return (
    <section className="panel">
      <div className="panel__head">
        <div>
          <p className="lbl" style={{ color: 'var(--accent)' }}>
            Sessions
          </p>
          <h2 className="panel__title">{title}</h2>
        </div>
        <div style={{ marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: 8 }}>
          <span className="lbl">Sort</span>
          <select className="sort-select" value={`${sortKey}:${sortDir}`} onChange={onSortSelect}>
            {SORT_OPTIONS.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      {isPhone ? (
        <div
          className="panel__body sessions-cards-wrap"
          style={{ display: 'flex', flexDirection: 'column', gap: 8 }}
        >
          {shown.map((row) => (
            <SessionCard
              key={row.session_id}
              row={row}
              report={report}
              onOpen={() => props.onOpenSession(row.session_id)}
            />
          ))}
        </div>
      ) : (
        <div className="sessions-table-wrap" style={{ overflowX: 'auto' }}>
          <table className="data-table">
            <thead>
              <tr>
                {COLUMNS.map((column) => (
                  <th
                    key={column.key}
                    style={{
                      padding: 0,
                      background: 'var(--bg-muted)',
                      boxShadow: 'inset 0 -1px 0 var(--border)',
                      textAlign: column.align,
                    }}
                  >
                    <button
                      type="button"
                      className="sortbtn"
                      onClick={() => onHeaderSort(column.key)}
                      style={{
                        width: '100%',
                        padding: '8px 10px',
                        border: 0,
                        background: 'none',
                        cursor: 'pointer',
                        fontFamily: 'var(--font-sans)',
                        fontSize: 9.5,
                        fontWeight: 700,
                        letterSpacing: '0.12em',
                        textTransform: 'uppercase',
                        color: sortKey === column.key ? 'var(--accent)' : 'var(--fg-muted)',
                        textAlign: column.align,
                      }}
                    >
                      {column.label}
                      <span className="num" style={{ marginLeft: 4 }}>
                        {sortKey === column.key ? (sortDir === 'desc' ? '▾' : '▴') : ''}
                      </span>
                    </button>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {shown.map((row) => (
                <tr
                  key={row.session_id}
                  className="row-hit"
                  onClick={() => props.onOpenSession(row.session_id)}
                  style={{ cursor: 'pointer' }}
                >
                  <td style={{ padding: '7px 10px', boxShadow: 'inset 0 -1px 0 var(--border)' }}>
                    <StateCell row={row} />
                  </td>
                  <td style={{ padding: '7px 10px', boxShadow: 'inset 0 -1px 0 var(--border)' }}>
                    <OutcomeCell outcome={row.outcome} />
                  </td>
                  <td
                    className="num"
                    style={{ padding: '7px 10px', color: 'var(--fg-strong)', boxShadow: 'inset 0 -1px 0 var(--border)' }}
                  >
                    {row.session_id}
                  </td>
                  <td style={{ padding: '7px 10px', color: 'var(--fg-muted)', boxShadow: 'inset 0 -1px 0 var(--border)' }}>
                    {row.client}
                  </td>
                  <td style={{ padding: '7px 10px', color: 'var(--fg-muted)', boxShadow: 'inset 0 -1px 0 var(--border)' }}>
                    <ModelCell row={row} report={report} />
                  </td>
                  <td style={{ padding: '7px 10px', color: 'var(--fg-muted)', boxShadow: 'inset 0 -1px 0 var(--border)' }}>
                    {row.project ?? '(no project)'}
                  </td>
                  <td
                    className="num"
                    style={{ padding: '7px 10px', color: 'var(--fg-faint)', boxShadow: 'inset 0 -1px 0 var(--border)' }}
                  >
                    {startLabel(row.start_time)}
                  </td>
                  <td
                    className="num"
                    style={{
                      padding: '7px 10px',
                      textAlign: 'right',
                      color: 'var(--fg-muted)',
                      boxShadow: 'inset 0 -1px 0 var(--border)',
                    }}
                  >
                    {formatCount(row.request_count)}
                  </td>
                  <td
                    className="num"
                    style={{
                      padding: '7px 10px',
                      textAlign: 'right',
                      color: row.error_count > 0 ? 'var(--rose)' : 'var(--fg-faint)',
                      boxShadow: 'inset 0 -1px 0 var(--border)',
                    }}
                  >
                    {formatCount(row.error_count)}
                  </td>
                  <td style={{ padding: '7px 10px', boxShadow: 'inset 0 -1px 0 var(--border)' }}>
                    <TokensCell row={row} maxTokens={maxTokens} />
                  </td>
                  <td
                    className="num"
                    style={{
                      padding: '7px 10px',
                      textAlign: 'right',
                      fontWeight: 600,
                      color: row.cost ? 'var(--fg-strong)' : 'var(--fg-faint)',
                      boxShadow: 'inset 0 -1px 0 var(--border)',
                    }}
                  >
                    {row.cost ? formatMoney(row.cost.total) : 'n/a'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <p style={{ margin: 0, padding: '10px 14px', fontSize: 10.5, color: 'var(--fg-faint)' }}>
        {shown.length < sorted.length
          ? `Showing the first ${formatCount(shown.length)} of ${formatCount(sorted.length)} sessions. Narrow the filters to see the rest.`
          : `${formatCount(sorted.length)} sessions shown. Click any row to open its trace, economics and context.`}
      </p>
    </section>
  )
}
