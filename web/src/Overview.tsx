import { useEffect, useRef, useState } from 'react'
import type { JSX } from 'react'
import type { Bucket, CostState, Meta, Report, SeriesPoint, SessionRow, SourceInfo, View } from './api'
import { timeChart, spark } from './chart'
import type { TimeChartRow } from './chart'
import { formatCount, formatDuration, formatMoney, formatPercent, formatTokens } from './format'
import { BUCKETS, PROVENANCE_COLOR, SERIES, STATE_COLOR } from './theme'

type StackBy = 'client' | 'provider' | 'model'
type Metric = 'cost' | 'tokens'

function sortedDays(report: Report): string[] {
  return [...report.by_day].map((bucket) => bucket.key).sort()
}

function SourceCard({ source, index, report }: { source: SourceInfo; index: number; report: Report }) {
  const dot = SERIES[index % SERIES.length]
  const isFull = source.token_data === 'full'
  const ownSessions = report.sessions.filter((session) => session.source === source.id)
  const cost = ownSessions.reduce((sum, session) => sum + (session.cost ? session.cost.total : 0), 0)
  const requests = ownSessions.reduce((sum, session) => sum + session.request_count, 0)
  const tokensTotal = ownSessions.reduce((sum, session) => sum + (session.tokens ? session.tokens.total : 0), 0)
  const headline = isFull ? formatMoney(cost) : formatCount(requests)
  const foot = isFull
    ? `${formatCount(ownSessions.length)} sessions · ${formatTokens(tokensTotal)} tokens`
    : 'requests logged, no token counts'

  const days = sortedDays(report)
  const points = report.series.filter((point) => point.source === source.id)
  const perDay = days.map((day) => {
    const dayPoints = points.filter((point) => point.day === day)
    return isFull
      ? dayPoints.reduce((sum, point) => sum + point.cost, 0)
      : dayPoints.reduce((sum, point) => sum + point.events, 0)
  })
  const { line, area } = spark(perDay, 96, 26)

  return (
    <div
      className="row-hit"
      style={{ padding: '12px 14px', borderRight: '1px solid var(--border)', borderBottom: '1px solid var(--border)' }}
    >
      <div style={{ display: 'flex', alignItems: 'center', gap: 7 }}>
        <span style={{ width: 7, height: 7, borderRadius: '50%', background: dot }} />
        <span style={{ fontSize: 12.5, fontWeight: 600, color: 'var(--fg-strong)' }}>{source.label}</span>
        <span
          className={isFull ? 'badge badge--accent' : 'badge'}
          style={{ marginLeft: 'auto', fontSize: 9, padding: '1px 5px' }}
        >
          {isFull ? 'token counts' : 'session only'}
        </span>
      </div>
      <div className="num" style={{ marginTop: 7, fontSize: 9.5, color: 'var(--fg-faint)', wordBreak: 'break-all', lineHeight: 1.4 }}>
        {source.path}
      </div>
      <div style={{ display: 'flex', alignItems: 'flex-end', justifyContent: 'space-between', gap: 8, marginTop: 10 }}>
        <div>
          <div className="num" style={{ fontSize: 19, fontWeight: 600, color: 'var(--fg-strong)', lineHeight: 1 }}>
            {headline}
          </div>
          <div style={{ marginTop: 4, fontSize: 10.5, color: 'var(--fg-muted)' }}>{foot}</div>
        </div>
        <svg width={96} height={26} viewBox="0 0 96 26" style={{ flex: 'none', overflow: 'visible' }}>
          <path d={area} fill={dot} opacity={0.14} />
          <polyline points={line} fill="none" stroke={dot} strokeWidth={1.4} />
        </svg>
      </div>
    </div>
  )
}

function DetectedSourcesPanel({
  meta,
  report,
  onSelectView,
}: {
  meta: Meta
  report: Report
  onSelectView: (view: View) => void
}) {
  const detected = meta.sources.filter((source) => source.detected)
  const undetectedCount = meta.sources.length - detected.length

  return (
    <section className="panel">
      <div className="panel__head">
        <div>
          <p className="lbl" style={{ color: 'var(--accent)' }}>
            Detected on this machine
          </p>
          <h2 className="panel__title">{`${detected.length} of ${meta.sources.length} readers found logs`}</h2>
        </div>
        <p style={{ margin: 0, maxWidth: '44ch', fontSize: 11, lineHeight: 1.5, color: 'var(--fg-muted)', textAlign: 'right' }}>
          Sources with token counts carry cost. The rest log sessions only, and their cost is never invented.
        </p>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(min(232px, 100%), 1fr))' }}>
        {detected.map((source, i) => (
          <SourceCard key={source.id} source={source} index={i} report={report} />
        ))}
      </div>
      {undetectedCount > 0 && (
        <button
          type="button"
          onClick={() => onSelectView('sources')}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: 8,
            width: '100%',
            padding: '9px 14px',
            border: 0,
            background: 'transparent',
            cursor: 'pointer',
            textAlign: 'left',
            fontFamily: 'var(--font-sans)',
            fontSize: 11,
            color: 'var(--fg-faint)',
          }}
        >
          <span>{`${undetectedCount} more readers ship with the tool and aren't found here`}</span>
        </button>
      )}
    </section>
  )
}

function StatTile({ label, value, foot, values }: { label: string; value: string; foot: string; values: number[] }) {
  const { line } = spark(values, 120, 26)
  return (
    <div className="kpi">
      <p className="lbl">{label}</p>
      <div className="stat__value">{value}</div>
      <p style={{ margin: '6px 0 0', fontSize: 10.5, lineHeight: 1.45, color: 'var(--fg-muted)' }}>{foot}</p>
      <svg width="100%" height={26} viewBox="0 0 120 26" preserveAspectRatio="none" style={{ marginTop: 8, display: 'block' }}>
        <polyline points={line} fill="none" stroke="var(--fg-faint)" strokeWidth={1.3} vectorEffect="non-scaling-stroke" />
      </svg>
    </div>
  )
}

function KpiRow({ report }: { report: Report }) {
  const days = sortedDays(report)
  const byDay = new Map(report.by_day.map((bucket) => [bucket.key, bucket]))
  const costPerDay = days.map((day) => byDay.get(day)?.cost.total ?? 0)
  const cacheReadPerDay = days.map((day) => byDay.get(day)?.tokens.cache_read ?? 0)
  const requestsPerDay = days.map((day) => byDay.get(day)?.events ?? 0)
  const sessionsPerDay = days.map((day) => byDay.get(day)?.sessions ?? 0)
  const cacheSavedPerDay = days.map((day) => byDay.get(day)?.cost.cache_savings ?? 0)

  const totals = report.totals
  const wideSpark = spark(costPerDay, 240, 34)
  const avgFoot = totals.sessions > 0 ? `${formatMoney(totals.cost.total / totals.sessions)} average each` : 'none in this slice'
  const cacheSaveFoot =
    totals.cost.no_cache_equivalent > 0
      ? `${formatPercent(totals.cost.cache_savings / totals.cost.no_cache_equivalent)} off the no cache price`
      : 'no priced tokens'

  return (
    <section style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(min(165px, 100%), 1fr))', gap: 10 }}>
      <div className="kpi kpi--wide">
        <p className="lbl">API equivalent cost</p>
        <div className="kpi__value">{formatMoney(totals.cost.total)}</div>
        <p style={{ margin: '8px 0 0', fontSize: 11, lineHeight: 1.5, color: 'var(--fg-muted)' }}>
          {`What ${formatCount(totals.events)} requests would cost at published list prices.`}
        </p>
        <svg width="100%" height={34} viewBox="0 0 240 34" preserveAspectRatio="none" style={{ marginTop: 10, display: 'block' }}>
          <path d={wideSpark.area} fill="var(--accent)" opacity={0.16} />
          <polyline points={wideSpark.line} fill="none" stroke="var(--accent)" strokeWidth={1.5} vectorEffect="non-scaling-stroke" />
        </svg>
      </div>

      <StatTile
        label="Tokens"
        value={formatTokens(totals.tokens.total)}
        foot={`${formatTokens(totals.tokens.cache_read)} of it cache reads`}
        values={cacheReadPerDay}
      />
      <StatTile
        label="Requests"
        value={formatCount(totals.events)}
        foot={`across ${formatCount(report.files_scanned)} log files`}
        values={requestsPerDay}
      />
      <StatTile label="Sessions" value={formatCount(totals.sessions)} foot={avgFoot} values={sessionsPerDay} />
      <StatTile label="Cache saved" value={formatMoney(totals.cost.cache_savings)} foot={cacheSaveFoot} values={cacheSavedPerDay} />
    </section>
  )
}

function OutcomeTile({ label, value, foot, available }: { label: string; value: string; foot: string; available: boolean }) {
  return (
    <div className="kpi">
      <p className="lbl">{label}</p>
      <div className="stat__value" style={available ? undefined : { color: 'var(--fg-faint)' }}>
        {value}
      </div>
      <p style={{ margin: '6px 0 0', fontSize: 10.5, lineHeight: 1.45, color: 'var(--fg-muted)' }}>{foot}</p>
    </div>
  )
}

function OutcomeRow({ report }: { report: Report }) {
  const sessions = report.sessions
  const rated = sessions.filter((session) => session.outcome !== 'unrated')
  const successful = rated.filter((session) => session.outcome === 'successful')
  const tokens = successful.reduce((sum, session) => sum + (session.tokens ? session.tokens.total : 0), 0)
  const cost = successful.reduce((sum, session) => sum + (session.cost ? session.cost.total : 0), 0)
  const noneRatedFoot = `Nothing is rated yet, so there is no rate to show. Rate a session in its workspace, then rescan: ${formatCount(sessions.length)} sessions are unrated.`
  const noneSuccessfulFoot = rated.length > 0 ? 'No rated session in this slice came out successful.' : 'Available once a session is rated successful.'

  return (
    <section style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(min(200px, 100%), 1fr))', gap: 10 }}>
      <OutcomeTile
        label="Success rate"
        value={rated.length > 0 ? formatPercent(successful.length / rated.length) : 'unavailable'}
        foot={
          rated.length > 0
            ? `${formatCount(successful.length)} of ${formatCount(rated.length)} rated sessions succeeded, ${formatCount(sessions.length - rated.length)} still unrated`
            : noneRatedFoot
        }
        available={rated.length > 0}
      />
      <OutcomeTile
        label="Tokens per success"
        value={successful.length > 0 ? formatTokens(tokens / successful.length) : 'unavailable'}
        foot={
          successful.length > 0
            ? `${formatTokens(tokens)} across ${formatCount(successful.length)} successful sessions`
            : noneSuccessfulFoot
        }
        available={successful.length > 0}
      />
      <OutcomeTile
        label="Cost per success"
        value={successful.length > 0 ? formatMoney(cost / successful.length) : 'unavailable'}
        foot={
          successful.length > 0
            ? `${formatMoney(cost)} of list price bought ${formatCount(successful.length)} successful sessions`
            : noneSuccessfulFoot
        }
        available={successful.length > 0}
      />
    </section>
  )
}

function logSpanMs(session: SessionRow): number {
  const start = Date.parse(session.start_time)
  const end = Date.parse(session.end_time)
  if (!Number.isFinite(start) || !Number.isFinite(end) || end <= start) return 0
  return end - start
}

function HeavyRow({ session, report, value }: { session: SessionRow; report: Report; value: string }) {
  const model = session.models[0] ?? '(no model)'
  const label = report.by_model.find((bucket) => bucket.key === model)?.label ?? model
  return (
    <div style={{ display: 'flex', alignItems: 'baseline', gap: 10, padding: '5px 0' }}>
      <div style={{ minWidth: 0, flex: 1 }}>
        <div className="num" style={{ fontSize: 11, color: 'var(--fg-strong)', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
          {session.session_id}
        </div>
        <div style={{ fontSize: 9.5, color: 'var(--fg-faint)', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
          {`${session.client} · ${label}`}
        </div>
      </div>
      <div className="num" style={{ flex: 'none', fontSize: 12, color: 'var(--fg-strong)' }}>
        {value}
      </div>
    </div>
  )
}

function ProvenanceTag({ word }: { word: 'derived' }) {
  return (
    <span className="badge" style={{ height: 18, fontSize: 9, gap: 5, color: 'var(--fg-muted)' }}>
      <span style={{ width: 6, height: 6, flex: 'none', background: PROVENANCE_COLOR[word] }} />
      {word}
    </span>
  )
}

function HeaviestSessionsPanel({ report }: { report: Report }) {
  const byCost = [...report.sessions].filter((session) => session.cost !== null).sort((a, b) => (b.cost?.total ?? 0) - (a.cost?.total ?? 0)).slice(0, 6)
  const bySpan = [...report.sessions].filter((session) => logSpanMs(session) > 0).sort((a, b) => logSpanMs(b) - logSpanMs(a)).slice(0, 6)

  return (
    <section className="panel">
      <div className="panel__head">
        <div>
          <p className="lbl" style={{ color: 'var(--accent)' }}>
            Heaviest sessions
          </p>
          <h2 className="panel__title">
            {byCost.length > 0 ? `The costliest session is ${formatMoney(byCost[0].cost?.total ?? 0)}` : 'No priced session in this slice'}
          </h2>
        </div>
      </div>
      <div className="panel__body">
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(min(260px, 100%), 1fr))', gap: '0 20px' }}>
          <div>
            <div className="lbl" style={{ paddingBottom: 6 }}>Most expensive</div>
            {byCost.map((session) => (
              <HeavyRow key={`cost-${session.source}-${session.session_id}`} session={session} report={report} value={formatMoney(session.cost?.total ?? 0)} />
            ))}
            {byCost.length === 0 && <p style={{ margin: 0, fontSize: 11, color: 'var(--fg-faint)' }}>unavailable</p>}
          </div>
          <div>
            <div className="lbl" style={{ display: 'flex', alignItems: 'center', gap: 8, paddingBottom: 6 }}>
              <span>Longest log span</span>
              <ProvenanceTag word="derived" />
            </div>
            {bySpan.map((session) => (
              <HeavyRow key={`span-${session.source}-${session.session_id}`} session={session} report={report} value={formatDuration(logSpanMs(session))} />
            ))}
            {bySpan.length === 0 && <p style={{ margin: 0, fontSize: 11, color: 'var(--fg-faint)' }}>unavailable</p>}
          </div>
        </div>
        <p className="panel__note">
          Cost is the list price of the session&rsquo;s own requests. The span is the last log record minus the first,
          derived, so it counts every idle minute between prompts and is not working time. Outcomes come from the last
          scan, so a rating shows up here after the next rescan.
        </p>
      </div>
    </section>
  )
}

function TimeChartPanel({ report, meta }: { report: Report; meta: Meta }) {
  const [stackBy, setStackBy] = useState<StackBy>('client')
  const [metric, setMetric] = useState<Metric>('cost')
  const [chartWidth, setChartWidth] = useState(600)
  const containerRef = useRef<HTMLDivElement | null>(null)

  useEffect(() => {
    const node = containerRef.current
    if (!node) return
    const measure = () => {
      const cs = getComputedStyle(node)
      const width = Math.round(node.clientWidth - parseFloat(cs.paddingLeft || '0') - parseFloat(cs.paddingRight || '0'))
      if (width > 100) setChartWidth(width)
    }
    measure()
    const observer = new ResizeObserver(measure)
    observer.observe(node)
    return () => observer.disconnect()
  }, [])

  const clientLabel = (id: string) => meta.clients.find((client) => client.id === id)?.label ?? id
  const modelLabel = (id: string) => report.by_model.find((bucket) => bucket.key === id)?.label ?? id

  const keyOf = (point: SeriesPoint) => (stackBy === 'client' ? point.client : stackBy === 'provider' ? point.provider : point.model)
  const labelOf = (point: SeriesPoint) =>
    stackBy === 'client' ? clientLabel(point.client) : stackBy === 'provider' ? point.provider : modelLabel(point.model)

  const rows: TimeChartRow[] = report.series.map((point) => ({
    day: point.day,
    key: keyOf(point),
    label: labelOf(point),
    value: metric === 'cost' ? point.cost : point.tokens,
  }))

  const days = sortedDays(report)
  const chart = timeChart({ days, rows, chartWidth, isCost: metric === 'cost', stackByLabel: stackBy })
  const eyebrow = metric === 'cost' ? 'Cost over time' : 'Tokens over time'

  return (
    <section className="panel">
      <div className="panel__head" style={{ alignItems: 'center', flexWrap: 'wrap' }}>
        <div>
          <p className="lbl" style={{ color: 'var(--accent)' }}>
            {eyebrow}
          </p>
          <h2 className="panel__title">{chart.title}</h2>
        </div>
        <div style={{ marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: 14, flexWrap: 'wrap' }}>
          <div style={{ display: 'flex', gap: 4 }}>
            {(['client', 'provider', 'model'] as const).map((option) => (
              <button
                key={option}
                type="button"
                className={`chip${stackBy === option ? ' is-active' : ''}`}
                style={{ height: 26, fontSize: 11, padding: '0 10px' }}
                onClick={() => setStackBy(option)}
              >
                {option === 'client' ? 'Client' : option === 'provider' ? 'Provider' : 'Model'}
              </button>
            ))}
          </div>
          <div style={{ display: 'flex', gap: 4 }}>
            {(['cost', 'tokens'] as const).map((option) => (
              <button
                key={option}
                type="button"
                className={`chip${metric === option ? ' is-active' : ''}`}
                style={{ height: 26, fontSize: 11, padding: '0 10px' }}
                onClick={() => setMetric(option)}
              >
                {option === 'cost' ? 'Cost' : 'Tokens'}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div ref={containerRef} className="chart-frame">
        <svg width={chart.w} height={chart.h} style={{ display: 'block', maxWidth: '100%' }}>
          {chart.grid.map((tick, i) => (
            <line key={i} x1={52} x2={chart.right} y1={tick.y} y2={tick.y} stroke="var(--border)" strokeWidth={1} />
          ))}
          {chart.bars.map((bar, i) => (
            <rect key={i} x={bar.x} y={bar.y} width={bar.w} height={bar.h} fill={bar.fill}>
              <title>{bar.title}</title>
            </rect>
          ))}
          <line x1={52} x2={chart.right} y1={chart.meanY} y2={chart.meanY} stroke="var(--fg-strong)" strokeWidth={1} strokeDasharray="4 4" opacity={0.55} />
          <line x1={chart.peakX} x2={chart.peakX} y1={chart.peakY} y2={chart.peakLineY} stroke="var(--accent)" strokeWidth={1} />
          <circle cx={chart.peakX} cy={chart.peakY} r={2.4} fill="var(--accent)" />
        </svg>
        <div className="chart-overlay">
          {chart.grid.map((tick, i) => (
            <div
              key={i}
              className="num"
              style={{ position: 'absolute', left: 0, top: tick.top, width: 46, textAlign: 'right', fontSize: 10, lineHeight: '12px', color: 'var(--fg-faint)' }}
            >
              {tick.label}
            </div>
          ))}
          {chart.xTicks.map((tick, i) => (
            <div
              key={i}
              className="num"
              style={{
                position: 'absolute',
                left: tick.left,
                top: chart.xLabelTop,
                transform: 'translateX(-50%)',
                fontSize: 10,
                lineHeight: '12px',
                whiteSpace: 'nowrap',
                color: 'var(--fg-faint)',
              }}
            >
              {tick.label}
            </div>
          ))}
          <div
            className="num"
            style={{
              position: 'absolute',
              left: chart.peakLabelLeft,
              top: chart.peakLabelTop,
              transform: chart.peakLabelTransform,
              fontSize: 10.5,
              fontWeight: 600,
              lineHeight: '12px',
              whiteSpace: 'nowrap',
              color: 'var(--accent)',
            }}
          >
            {chart.peakLabel}
          </div>
        </div>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: 14, flexWrap: 'wrap', padding: '6px 14px 12px' }}>
        {chart.legend.map((item) => (
          <span key={item.key} style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: 11, color: 'var(--fg-muted)' }}>
            <span style={{ width: 9, height: 9, flex: 'none', background: item.color }} />
            <span>{item.label}</span>
            <span className="num" style={{ color: 'var(--fg-strong)' }}>
              {item.value}
            </span>
          </span>
        ))}
        <span style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: 11, color: 'var(--fg-muted)' }}>
          <span style={{ width: 14, height: 0, borderTop: '1px dashed var(--fg-strong)' }} />
          <span className="num">{chart.meanLabel}</span>
        </span>
        <p style={{ margin: '2px 0 0', width: '100%', fontSize: 10.5, color: 'var(--fg-faint)' }}>{chart.note}</p>
      </div>
    </section>
  )
}

function ModelRow({
  bucket,
  index,
  maxCost,
  totalCost,
  fallbackState,
}: {
  bucket: Bucket
  index: number
  maxCost: number
  totalCost: number
  fallbackState: CostState
}) {
  const priced = bucket.cost.total > 0
  const state = priced ? null : fallbackState
  const pct = (bucket.cost.total / maxCost) * 92
  const share = priced ? (totalCost > 0 ? formatPercent(bucket.cost.total / totalCost) : '0%') : state
  const cost = priced ? formatMoney(bucket.cost.total) : state === 'free' ? '$0.00' : 'n/a'
  const color = priced ? SERIES[index % SERIES.length] : state ? STATE_COLOR[state] : STATE_COLOR.unavailable
  const meta = state ? `${formatCount(bucket.sessions)} sessions · ${state}` : `${formatCount(bucket.sessions)} sessions`

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '132px minmax(0,1fr) 72px', alignItems: 'center', gap: 10, padding: '5px 0' }}>
      <div style={{ minWidth: 0 }}>
        <div style={{ fontSize: 11.5, color: 'var(--fg-strong)', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
          {bucket.label}
        </div>
        <div className="num" style={{ fontSize: 9.5, color: 'var(--fg-faint)', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
          {meta}
        </div>
      </div>
      <div className="meter">
        <div className="meter__fill" style={{ width: `${pct}%`, background: color }} />
        <span className="num" style={{ position: 'absolute', top: 2, left: `calc(${pct}% + 6px)`, fontSize: 9.5, color: 'var(--fg-faint)' }}>
          {share}
        </span>
      </div>
      <div className="num" style={{ textAlign: 'right', fontSize: 12, color: 'var(--fg-strong)' }}>
        {cost}
      </div>
    </div>
  )
}

const STATE_RANK: Record<CostState, number> = { priced: 0, free: 1, unpriced: 2, unavailable: 3 }

function modelFallbackStates(report: Report): Map<string, CostState> {
  const statesByModel = new Map<string, Set<CostState>>()
  for (const session of report.sessions) {
    const states = session.cost_states.length > 0 ? session.cost_states : [session.cost_state]
    for (const model of session.models) {
      const set = statesByModel.get(model) ?? new Set<CostState>()
      for (const state of states) set.add(state)
      statesByModel.set(model, set)
    }
  }
  const unknownModels = new Set(report.unknown_models.map((unknown) => unknown.model))
  const result = new Map<string, CostState>()
  for (const [model, states] of statesByModel) {
    if (unknownModels.has(model)) {
      result.set(model, 'unpriced')
      continue
    }
    const nonPriced = [...states].filter((state) => state !== 'priced')
    const worst = nonPriced.sort((a, b) => STATE_RANK[b] - STATE_RANK[a])[0]
    result.set(model, worst ?? 'unavailable')
  }
  return result
}

function CostByModelPanel({ report }: { report: Report }) {
  const buckets = [...report.by_model].sort((a, b) => b.cost.total - a.cost.total)
  const maxCost = Math.max(...buckets.map((bucket) => bucket.cost.total), 0.01)
  const fallbackStates = modelFallbackStates(report)
  const totalCost = report.totals.cost.total
  const top = buckets[0]
  const headline = top
    ? `${top.label} carries ${totalCost > 0 ? formatPercent(top.cost.total / totalCost) : '0%'} of the spend`
    : 'No priced models in this slice'

  return (
    <section className="panel">
      <div className="panel__head">
        <div>
          <p className="lbl" style={{ color: 'var(--accent)' }}>
            Cost by model
          </p>
          <h2 className="panel__title">{headline}</h2>
        </div>
      </div>
      <div className="panel__body">
        {buckets.map((bucket, i) => (
          <ModelRow
            key={bucket.key}
            bucket={bucket}
            index={i}
            maxCost={maxCost}
            totalCost={totalCost}
            fallbackState={fallbackStates.get(bucket.key) ?? 'unavailable'}
          />
        ))}
        <p className="panel__note">
          Bars are absolute spend, the number beside each bar is its share. Free and unpriced models keep their row so nothing disappears from view.
        </p>
      </div>
    </section>
  )
}

function TokenMixRow({ bucket }: { bucket: Bucket }) {
  const total = bucket.tokens.total
  return (
    <div style={{ padding: '5px 0' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 11, color: 'var(--fg-strong)' }}>
        <span style={{ whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{bucket.label}</span>
        <span className="num" style={{ color: 'var(--fg-muted)' }}>
          {formatTokens(total)}
        </span>
      </div>
      <div style={{ display: 'flex', height: 14, marginTop: 4, background: 'var(--bg-muted)' }}>
        {BUCKETS.map((segment) => {
          const value = bucket.tokens[segment.key]
          const pct = total > 0 ? (value / total) * 100 : 0
          return <div key={segment.key} style={{ width: `${pct}%`, background: segment.color }} title={`${segment.label} ${formatTokens(value)}`} />
        })}
      </div>
    </div>
  )
}

function TokenMixPanel({ report }: { report: Report }) {
  const buckets = report.by_model.filter((bucket) => bucket.tokens.total > 0)
  const totals = report.totals.tokens
  const cacheShare = totals.total > 0 ? totals.cache_read / totals.total : 0
  const headline = `${formatPercent(cacheShare)} of all tokens are cache reads`

  return (
    <section className="panel">
      <div className="panel__head">
        <div>
          <p className="lbl" style={{ color: 'var(--accent)' }}>
            Token mix
          </p>
          <h2 className="panel__title">{headline}</h2>
        </div>
      </div>
      <div className="panel__body">
        <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap', marginBottom: 10 }}>
          {BUCKETS.map((segment) => (
            <span key={segment.key} style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: 10.5, color: 'var(--fg-muted)' }}>
              <span style={{ width: 9, height: 9, background: segment.color }} />
              {segment.label}
              <span className="num" style={{ color: 'var(--fg-strong)' }}>
                {segment.mult}
              </span>
            </span>
          ))}
        </div>
        {buckets.map((bucket) => (
          <TokenMixRow key={bucket.key} bucket={bucket} />
        ))}
        <p className="panel__note">
          Cache reads bill at a tenth of the input price, so the widest band is also the cheapest. Output is the narrow band that costs the most.
        </p>
      </div>
    </section>
  )
}

function CacheSavingsPanel({ report }: { report: Report }) {
  const cost = report.totals.cost
  const pct = cost.no_cache_equivalent > 0 ? (cost.total / cost.no_cache_equivalent) * 100 : 0
  const headline =
    cost.no_cache_equivalent > 0
      ? `Caching cut the bill by ${formatPercent(cost.cache_savings / cost.no_cache_equivalent)}`
      : 'No priced tokens in this slice'

  return (
    <section className="panel">
      <div className="panel__head">
        <div>
          <p className="lbl" style={{ color: 'var(--accent)' }}>
            Cache savings
          </p>
          <h2 className="panel__title">{headline}</h2>
        </div>
      </div>
      <div className="panel__body">
        <div style={{ position: 'relative', paddingBottom: 6 }}>
          <div style={{ fontSize: 10.5, color: 'var(--fg-muted)' }}>Same tokens billed with no cache discount</div>
          <div className="meter" style={{ height: 26, marginTop: 5 }}>
            <div className="meter__fill" style={{ width: '100%', background: 'var(--border-strong)' }} />
            <span className="num" style={{ position: 'absolute', top: 6, right: 8, fontSize: 12, fontWeight: 600, color: 'var(--fg-strong)' }}>
              {formatMoney(cost.no_cache_equivalent)}
            </span>
          </div>
        </div>
        <div style={{ marginTop: 10 }}>
          <div style={{ fontSize: 10.5, color: 'var(--fg-muted)' }}>Actually billed at cache rates</div>
          <div className="meter" style={{ height: 26, marginTop: 5 }}>
            <div className="meter__fill" style={{ width: `${pct}%` }} />
            <span className="num" style={{ position: 'absolute', top: 6, left: `calc(${pct}% + 8px)`, fontSize: 12, fontWeight: 600, color: 'var(--fg-strong)' }}>
              {formatMoney(cost.total)}
            </span>
          </div>
        </div>
        <div style={{ display: 'flex', alignItems: 'baseline', gap: 8, marginTop: 14, paddingTop: 12, borderTop: '1px solid var(--border)' }}>
          <span className="num" style={{ fontSize: 22, fontWeight: 600, color: 'var(--success)' }}>
            {formatMoney(cost.cache_savings)}
          </span>
          <span style={{ fontSize: 11, lineHeight: 1.5, color: 'var(--fg-muted)' }}>
            saved against the same tokens billed with every read and write at full input price.
          </span>
        </div>
      </div>
    </section>
  )
}

function ProjectRow({ bucket, index, maxCost }: { bucket: Bucket; index: number; maxCost: number }) {
  const pct = (bucket.cost.total / maxCost) * 100
  return (
    <div style={{ display: 'grid', gridTemplateColumns: '148px minmax(0,1fr) 72px', alignItems: 'center', gap: 10, padding: '5px 4px' }}>
      <div style={{ minWidth: 0 }}>
        <div style={{ fontSize: 11.5, color: 'var(--fg-strong)', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
          {bucket.label}
        </div>
        <div className="num" style={{ fontSize: 9.5, color: 'var(--fg-faint)', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
          {`${formatCount(bucket.sessions)} sessions · ${formatCount(bucket.events)} req`}
        </div>
      </div>
      <div className="meter" style={{ height: 14 }}>
        <div className="meter__fill" style={{ width: `${pct}%`, background: SERIES[index % SERIES.length] }} />
      </div>
      <div className="num" style={{ textAlign: 'right', fontSize: 12, color: 'var(--fg-strong)' }}>
        {formatMoney(bucket.cost.total)}
      </div>
    </div>
  )
}

function ByProjectPanel({ report }: { report: Report }) {
  const buckets = [...report.by_project].sort((a, b) => b.cost.total - a.cost.total)
  const maxCost = Math.max(...buckets.map((bucket) => bucket.cost.total), 0.01)
  const headline = buckets.length ? `${buckets.length} projects, led by ${buckets[0].label}` : 'No sessions in this slice'

  return (
    <section className="panel">
      <div className="panel__head">
        <div>
          <p className="lbl" style={{ color: 'var(--accent)' }}>
            By project
          </p>
          <h2 className="panel__title">{headline}</h2>
        </div>
      </div>
      <div className="panel__body">
        {buckets.map((bucket, i) => (
          <ProjectRow key={bucket.key} bucket={bucket} index={i} maxCost={maxCost} />
        ))}
        <p className="panel__note">Attributed from each session&rsquo;s working directory. Sessions without one land in (no project).</p>
      </div>
    </section>
  )
}

export default function Overview(props: { report: Report; meta: Meta; onSelectView: (view: View) => void }): JSX.Element {
  const { report, meta, onSelectView } = props

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
      <DetectedSourcesPanel meta={meta} report={report} onSelectView={onSelectView} />
      <KpiRow report={report} />
      <OutcomeRow report={report} />
      <HeaviestSessionsPanel report={report} />
      <TimeChartPanel report={report} meta={meta} />
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(min(380px, 100%), 1fr))', gap: 14 }}>
        <CostByModelPanel report={report} />
        <TokenMixPanel report={report} />
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(min(380px, 100%), 1fr))', gap: 14 }}>
        <CacheSavingsPanel report={report} />
        <ByProjectPanel report={report} />
      </div>
    </div>
  )
}
