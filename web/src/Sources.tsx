import { useState } from 'react'
import type { JSX } from 'react'
import type { Capabilities, Meta, Provenance, Report, SourceInfo } from './api'
import { formatCount, formatDayShort, formatMoney } from './format'
import { spark } from './chart'
import { PROVENANCE_COLOR, SERIES } from './theme'

const CAPABILITY_COLUMNS: { key: keyof Capabilities; label: string }[] = [
  { key: 'trace', label: 'Trace' },
  { key: 'tokens', label: 'Tokens' },
  { key: 'cost', label: 'Cost' },
  { key: 'context', label: 'Context' },
  { key: 'latency', label: 'Latency' },
]

const PROVENANCE_MEANING: Record<Provenance, string> = {
  measured: 'read straight out of the log',
  derived: 'computed from two logged values',
  estimated: 'from a table, not the log',
  inferred: 'read off the model id',
  unavailable: 'the log does not carry it',
}

function ProvenanceChip({ value }: { value: Provenance }) {
  const known = value !== 'unavailable'
  return (
    <span
      className="badge"
      title={`${value}: ${PROVENANCE_MEANING[value]}`}
      style={{ height: 19, gap: 5, fontSize: 9, color: known ? 'var(--fg-strong)' : 'var(--fg-faint)' }}
    >
      <span style={{ width: 6, height: 6, flex: 'none', background: PROVENANCE_COLOR[value] }} />
      {value}
    </span>
  )
}

function CapabilityMatrixPanel({ sources }: { sources: SourceInfo[] }) {
  const cell = { padding: '7px 10px', boxShadow: 'inset 0 -1px 0 var(--border)' } as const
  const head = {
    padding: '8px 10px',
    background: 'var(--bg-muted)',
    boxShadow: 'inset 0 -1px 0 var(--border)',
    fontFamily: 'var(--font-sans)',
    fontSize: 9.5,
    fontWeight: 700,
    letterSpacing: '0.12em',
    textTransform: 'uppercase',
    color: 'var(--fg-muted)',
    textAlign: 'left',
  } as const

  return (
    <section className="panel">
      <div className="panel__head" style={{ display: 'block' }}>
        <p className="lbl" style={{ color: 'var(--accent)' }}>
          Capability matrix
        </p>
        <h2 className="panel__title">{`What each of the ${formatCount(sources.length)} readers can tell you, and how it knows`}</h2>
      </div>
      <div style={{ overflowX: 'auto' }}>
        <table className="data-table">
          <thead>
            <tr>
              <th style={head}>Source</th>
              {CAPABILITY_COLUMNS.map((column) => (
                <th key={column.key} style={head}>
                  {column.label}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {sources.map((source) => (
              <tr key={source.id}>
                <td style={cell}>
                  <span style={{ color: source.detected ? 'var(--fg-strong)' : 'var(--fg-faint)' }}>{source.label}</span>
                  {!source.detected && (
                    <span className="num" style={{ marginLeft: 8, fontSize: 9.5, color: 'var(--fg-faint)' }}>
                      not detected
                    </span>
                  )}
                </td>
                {CAPABILITY_COLUMNS.map((column) => (
                  <td key={column.key} style={cell}>
                    <ProvenanceChip value={source.capabilities[column.key]} />
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p className="panel__note">
        Every number this tool shows carries where it came from. Measured is read straight out of a log, derived is
        computed from two logged values, estimated comes from a table rather than the log, inferred is read off a model
        id, and unavailable means the log does not carry it, so nothing is shown rather than a zero. Cursor is listed
        with everything unavailable on purpose: it is not installed here, so its logs could not be audited and no reader
        was written for it.
      </p>
    </section>
  )
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <div className="lbl">{label}</div>
      <div className="num" style={{ fontSize: 14, color: 'var(--fg-strong)' }}>
        {value}
      </div>
    </div>
  )
}

function perDayValues(report: Report, sourceId: string, useCost: boolean): number[] {
  const totals = new Map<string, number>()
  for (const point of report.series) {
    if (point.source !== sourceId) continue
    const value = useCost ? point.cost : point.events
    totals.set(point.day, (totals.get(point.day) ?? 0) + value)
  }
  const days = [...totals.keys()].sort()
  return days.map((day) => totals.get(day) ?? 0)
}

function SourceDetail({ source, index, report }: { source: SourceInfo; index: number; report: Report }) {
  const dot = SERIES[index % SERIES.length]
  const isFull = source.token_data === 'full'
  const ownSessions = report.sessions.filter((session) => session.source === source.id)
  const cost = ownSessions.reduce((sum, session) => sum + (session.cost ? session.cost.total : 0), 0)
  const requests = ownSessions.reduce((sum, session) => sum + session.request_count, 0)
  const lastEvent = ownSessions.reduce<string | null>(
    (latest, session) => (!latest || session.end_time > latest ? session.end_time : latest),
    null,
  )
  const headline = isFull ? formatMoney(cost) : formatCount(requests)
  const { line, area } = spark(perDayValues(report, source.id, isFull), 96, 26)

  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'minmax(170px,220px) minmax(0,1fr)', gap: '14px 20px', padding: '13px 14px', borderBottom: '1px solid var(--border)' }}>
      <div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 7 }}>
          <span style={{ width: 7, height: 7, borderRadius: '50%', background: dot }} />
          <span style={{ fontSize: 12.5, fontWeight: 600, color: 'var(--fg-strong)' }}>{source.label}</span>
        </div>
        <div className="num" style={{ marginTop: 5, fontSize: 10, color: 'var(--fg-faint)' }}>
          {source.clients.join(', ')}
        </div>
        <div className="num" style={{ marginTop: 10, fontSize: 18, fontWeight: 600, color: 'var(--fg-strong)' }}>
          {headline}
        </div>
      </div>
      <div>
        <div className="num" style={{ fontSize: 10.5, color: 'var(--fg-muted)', wordBreak: 'break-all' }}>
          {source.path}
        </div>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px 20px', marginTop: 9 }}>
          <Stat label="Files" value={formatCount(source.files)} />
          <Stat label="Sessions" value={formatCount(ownSessions.length)} />
          <Stat label="Requests" value={formatCount(requests)} />
          <Stat label="Last event" value={lastEvent ? formatDayShort(lastEvent.slice(0, 10)) : 'none'} />
        </div>
        <svg width="100%" height={34} viewBox="0 0 96 26" preserveAspectRatio="none" style={{ marginTop: 10, display: 'block' }}>
          <path d={area} fill={dot} opacity={0.14} />
          <polyline points={line} fill="none" stroke={dot} strokeWidth={1.4} vectorEffect="non-scaling-stroke" />
        </svg>
      </div>
    </div>
  )
}

function UndetectedSection({ sources }: { sources: SourceInfo[] }) {
  const [open, setOpen] = useState(false)

  return (
    <section className="panel" style={{ borderStyle: 'dashed', borderColor: 'var(--border-strong)', background: 'transparent' }}>
      <button
        type="button"
        onClick={() => setOpen((current) => !current)}
        style={{ display: 'flex', alignItems: 'center', gap: 10, width: '100%', padding: '12px 14px', border: 0, background: 'none', cursor: 'pointer', textAlign: 'left' }}
      >
        <span className="num" style={{ color: 'var(--fg-faint)' }}>
          {open ? '−' : '+'}
        </span>
        <span>
          <span className="lbl" style={{ display: 'block' }}>
            Available, not detected here
          </span>
          <span style={{ display: 'block', marginTop: 4, fontSize: 12, color: 'var(--fg-muted)' }}>
            {`${sources.length} more readers ship with the tool and found nothing here: ${sources.map((source) => source.id).join(', ')}`}
          </span>
        </span>
      </button>
      {open && (
        <div style={{ padding: '0 14px 14px' }}>
          {sources.map((source) => (
            <div
              key={source.id}
              style={{ display: 'grid', gridTemplateColumns: '200px minmax(0,1fr)', gap: 14, padding: '10px 0', borderTop: '1px solid var(--border)' }}
            >
              <div style={{ fontSize: 12, color: 'var(--fg-muted)' }}>{source.label}</div>
              <div>
                <div className="num" style={{ fontSize: 10.5, color: 'var(--fg-faint)', wordBreak: 'break-all' }}>
                  {source.path}
                </div>
                <div className="num" style={{ marginTop: 5, fontSize: 10.5, color: 'var(--fg-muted)' }}>
                  {source.root_hint}
                </div>
              </div>
            </div>
          ))}
          <p style={{ margin: '12px 0 0', fontSize: 11, lineHeight: 1.55, color: 'var(--fg-muted)', maxWidth: '78ch' }}>
            These readers ship with the tool but found nothing on this machine, so they stay out of the filter rail, the
            totals, and every chart. Give one a path and it appears everywhere on the next scan.
          </p>
        </div>
      )}
    </section>
  )
}

function ScanWarningsPanel({ warnings }: { warnings: string[] }) {
  return (
    <section className="panel">
      <div className="panel__head" style={{ display: 'block' }}>
        <p className="lbl" style={{ color: 'var(--accent)' }}>
          Scan warnings
        </p>
        <h2 className="panel__title">{`${formatCount(warnings.length)} file or parse warnings from the last scan`}</h2>
      </div>
      <div className="panel__body">
        <ul style={{ margin: 0, paddingLeft: 18, display: 'flex', flexDirection: 'column', gap: 6 }}>
          {warnings.map((warning, i) => (
            <li key={i} className="num" style={{ fontSize: 11, lineHeight: 1.5, color: 'var(--fg-muted)' }}>
              {warning}
            </li>
          ))}
        </ul>
      </div>
    </section>
  )
}

export default function Sources(props: { report: Report; meta: Meta }): JSX.Element {
  const { report, meta } = props
  const detected = meta.sources.filter((source) => source.detected)
  const undetected = meta.sources.filter((source) => !source.detected)
  const withTokens = detected.filter((source) => source.token_data === 'full').length
  const headline = `${formatCount(detected.length)} readers found logs, ${formatCount(withTokens)} of them with token counts`

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
      <CapabilityMatrixPanel sources={meta.sources} />

      <section className="panel">
        <div className="panel__head" style={{ display: 'block' }}>
          <p className="lbl" style={{ color: 'var(--accent)' }}>
            Readers with data
          </p>
          <h2 className="panel__title">{headline}</h2>
        </div>
        <div>
          {detected.map((source, i) => (
            <SourceDetail key={source.id} source={source} index={i} report={report} />
          ))}
        </div>
      </section>

      {undetected.length > 0 && <UndetectedSection sources={undetected} />}

      {report.scan_warnings.length > 0 && <ScanWarningsPanel warnings={report.scan_warnings} />}
    </div>
  )
}
