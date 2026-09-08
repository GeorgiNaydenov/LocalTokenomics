import { useState } from 'react'
import type { JSX } from 'react'
import type { ContextSnapshot, Provenance } from './api'
import type { ContextTabProps } from './SessionWorkspace'
import { contextBars } from './chart'
import { ProvenanceChip, Unavailable } from './SessionWorkspace'
import { formatClock, formatCount, formatPercent, formatTokens } from './format'

const REVEAL_BATCH = 60
const CHART_W = 1200
const CHART_H = 56
const HIGH_OCCUPANCY = 0.85
const MAX_CONTRIBUTORS = 6

const CAPACITY_NOTE: Record<Provenance, string> = {
  measured: 'The client logged this model’s context window for this call.',
  derived: 'Computed from other logged values on this call.',
  estimated: 'Read from the rate table for this model, not from the log.',
  inferred: 'Inferred from the model id — a [1m] suffix means a one million token window.',
  unavailable: 'No context window is known for this model, so no bar is drawn.',
}

const OCCUPANCY_NOTE: Record<Provenance, string> = {
  measured: 'Both the input total and the capacity came straight from the log.',
  derived: 'Logged input tokens over the logged context window.',
  estimated: 'Logged input tokens over an estimated capacity, so the percentage is only as good as that estimate.',
  inferred: 'Logged input tokens over a capacity inferred from the model id.',
  unavailable: 'Needs both an input total and a capacity; one of them is missing.',
}

function shortId(spanId: string): string {
  return spanId.length > 16 ? `${spanId.slice(0, 6)}…${spanId.slice(-6)}` : spanId
}

function deltaLabel(delta: number): string {
  return `${delta >= 0 ? '+' : '−'}${formatTokens(Math.abs(delta))}`
}

function OccupancyMeter({ snapshot }: { snapshot: ContextSnapshot }) {
  if (snapshot.occupancy === null || snapshot.capacity === null) {
    return (
      <div style={{ fontSize: 11 }}>
        <Unavailable hint={OCCUPANCY_NOTE[snapshot.occupancy_provenance]} />
        <span style={{ marginLeft: 6, color: 'var(--fg-faint)', fontSize: 10.5 }}>
          {snapshot.capacity === null ? 'no capacity known for this model' : 'no input total on this call'}
        </span>
      </div>
    )
  }
  const pct = Math.min(snapshot.occupancy, 1) * 100
  const flip = pct > 55
  return (
    <div className="meter" style={{ height: 18 }}>
      <div
        className="meter__fill"
        style={{
          width: `${pct}%`,
          background: snapshot.occupancy >= HIGH_OCCUPANCY ? 'var(--bubble-c-3)' : 'var(--accent)',
        }}
      />
      <span
        className="num"
        style={{
          position: 'absolute',
          top: 0,
          left: `${pct}%`,
          height: '100%',
          display: 'flex',
          alignItems: 'center',
          padding: '0 6px',
          fontSize: 9.5,
          whiteSpace: 'nowrap',
          color: flip ? 'var(--bg-panel)' : 'var(--fg-muted)',
          transform: flip ? 'translateX(-100%)' : 'none',
        }}
      >
        {`${formatPercent(snapshot.occupancy)} of ${formatTokens(snapshot.capacity)}`}
      </span>
    </div>
  )
}

function SnapshotRow({ snapshot, onFocusSpan }: { snapshot: ContextSnapshot; onFocusSpan: (spanId: string) => void }) {
  const contributors = snapshot.added_span_ids.slice(0, MAX_CONTRIBUTORS)
  const restCount = snapshot.added_span_ids.length - contributors.length

  return (
    <>
      {snapshot.compacted_before && (
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: 8,
            padding: '4px 0',
            fontSize: 10.5,
            color: 'var(--bubble-c-3)',
          }}
        >
          <span aria-hidden="true">{'⇥'}</span>
          compacted before this call — the context was replaced, so the drop below is not the model forgetting
          <span style={{ flex: 1, height: 1, background: 'var(--border)' }} />
        </div>
      )}
      <div className="row-card">
        <div style={{ display: 'flex', flexWrap: 'wrap', alignItems: 'baseline', gap: 8 }}>
          <span className="num" style={{ fontSize: 11, color: 'var(--fg-faint)' }}>
            {formatClock(snapshot.started_at)}
          </span>
          <span style={{ fontSize: 11.5, color: 'var(--fg-strong)' }}>{snapshot.model ?? 'no model id'}</span>
          <span style={{ marginLeft: 'auto', display: 'flex', flexWrap: 'wrap', alignItems: 'center', gap: 10, fontSize: 11 }}>
            <span className="num" title={`${formatCount(snapshot.input_total ?? 0)} input tokens`}>
              {snapshot.input_total === null ? (
                <Unavailable hint="This call logs no input token count." />
              ) : (
                `${formatTokens(snapshot.input_total)} in`
              )}
            </span>
            <span className="num" style={{ color: 'var(--fg-muted)' }}>
              {snapshot.delta_input === null ? (
                <Unavailable hint="The first call of this session or agent has nothing to compare against. This is an absence, not a zero." />
              ) : (
                `${deltaLabel(snapshot.delta_input)} since the previous call`
              )}
            </span>
          </span>
        </div>

        <OccupancyMeter snapshot={snapshot} />

        <div style={{ display: 'flex', flexWrap: 'wrap', alignItems: 'center', gap: 6 }}>
          <ProvenanceChip
            group="capacity"
            provenance={snapshot.capacity_provenance}
            title={CAPACITY_NOTE[snapshot.capacity_provenance]}
          />
          <ProvenanceChip
            group="occupancy"
            provenance={snapshot.occupancy_provenance}
            title={OCCUPANCY_NOTE[snapshot.occupancy_provenance]}
          />
          <ProvenanceChip
            group="tokens"
            provenance={snapshot.tokens_provenance}
            title={
              snapshot.tokens_provenance === 'measured'
                ? 'The input total came from the client’s own usage record.'
                : 'The input total did not come straight from a usage record.'
            }
          />
          {contributors.map((spanId) => (
            <button
              key={spanId}
              type="button"
              className="chip"
              onClick={() => onFocusSpan(spanId)}
              title={`Show ${spanId} in the trace`}
              style={{ height: 22, fontSize: 9, padding: '0 8px' }}
            >
              <span className="chip__group" style={{ fontSize: 8.5 }}>
                added
              </span>
              {shortId(spanId)}
            </button>
          ))}
          {restCount > 0 && (
            <span style={{ fontSize: 10, color: 'var(--fg-faint)' }}>{`+${formatCount(restCount)} more contributors`}</span>
          )}
          {snapshot.added_span_ids.length === 0 && (
            <span style={{ fontSize: 10, color: 'var(--fg-faint)' }}>no new records between this call and the last</span>
          )}
        </div>
      </div>
    </>
  )
}

function Sparkline({ snapshots }: { snapshots: ContextSnapshot[] }) {
  const chart = contextBars(snapshots, CHART_W, CHART_H)
  return (
    <div className="panel__body">
      <svg
        width="100%"
        height={CHART_H}
        viewBox={`0 0 ${CHART_W} ${CHART_H}`}
        preserveAspectRatio="none"
        role="img"
        aria-label={`Context occupancy over ${snapshots.length} model calls`}
        style={{ display: 'block', background: 'var(--bg-muted)' }}
      >
        <defs>
          <pattern id="context-unknown" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
            <rect width="6" height="6" fill="var(--bg-muted)" />
            <line x1="0" y1="0" x2="0" y2="6" stroke="var(--border-strong)" strokeWidth="2" />
          </pattern>
        </defs>
        {chart.bars.map((bar) => (
          <rect
            key={bar.spanId}
            x={bar.x}
            y={bar.y}
            width={bar.w}
            height={bar.h}
            fill={bar.unknown ? 'url(#context-unknown)' : bar.fill}
            opacity={bar.unknown ? 0.7 : 1}
          >
            <title>{bar.title}</title>
          </rect>
        ))}
        {chart.meanY !== null && (
          <line x1={0} x2={CHART_W} y1={chart.meanY} y2={chart.meanY} stroke="var(--fg-faint)" strokeWidth={1} strokeDasharray="4 4" />
        )}
        {chart.maxY !== null && (
          <line x1={0} x2={CHART_W} y1={chart.maxY} y2={chart.maxY} stroke="var(--accent)" strokeWidth={1} strokeDasharray="2 3" />
        )}
      </svg>
      <p style={{ margin: '8px 0 0', fontSize: 10.5, lineHeight: 1.5, color: 'var(--fg-muted)' }}>
        {`One bar per model call, oldest first. ${chart.maxLabel}, ${chart.meanLabel}. `}
        {chart.unknown > 0
          ? `${formatCount(chart.known)} of ${formatCount(snapshots.length)} calls have a known occupancy; the ${formatCount(
              chart.unknown,
            )} hatched full-height bars are calls whose occupancy could not be worked out, not calls at zero.`
          : `All ${formatCount(chart.known)} calls have a known occupancy.`}
      </p>
    </div>
  )
}

export default function ContextTab(props: ContextTabProps): JSX.Element {
  const [revealed, setRevealed] = useState(REVEAL_BATCH)
  const snapshots = props.snapshots

  if (snapshots.length === 0) {
    return (
      <div className="empty-state">
        <strong>No context snapshots</strong>
        <span style={{ fontSize: 11.5, lineHeight: 1.55 }}>
          A snapshot needs a model call with an input token count. This session has none, so occupancy is left blank
          rather than drawn as an empty bar.
        </span>
      </div>
    )
  }

  const shown = snapshots.slice(0, revealed)
  const hidden = snapshots.length - shown.length

  return (
    <>
      <section className="panel">
        <div className="panel__head">
          <div>
            <p className="lbl" style={{ color: 'var(--accent)' }}>
              Context
            </p>
            <h2 className="panel__title">{`${formatCount(snapshots.length)} model calls, occupancy over the session`}</h2>
          </div>
        </div>
        <Sparkline snapshots={snapshots} />
        {props.source === 'claude-code' && (
          <div className="panel__body" style={{ paddingTop: 0 }}>
            <p className="panel__note">
              Claude Code logs no context window and no server-side context. Capacity here is estimated from the rate
              table for the model, and the contributors below are reconstructed from the records visible in the log
              between one call and the next. The real prompt the server assembled may hold more than this.
            </p>
          </div>
        )}
      </section>

      <section style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
        {shown.map((snapshot) => (
          <SnapshotRow key={snapshot.span_id} snapshot={snapshot} onFocusSpan={props.onFocusSpan} />
        ))}
      </section>

      {hidden > 0 && (
        <button type="button" className="chip" onClick={() => setRevealed(revealed + REVEAL_BATCH)} style={{ alignSelf: 'flex-start' }}>
          {`Show ${Math.min(REVEAL_BATCH, hidden)} more calls (${formatCount(hidden)} hidden)`}
        </button>
      )}
    </>
  )
}
