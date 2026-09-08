import { useState, useSyncExternalStore } from 'react'
import type { JSX, ReactNode } from 'react'
import type { EconRow, Provenance } from './api'
import type { EconomicsTabProps } from './SessionWorkspace'
import { ProvenanceChip, Unavailable } from './SessionWorkspace'
import { formatCount, formatDuration, formatMoney, formatPercent, formatTokens } from './format'
import { STATE_BADGE } from './theme'

const REVEAL_BATCH = 40
const PHONE_QUERY = '(max-width: 639px)'

const DURATION_NOTE: Record<Provenance, string> = {
  measured: 'The log records a start and an end for this work.',
  derived: 'Wall-clock gap between log records. The API never reports its own latency here.',
  estimated: 'Estimated from a table, not from this log.',
  inferred: 'Inferred from the model id, not from this log.',
  unavailable: 'This client logs no timing for these spans.',
}

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

function DurationCell({ row }: { row: EconRow }) {
  if (row.duration_ms === null) {
    return <Unavailable hint={DURATION_NOTE[row.duration_provenance]} />
  }
  return (
    <span style={{ display: 'inline-flex', alignItems: 'center', gap: 6, justifyContent: 'flex-end' }}>
      <span className="num">{formatDuration(row.duration_ms)}</span>
      <ProvenanceChip group="time" provenance={row.duration_provenance} />
    </span>
  )
}

function CostCell({ row }: { row: EconRow }) {
  const partial = row.cost !== null && row.cost_state !== 'priced' && row.cost_state !== 'free'
  return (
    <span style={{ display: 'inline-flex', alignItems: 'center', gap: 6, justifyContent: 'flex-end' }}>
      {row.cost === null ? (
        <Unavailable hint="No model call in this row carried a priced token count." />
      ) : (
        <span className="num" style={{ color: 'var(--fg-strong)' }}>
          {formatMoney(row.cost.total)}
        </span>
      )}
      {partial && (
        <span style={{ fontSize: 9.5, color: 'var(--fg-faint)' }} title="Only the priced model calls in this row are in that figure.">
          partial
        </span>
      )}
      <span
        className={STATE_BADGE[row.cost_state]}
        title="The worst cost state among this row's model calls."
        style={{ height: 18, padding: '0 5px', fontSize: 8.5 }}
      >
        {row.cost_state}
      </span>
    </span>
  )
}

function hasTokens(row: EconRow): boolean {
  if (row.model_calls === 0) return false
  return row.tokens.total > 0 || row.cost_state !== 'unavailable'
}

function TokensCell({ row }: { row: EconRow }) {
  if (!hasTokens(row)) {
    return <Unavailable hint="No model call in this row logged a token count, so this is an absence rather than a zero." />
  }
  return (
    <span className="num" title={`${formatCount(row.tokens.total)} tokens`}>
      {formatTokens(row.tokens.total)}
    </span>
  )
}

function RetriesCell({ row }: { row: EconRow }) {
  if (row.retries === null) {
    return <Unavailable hint="This client does not log retry attempts, so this is not a zero." />
  }
  return <span className="num">{formatCount(row.retries)}</span>
}

function AmplificationCell({ row }: { row: EconRow }) {
  if (row.amplification === null) {
    return <Unavailable hint="Needs model calls with both input and output tokens." />
  }
  return <span className="num">{`${row.amplification.toFixed(1)}x`}</span>
}

function CacheCell({ row }: { row: EconRow }) {
  if (row.cache_hit_ratio === null) {
    return <Unavailable hint="No input tokens counted for this row." />
  }
  return <span className="num">{formatPercent(row.cache_hit_ratio)}</span>
}

interface Column {
  key: string
  label: string
  align: 'left' | 'right'
  cell: (row: EconRow) => ReactNode
}

function labelColumn(label: string): Column {
  return {
    key: 'label',
    label,
    align: 'left',
    cell: (row) => (
      <span
        className="num"
        title={row.key}
        style={{
          display: 'inline-block',
          maxWidth: 220,
          overflow: 'hidden',
          textOverflow: 'ellipsis',
          whiteSpace: 'nowrap',
          color: 'var(--fg-strong)',
          verticalAlign: 'bottom',
        }}
      >
        {row.label}
      </span>
    ),
  }
}

const COUNT_COLUMNS: Column[] = [
  { key: 'model_calls', label: 'Model calls', align: 'right', cell: (row) => <span className="num">{formatCount(row.model_calls)}</span> },
  { key: 'tool_calls', label: 'Tool calls', align: 'right', cell: (row) => <span className="num">{formatCount(row.tool_calls)}</span> },
]

const ERROR_COLUMN: Column = {
  key: 'errors',
  label: 'Errors',
  align: 'right',
  cell: (row) => (
    <span className="num" style={{ color: row.errors > 0 ? 'var(--rose)' : 'var(--fg-muted)' }}>
      {formatCount(row.errors)}
    </span>
  ),
}

const DURATION_COLUMN: Column = { key: 'duration', label: 'Duration', align: 'right', cell: (row) => <DurationCell row={row} /> }
const TOKENS_COLUMN: Column = { key: 'tokens', label: 'Tokens', align: 'right', cell: (row) => <TokensCell row={row} /> }
const COST_COLUMN: Column = { key: 'cost', label: 'Cost', align: 'right', cell: (row) => <CostCell row={row} /> }

const TURN_COLUMNS: Column[] = [
  labelColumn('Turn'),
  ...COUNT_COLUMNS,
  TOKENS_COLUMN,
  COST_COLUMN,
  DURATION_COLUMN,
  ERROR_COLUMN,
  { key: 'retries', label: 'Retries', align: 'right', cell: (row) => <RetriesCell row={row} /> },
]

const MODEL_COLUMNS: Column[] = [
  labelColumn('Model'),
  COUNT_COLUMNS[0],
  TOKENS_COLUMN,
  COST_COLUMN,
  DURATION_COLUMN,
  { key: 'cache', label: 'Cache hit', align: 'right', cell: (row) => <CacheCell row={row} /> },
  { key: 'amplification', label: 'Amplification', align: 'right', cell: (row) => <AmplificationCell row={row} /> },
  {
    key: 'rate',
    label: 'Tokens/s',
    align: 'right',
    cell: (row) =>
      row.tokens_per_second === null ? (
        <Unavailable hint="Needs measured tokens and a measured duration on the same call. No source logs both today." />
      ) : (
        <span className="num">{row.tokens_per_second.toFixed(1)}</span>
      ),
  },
]

const TOOL_COLUMNS: Column[] = [
  labelColumn('Tool'),
  COUNT_COLUMNS[1],
  DURATION_COLUMN,
  ERROR_COLUMN,
]

function EconCard({ row, columns }: { row: EconRow; columns: Column[] }) {
  const [first, ...rest] = columns
  return (
    <div className="row-card">
      <div>{first.cell(row)}</div>
      {rest.map((column) => (
        <div key={column.key} style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 10, fontSize: 11 }}>
          <span className="lbl">{column.label}</span>
          <span style={{ color: 'var(--fg-muted)', textAlign: 'right' }}>{column.cell(row)}</span>
        </div>
      ))}
    </div>
  )
}

function EconPanel(props: {
  eyebrow: string
  title: string
  note: string
  columns: Column[]
  rows: EconRow[]
  empty: string
  isPhone: boolean
}) {
  const [revealed, setRevealed] = useState(REVEAL_BATCH)
  const shown = props.rows.slice(0, revealed)
  const hidden = props.rows.length - shown.length

  return (
    <section className="panel">
      <div className="panel__head">
        <div>
          <p className="lbl" style={{ color: 'var(--accent)' }}>
            {props.eyebrow}
          </p>
          <h2 className="panel__title">{props.title}</h2>
        </div>
      </div>
      {props.rows.length === 0 ? (
        <p style={{ margin: 0, padding: '12px 14px', fontSize: 11.5, color: 'var(--fg-muted)' }}>{props.empty}</p>
      ) : props.isPhone ? (
        <div className="panel__body" style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
          {shown.map((row) => (
            <EconCard key={row.key} row={row} columns={props.columns} />
          ))}
        </div>
      ) : (
        <div style={{ overflowX: 'auto' }}>
          <table className="data-table">
            <thead>
              <tr>
                {props.columns.map((column) => (
                  <th
                    key={column.key}
                    className="lbl"
                    style={{
                      padding: '8px 10px',
                      background: 'var(--bg-muted)',
                      borderBottom: '1px solid var(--border)',
                      textAlign: column.align,
                      whiteSpace: 'nowrap',
                    }}
                  >
                    {column.label}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {shown.map((row) => (
                <tr key={row.key} className="row-hit" style={{ borderBottom: '1px solid var(--border)' }}>
                  {props.columns.map((column) => (
                    <td
                      key={column.key}
                      style={{ padding: '7px 10px', textAlign: column.align, color: 'var(--fg-muted)', whiteSpace: 'nowrap' }}
                    >
                      {column.cell(row)}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      <div className="panel__body" style={{ paddingTop: 10 }}>
        {hidden > 0 && (
          <button type="button" className="chip" onClick={() => setRevealed(revealed + REVEAL_BATCH)}>
            {`Show ${Math.min(REVEAL_BATCH, hidden)} more (${formatCount(hidden)} hidden)`}
          </button>
        )}
        <p className="panel__note" style={{ borderTop: hidden > 0 ? '1px solid var(--border)' : 'none', paddingTop: hidden > 0 ? 10 : 0, marginTop: hidden > 0 ? 10 : 0 }}>
          {props.note}
        </p>
      </div>
    </section>
  )
}

function Kpi({ label, value, foot }: { label: string; value: ReactNode; foot: string }) {
  return (
    <div className="kpi">
      <p className="lbl">{label}</p>
      <div className="stat__value">{value}</div>
      <p style={{ margin: '6px 0 0', fontSize: 10.5, lineHeight: 1.45, color: 'var(--fg-muted)' }}>{foot}</p>
    </div>
  )
}

function retryFoot(source: string): string {
  if (source === 'claude-code') return 'Retry attempts and api_error records, when the log carries them.'
  return `${source} writes no retry field, so this is absent rather than zero.`
}

export default function EconomicsTab(props: EconomicsTabProps): JSX.Element {
  const isPhone = useIsPhone()
  const totals = props.economics.totals
  const tokens = totals.tokens

  return (
    <>
      <section style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(min(155px, 100%), 1fr))', gap: 10 }}>
        <Kpi
          label="Tokens"
          value={<TokensCell row={totals} />}
          foot={
            hasTokens(totals)
              ? `${formatTokens(tokens.input_total)} in, ${formatTokens(tokens.output)} out across ${formatCount(totals.model_calls)} model calls.`
              : `This client logs no token counts. Its ${formatCount(totals.model_calls)} model calls are real; their tokens are not recorded.`
          }
        />
        <Kpi
          label="Cost"
          value={
            totals.cost === null ? (
              <Unavailable hint="No priced model call in this session." />
            ) : (
              formatMoney(totals.cost.total)
            )
          }
          foot={`List prices from the rate table. State is ${totals.cost_state}, the worst of this session's model calls.`}
        />
        <Kpi
          label="Duration"
          value={<DurationCell row={totals} />}
          foot="Summed over the session's turns, not wall clock between the first and last record."
        />
        <Kpi
          label="Calls"
          value={<span className="num">{formatCount(totals.model_calls + totals.tool_calls)}</span>}
          foot={`${formatCount(totals.model_calls)} model, ${formatCount(totals.tool_calls)} tool, ${formatCount(totals.errors)} errored.`}
        />
        <Kpi label="Retries" value={<RetriesCell row={totals} />} foot={retryFoot(props.source)} />
        <Kpi
          label="Amplification"
          value={<AmplificationCell row={totals} />}
          foot="Input tokens read per output token produced."
        />
        <Kpi label="Cache hit ratio" value={<CacheCell row={totals} />} foot="Share of input tokens served from the prompt cache." />
        <Kpi
          label="Tokens per second"
          value={
            totals.tokens_per_second === null ? (
              <Unavailable hint="Needs measured tokens and a measured duration on the same call." />
            ) : (
              <span className="num">{totals.tokens_per_second.toFixed(1)}</span>
            )
          }
          foot="Only measured tokens over a measured duration count. No client here logs both on one call, so it stays blank."
        />
      </section>

      {hasTokens(totals) && (
        <p className="panel__note" style={{ margin: 0, borderTop: 'none', paddingTop: 0 }}>
          {tokens.reasoning_output > 0
            ? `Reasoning — ${formatTokens(tokens.reasoning_output)}, already inside the ${formatTokens(tokens.output)} output above, never a fifth bucket.`
            : 'No reasoning tokens are logged for this session. When they are, they sit inside output, not beside it.'}
        </p>
      )}

      <EconPanel
        eyebrow="Per turn"
        title={`${formatCount(props.economics.by_turn.length)} turns, in the order they ran`}
        note="A turn is one prompt and everything it caused. Cost is the sum of its priced model calls; a row marked partial has model calls that no rate matched."
        columns={TURN_COLUMNS}
        rows={props.economics.by_turn}
        empty="No turns carry spans for this session."
        isPhone={isPhone}
      />

      <EconPanel
        eyebrow="Per model"
        title={`${formatCount(props.economics.by_model.length)} models, heaviest first`}
        note="Sorted by tokens. A model with no rate entry still shows its tokens; its cost stays out."
        columns={MODEL_COLUMNS}
        rows={props.economics.by_model}
        empty="No model call in this session carried a model id."
        isPhone={isPhone}
      />

      <EconPanel
        eyebrow="Per tool"
        title={`${formatCount(props.economics.by_tool.length)} tools, most called first`}
        note="Tools carry no tokens of their own, so this table counts calls, time and errors only. Their cost lands on the model call that read the result."
        columns={TOOL_COLUMNS}
        rows={props.economics.by_tool}
        empty="No tool calls in this session."
        isPhone={isPhone}
      />
    </>
  )
}
