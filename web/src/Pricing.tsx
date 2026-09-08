import { useState } from 'react'
import type { JSX } from 'react'
import type { ModelRate, ProviderRules, RateTable, Report } from './api'
import { formatCount, formatMoney, formatTokens } from './format'

const DEFAULT_RULES: ProviderRules = { cache_read: 0.1, cache_write_5m: 1.25, cache_write_1h: 2.0, batch: 0.5, free: false }
const REVEAL_BATCH = 20

const RATE_COLUMNS: { label: string; align: 'left' | 'right' }[] = [
  { label: 'Model', align: 'left' },
  { label: 'Provider', align: 'left' },
  { label: 'Input', align: 'right' },
  { label: 'Cache read', align: 'right' },
  { label: 'Cache write 5m', align: 'right' },
  { label: 'Output', align: 'right' },
  { label: 'State', align: 'right' },
  { label: 'Spend here', align: 'right' },
]

interface RateRow {
  rate: ModelRate
  input: string
  output: string
  cacheRead: string
  cacheWrite5m: string
  spendValue: number
  spendLabel: string
  stateLabel: string
  badgeClass: string
}

function effectiveRules(rate: ModelRate, rates: RateTable): ProviderRules {
  return rate.cache_rules ?? rates.providers[rate.provider] ?? DEFAULT_RULES
}

function buildRow(rate: ModelRate, rates: RateTable, report: Report): RateRow {
  const providerRules = rates.providers[rate.provider]
  const isFree = providerRules?.free === true
  const rules = effectiveRules(rate, rates)
  const bucket = report.by_model.find((b) => b.label === rate.display)
  const spendValue = bucket ? bucket.cost.total : 0
  const stateLabel = isFree ? 'free' : spendValue > 0 ? 'priced' : 'unused'
  const badgeClass = isFree ? 'badge badge--free' : spendValue > 0 ? 'badge badge--accent' : 'badge'

  return {
    rate,
    input: isFree ? 'free' : `$${rate.input.toFixed(2)}`,
    output: isFree ? 'free' : `$${rate.output.toFixed(2)}`,
    cacheRead: isFree ? 'free' : `$${(rate.input * rules.cache_read).toFixed(3)}`,
    cacheWrite5m: isFree ? 'free' : `$${(rate.input * rules.cache_write_5m).toFixed(3)}`,
    spendValue,
    spendLabel: formatMoney(spendValue),
    stateLabel,
    badgeClass,
  }
}

function RateTableRow({ row }: { row: RateRow }) {
  return (
    <tr className="row-hit" style={{ borderBottom: '1px solid var(--border)' }}>
      <td style={{ padding: '8px 10px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 6, color: 'var(--fg-strong)' }}>
          {row.rate.display}
          {row.rate.inherited && (
            <span className="badge" style={{ fontSize: 9, padding: '1px 5px' }}>
              inherited
            </span>
          )}
        </div>
        <div className="num" style={{ fontSize: 9.5, color: 'var(--fg-faint)' }}>
          {row.rate.match}
        </div>
      </td>
      <td style={{ padding: '8px 10px', color: 'var(--fg-muted)' }}>{row.rate.provider}</td>
      <td className="num" style={{ padding: '8px 10px', textAlign: 'right', color: 'var(--fg-strong)' }}>
        {row.input}
      </td>
      <td className="num" style={{ padding: '8px 10px', textAlign: 'right', color: 'var(--fg-muted)' }}>
        {row.cacheRead}
      </td>
      <td className="num" style={{ padding: '8px 10px', textAlign: 'right', color: 'var(--fg-muted)' }}>
        {row.cacheWrite5m}
      </td>
      <td className="num" style={{ padding: '8px 10px', textAlign: 'right', color: 'var(--fg-strong)' }}>
        {row.output}
      </td>
      <td style={{ padding: '8px 10px', textAlign: 'right' }}>
        <span className={row.badgeClass} style={{ fontSize: 9, padding: '1px 5px' }}>
          {row.stateLabel}
        </span>
      </td>
      <td className="num" style={{ padding: '8px 10px', textAlign: 'right', color: 'var(--fg-strong)' }}>
        {row.spendLabel}
      </td>
    </tr>
  )
}

function RateTablePanel({ rates, report }: { rates: RateTable; report: Report }) {
  const [revealed, setRevealed] = useState(0)

  const sorted = rates.models.map((rate) => buildRow(rate, rates, report)).sort((a, b) => b.spendValue - a.spendValue)
  const priced = sorted.filter((row) => row.spendValue > 0)
  const zero = sorted.filter((row) => row.spendValue === 0)
  const shownZero = zero.slice(0, revealed)
  const hiddenCount = zero.length - shownZero.length
  const visibleRows = [...priced, ...shownZero]

  return (
    <section className="panel">
      <div className="panel__head">
        <div>
          <p className="lbl" style={{ color: 'var(--accent)' }}>
            Rate table
          </p>
          <h2 className="panel__title">{`Prices per million tokens, as of ${rates.as_of}`}</h2>
        </div>
        <p style={{ margin: 0, maxWidth: '40ch', fontSize: 11, lineHeight: 1.5, color: 'var(--fg-muted)', textAlign: 'right' }}>
          Cache prices are derived from the input rate by each provider's own rules. Cost is never stored.
        </p>
      </div>
      <div style={{ overflowX: 'auto' }}>
        <table className="data-table">
          <thead>
            <tr>
              {RATE_COLUMNS.map((column) => (
                <th
                  key={column.label}
                  className="lbl"
                  style={{ padding: '8px 10px', background: 'var(--bg-muted)', borderBottom: '1px solid var(--border)', textAlign: column.align }}
                >
                  {column.label}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {visibleRows.map((row) => (
              <RateTableRow key={row.rate.match} row={row} />
            ))}
          </tbody>
        </table>
      </div>
      {hiddenCount > 0 && (
        <div className="panel__body">
          <button
            type="button"
            className="chip"
            onClick={() => setRevealed((current) => current + REVEAL_BATCH)}
          >
            {`Show ${Math.min(REVEAL_BATCH, hiddenCount)} more rates (${hiddenCount} hidden)`}
          </button>
        </div>
      )}
    </section>
  )
}

function ProviderMultipliers({ providerId, rules }: { providerId: string; rules: ProviderRules }) {
  const items = [
    { label: 'Cache read', value: rules.cache_read },
    { label: 'Cache write, 5 min', value: rules.cache_write_5m },
    { label: 'Cache write, 1 hour', value: rules.cache_write_1h },
    { label: 'Batch tier', value: rules.batch },
  ]
  const max = Math.max(...items.map((item) => item.value), 1)
  const providerLabel = providerId.charAt(0).toUpperCase() + providerId.slice(1)

  return (
    <div style={{ padding: '8px 0', borderBottom: '1px solid var(--border)' }}>
      <p className="lbl" style={{ marginBottom: 6 }}>
        {providerLabel}
      </p>
      {items.map((item) => (
        <div
          key={item.label}
          style={{ display: 'grid', gridTemplateColumns: '140px minmax(0,1fr) 46px', alignItems: 'center', gap: 10, padding: '4px 0' }}
        >
          <span style={{ fontSize: 11.5, color: 'var(--fg-strong)' }}>{item.label}</span>
          <div className="meter" style={{ height: 14 }}>
            <div className="meter__fill" style={{ width: `${(item.value / max) * 100}%` }} />
          </div>
          <span className="num" style={{ textAlign: 'right', fontSize: 11.5, color: 'var(--fg-strong)' }}>{`${item.value}x`}</span>
        </div>
      ))}
    </div>
  )
}

function MultipliersPanel({ rates, report }: { rates: RateTable; report: Report }) {
  const providersPresent = report.by_provider.filter((bucket) => bucket.cost.total > 0)

  return (
    <section className="panel">
      <div className="panel__head" style={{ display: 'block' }}>
        <p className="lbl" style={{ color: 'var(--accent)' }}>
          Multipliers
        </p>
        <h2 className="panel__title">Every bucket priced off the base input rate, per provider</h2>
      </div>
      <div className="panel__body">
        {providersPresent.length === 0 ? (
          <p style={{ fontSize: 11, color: 'var(--fg-muted)' }}>No priced activity in this slice yet.</p>
        ) : (
          providersPresent.map((bucket) => {
            const rules = rates.providers[bucket.key]
            return rules ? <ProviderMultipliers key={bucket.key} providerId={bucket.key} rules={rules} /> : null
          })
        )}
        <p className="panel__note">
          These rules differ by provider — a discount that holds for one vendor is not universal, so each is shown on its
          own rather than as one shared list.
        </p>
      </div>
    </section>
  )
}

function UnpricedPanel({ report }: { report: Report }) {
  const models = report.unknown_models
  if (models.length === 0) return null

  const first = models[0]
  const snippet = `{"match": "${first.model}", "provider": "...", "display": "...", "input": 0, "output": 0}`

  return (
    <section className="panel" style={{ borderLeft: '3px solid var(--accent)' }}>
      <div className="panel__head" style={{ display: 'block' }}>
        <p className="lbl" style={{ color: 'var(--accent)' }}>
          Unpriced
        </p>
        <h2 className="panel__title">{`${formatCount(models.length)} model with tokens and no rate`}</h2>
      </div>
      <div className="panel__body">
        {models.map((model) => (
          <div
            key={model.model}
            style={{ display: 'flex', alignItems: 'baseline', justifyContent: 'space-between', gap: 10, padding: '6px 0', borderBottom: '1px solid var(--border)' }}
          >
            <span className="num" style={{ fontSize: 11.5, color: 'var(--fg-strong)' }}>
              {model.model}
            </span>
            <span className="num" style={{ fontSize: 11, color: 'var(--fg-muted)' }}>
              {`${formatTokens(model.tokens)} tokens · ${formatCount(model.events)} events`}
            </span>
          </div>
        ))}
        <p style={{ margin: '10px 0 8px', fontSize: 11, lineHeight: 1.55, color: 'var(--fg-muted)' }}>
          Tokens are counted and shown, cost stays out of the totals until a rate exists. Add one line to rates.json and
          history reprices.
        </p>
        <pre
          className="num"
          style={{ margin: 0, padding: '10px 12px', background: 'var(--bg-muted)', border: '1px solid var(--border)', fontSize: 10.5, lineHeight: 1.6, color: 'var(--fg-strong)', overflow: 'auto' }}
        >
          {snippet}
        </pre>
      </div>
    </section>
  )
}

export default function Pricing(props: { report: Report; rates: RateTable }): JSX.Element {
  const { report, rates } = props

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
      <RateTablePanel rates={rates} report={report} />
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(min(360px, 100%), 1fr))', gap: 14 }}>
        <MultipliersPanel rates={rates} report={report} />
        <UnpricedPanel report={report} />
      </div>
    </div>
  )
}
