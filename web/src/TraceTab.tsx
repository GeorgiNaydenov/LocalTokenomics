import { useEffect, useState } from 'react'
import type { CSSProperties, JSX } from 'react'
import type { Capabilities, Insight, Provenance, Span, SpanContent, SpanKind, SpanStatus } from './api'
import { ApiError, fetchSpanContent } from './api'
import { ProvenanceChip, Unavailable } from './SessionWorkspace'
import { formatClock, formatCount, formatDuration, formatTokens } from './format'
import { PROVENANCE_COLOR, SPAN_KIND_GLYPH } from './theme'
import type { TraceTabProps } from './SessionWorkspace'

type Mode = 'timeline' | 'tree'

const INITIAL_ROWS = 200
const ROW_BATCH = 400
const INITIAL_INSIGHTS = 6
const INSIGHT_BATCH = 20

const PROVENANCE_RANK: Record<Provenance, number> = {
  measured: 0,
  derived: 1,
  estimated: 2,
  inferred: 3,
  unavailable: 4,
}

const STATUS_COLOR: Record<SpanStatus, string> = {
  ok: 'var(--success)',
  error: 'var(--rose)',
  interrupted: 'var(--bubble-c-3)',
  aborted: 'var(--bubble-c-7)',
  running: 'var(--accent)',
  unknown: 'var(--fg-faint)',
}

const SEVERITY_COLOR: Record<Insight['severity'], string> = {
  info: 'var(--fg-muted)',
  warning: 'var(--bubble-c-3)',
  critical: 'var(--rose)',
}

const CAPABILITY_LABELS: { key: keyof Capabilities; label: string }[] = [
  { key: 'trace', label: 'trace' },
  { key: 'latency', label: 'latency' },
  { key: 'tokens', label: 'tokens' },
  { key: 'context', label: 'context' },
  { key: 'cost', label: 'cost' },
]

interface Row {
  span: Span
  depth: number
  descendants: number
  subtreeTokens: number
  subtreeTokensProvenance: Provenance
  subtreeDuration: number | null
  subtreeDurationProvenance: Provenance
}

type ContentState =
  | { status: 'loading' }
  | { status: 'ready'; content: SpanContent }
  | { status: 'off' }
  | { status: 'error'; message: string }

function worstProvenance(values: Provenance[]): Provenance {
  const sorted = [...values].sort((a, b) => PROVENANCE_RANK[b] - PROVENANCE_RANK[a])
  return sorted[0] ?? 'unavailable'
}

function rowDomId(spanId: string): string {
  return `trace-span-${spanId}`
}

function spanLabel(span: Span): string {
  return span.name ?? span.model ?? span.kind
}

function isMissing(cause: unknown): boolean {
  return cause instanceof ApiError && cause.message.includes('404')
}

function messageOf(cause: unknown): string {
  return cause instanceof ApiError ? cause.message : String(cause)
}

function DurationCell({
  ms,
  provenance,
  descendants,
}: {
  ms: number | null
  provenance: Provenance
  descendants: number
}) {
  if (ms === null) return <Unavailable hint="duration" />
  const scope = descendants > 0 ? `summed over ${formatCount(descendants + 1)} spans` : 'this span'
  return (
    <span style={{ display: 'inline-flex', alignItems: 'center', gap: 5 }}>
      <span className="num" style={{ fontSize: 11, color: 'var(--fg-strong)' }}>
        {formatDuration(ms)}
      </span>
      <ProvenanceChip provenance={provenance} title={`Duration, ${scope}: ${provenance}`} />
    </span>
  )
}

function TokensCell({
  total,
  provenance,
  descendants,
}: {
  total: number
  provenance: Provenance
  descendants: number
}) {
  if (provenance === 'unavailable') return null
  const scope = descendants > 0 ? `summed over ${formatCount(descendants + 1)} spans` : 'this span'
  return (
    <span style={{ display: 'inline-flex', alignItems: 'center', gap: 5 }}>
      <span className="num" style={{ fontSize: 11, color: 'var(--fg-muted)' }} title={`${formatCount(total)} tokens`}>
        {formatTokens(total)}
      </span>
      <ProvenanceChip provenance={provenance} title={`Tokens, ${scope}: ${provenance}`} />
    </span>
  )
}

function ContentBlock({ state }: { state: ContentState }) {
  const frame: CSSProperties = { marginTop: 8, display: 'flex', flexDirection: 'column', gap: 5 }
  switch (state.status) {
    case 'loading':
      return (
        <div style={frame}>
          <span style={{ fontSize: 11, color: 'var(--fg-muted)' }}>Reading the record…</span>
        </div>
      )
    case 'off':
      return (
        <div style={frame}>
          <span style={{ fontSize: 11, lineHeight: 1.5, color: 'var(--fg-muted)' }}>
            Content capture is off (metadata-only). Nothing is read back from your logs until you set
            <span className="num"> metadata_only: false</span> in <span className="num">~/.ai-usage-cost/config.json</span>.
            The same answer covers a record whose file has moved since the scan.
          </span>
        </div>
      )
    case 'error':
      return (
        <div style={frame}>
          <span style={{ fontSize: 11, color: 'var(--rose)' }}>{state.message}</span>
        </div>
      )
    case 'ready': {
      const { content, truncated, redactions } = state.content
      return (
        <div style={frame}>
          <pre className="code">{content}</pre>
          <span style={{ fontSize: 10.5, color: 'var(--fg-faint)' }}>
            {truncated ? 'Truncated at the configured byte limit. ' : ''}
            {redactions > 0
              ? `${formatCount(redactions)} secret${redactions === 1 ? '' : 's'} redacted before display.`
              : 'Nothing matched a redaction pattern.'}
          </span>
        </div>
      )
    }
  }
}

function TraceRow({
  row,
  mode,
  focused,
  expanded,
  content,
  onToggle,
}: {
  row: Row
  mode: Mode
  focused: boolean
  expanded: boolean
  content: ContentState | undefined
  onToggle: () => void
}) {
  const { span, depth } = row
  const rolled = mode === 'tree' && row.descendants > 0
  const label = spanLabel(span)
  const durationMs = rolled ? row.subtreeDuration : span.duration_ms
  const durationProvenance = rolled ? row.subtreeDurationProvenance : span.duration_provenance
  const tokensTotal = rolled ? row.subtreeTokens : (span.tokens?.total ?? 0)
  const tokensProvenance = rolled ? row.subtreeTokensProvenance : span.tokens_provenance

  return (
    <div
      id={rowDomId(span.span_id)}
      role="listitem"
      aria-label={`${span.kind} ${label}, status ${span.status}`}
      className="row-hit"
      style={{
        padding: '6px 8px 6px 0',
        paddingLeft: 8 + depth * 13,
        borderBottom: '1px solid var(--border)',
        borderLeft: focused ? '3px solid var(--accent)' : '3px solid transparent',
        background: focused ? 'var(--accent-soft)' : undefined,
      }}
    >
      <div style={{ display: 'flex', alignItems: 'center', gap: 8, flexWrap: 'wrap' }}>
        <span aria-hidden="true" style={{ width: 12, flex: 'none', color: 'var(--fg-faint)', fontSize: 12 }}>
          {SPAN_KIND_GLYPH[span.kind]}
        </span>
        <span style={{ minWidth: 0, flex: '1 1 190px', display: 'flex', alignItems: 'baseline', gap: 6 }}>
          <span
            style={{
              fontSize: 11.5,
              color: 'var(--fg-strong)',
              whiteSpace: 'nowrap',
              overflow: 'hidden',
              textOverflow: 'ellipsis',
            }}
          >
            {label}
          </span>
          <span className="lbl" style={{ flex: 'none', fontSize: 8.5, color: 'var(--fg-faint)' }}>
            {span.kind}
          </span>
        </span>
        <span className="num" style={{ flex: 'none', fontSize: 10.5, color: 'var(--fg-faint)' }}>
          {formatClock(span.started_at)}
        </span>
        <TokensCell total={tokensTotal} provenance={tokensProvenance} descendants={rolled ? row.descendants : 0} />
        <DurationCell
          ms={durationMs}
          provenance={durationProvenance}
          descendants={rolled ? row.descendants : 0}
        />
        <span
          className="badge"
          style={{
            flex: 'none',
            fontSize: 9,
            padding: '1px 5px',
            borderColor: STATUS_COLOR[span.status],
            color: STATUS_COLOR[span.status],
          }}
        >
          {span.status}
        </span>
        {span.content_path === null ? (
          <span style={{ flex: 'none', width: 62, fontSize: 9.5, color: 'var(--fg-faint)', textAlign: 'right' }}>
            no text
          </span>
        ) : (
          <button
            type="button"
            className="chip"
            aria-expanded={expanded}
            onClick={onToggle}
            style={{ flex: 'none', height: 20, fontSize: 9, padding: '0 8px' }}
          >
            {expanded ? 'Hide' : 'Text'}
          </button>
        )}
      </div>
      {span.error && (
        <p className="num" style={{ margin: '4px 0 0 20px', fontSize: 10.5, lineHeight: 1.5, color: 'var(--rose)' }}>
          {span.error}
        </p>
      )}
      {expanded && content && <ContentBlock state={content} />}
    </div>
  )
}

function InsightList({
  insights,
  onFocus,
}: {
  insights: Insight[]
  onFocus: (spanId: string) => void
}) {
  const [revealed, setRevealed] = useState(0)
  if (insights.length === 0) return null
  const shown = insights.slice(0, INITIAL_INSIGHTS + revealed * INSIGHT_BATCH)
  const hidden = insights.length - shown.length

  return (
    <section className="panel">
      <div className="panel__head">
        <div>
          <p className="lbl" style={{ color: 'var(--accent)' }}>
            Insights
          </p>
          <h2 className="panel__title">{`${formatCount(insights.length)} things worth a look in this session`}</h2>
        </div>
      </div>
      <div className="panel__body" style={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
        {shown.map((insight, index) => (
          <button
            key={`${insight.kind}-${insight.span_id}-${index}`}
            type="button"
            className="row-hit"
            onClick={() => onFocus(insight.span_id)}
            style={{
              display: 'flex',
              alignItems: 'baseline',
              gap: 8,
              width: '100%',
              padding: '6px 4px',
              border: 0,
              borderBottom: '1px solid var(--border)',
              background: 'transparent',
              textAlign: 'left',
              cursor: 'pointer',
              fontFamily: 'var(--font-sans)',
            }}
          >
            <span
              className="badge"
              style={{
                flex: 'none',
                fontSize: 9,
                padding: '1px 5px',
                borderColor: SEVERITY_COLOR[insight.severity],
                color: SEVERITY_COLOR[insight.severity],
              }}
            >
              {insight.severity}
            </span>
            <span style={{ flex: '1 1 auto', fontSize: 11.5, lineHeight: 1.5, color: 'var(--fg-strong)' }}>
              {insight.message}
            </span>
            <span className="lbl" style={{ flex: 'none', fontSize: 8.5, color: 'var(--fg-faint)' }}>
              {insight.kind}
            </span>
          </button>
        ))}
        {hidden > 0 && (
          <button
            type="button"
            className="chip"
            onClick={() => setRevealed((current) => current + 1)}
            style={{ alignSelf: 'flex-start', marginTop: 8, height: 24, fontSize: 10, padding: '0 9px' }}
          >
            {`Show ${Math.min(INSIGHT_BATCH, hidden)} more (${formatCount(hidden)} hidden)`}
          </button>
        )}
        <p className="panel__note">Each line points at one span. Selecting it scrolls the rows below to that span.</p>
      </div>
    </section>
  )
}

function depthMap(spans: Span[]): Map<string, number> {
  const byId = new Map(spans.map((span) => [span.span_id, span]))
  const depths = new Map<string, number>()
  for (const span of spans) {
    const chain: string[] = []
    let cursor: Span | undefined = span
    let depth = 0
    while (cursor) {
      const known = depths.get(cursor.span_id)
      if (known !== undefined) {
        depth = known + 1
        break
      }
      if (chain.includes(cursor.span_id)) break
      chain.push(cursor.span_id)
      cursor = cursor.parent_id ? byId.get(cursor.parent_id) : undefined
    }
    for (let i = chain.length - 1; i >= 0; i -= 1) {
      depths.set(chain[i], depth)
      depth += 1
    }
  }
  return depths
}

interface Subtree {
  descendants: number
  tokens: number
  tokensProvenance: Provenance
  duration: number | null
  durationProvenance: Provenance
}

function buildRows(spans: Span[], mode: Mode, visible: Set<string>): Row[] {
  const byId = new Map(spans.map((span) => [span.span_id, span]))
  const children = new Map<string, Span[]>()
  const roots: Span[] = []
  for (const span of spans) {
    const parent = span.parent_id && byId.has(span.parent_id) ? span.parent_id : null
    if (parent === null) {
      roots.push(span)
      continue
    }
    const siblings = children.get(parent)
    if (siblings) siblings.push(span)
    else children.set(parent, [span])
  }

  const subtrees = new Map<string, Subtree>()
  const collect = (span: Span): Subtree => {
    const cached = subtrees.get(span.span_id)
    if (cached) return cached
    const placeholder: Subtree = {
      descendants: 0,
      tokens: span.tokens?.total ?? 0,
      tokensProvenance: span.tokens_provenance,
      duration: span.duration_ms,
      durationProvenance: span.duration_provenance,
    }
    subtrees.set(span.span_id, placeholder)
    let descendants = 0
    let tokens = span.tokens?.total ?? 0
    let duration = span.duration_ms
    const tokenSources: Provenance[] = span.tokens ? [span.tokens_provenance] : []
    const durationSources: Provenance[] = span.duration_ms === null ? [] : [span.duration_provenance]
    for (const child of children.get(span.span_id) ?? []) {
      const sub = collect(child)
      descendants += sub.descendants + 1
      tokens += sub.tokens
      if (sub.tokensProvenance !== 'unavailable') tokenSources.push(sub.tokensProvenance)
      if (sub.duration !== null) {
        duration = (duration ?? 0) + sub.duration
        durationSources.push(sub.durationProvenance)
      }
    }
    const result: Subtree = {
      descendants,
      tokens,
      tokensProvenance: tokenSources.length > 0 ? worstProvenance(tokenSources) : 'unavailable',
      duration: durationSources.length > 0 ? duration : null,
      durationProvenance: durationSources.length > 0 ? worstProvenance(durationSources) : 'unavailable',
    }
    subtrees.set(span.span_id, result)
    return result
  }
  for (const span of spans) collect(span)

  const depths = depthMap(spans)
  const rowOf = (span: Span): Row => {
    const subtree = subtrees.get(span.span_id)
    return {
      span,
      depth: depths.get(span.span_id) ?? 0,
      descendants: subtree ? subtree.descendants : 0,
      subtreeTokens: subtree ? subtree.tokens : 0,
      subtreeTokensProvenance: subtree ? subtree.tokensProvenance : 'unavailable',
      subtreeDuration: subtree ? subtree.duration : null,
      subtreeDurationProvenance: subtree ? subtree.durationProvenance : 'unavailable',
    }
  }

  if (mode === 'timeline') {
    return spans.filter((span) => visible.has(span.span_id)).map(rowOf)
  }

  const rows: Row[] = []
  const seen = new Set<string>()
  const walk = (span: Span) => {
    if (seen.has(span.span_id)) return
    seen.add(span.span_id)
    if (visible.has(span.span_id)) rows.push(rowOf(span))
    for (const child of children.get(span.span_id) ?? []) walk(child)
  }
  for (const root of roots) walk(root)
  for (const span of spans) walk(span)
  return rows
}

function visibleSpanIds(
  spans: Span[],
  kinds: SpanKind[],
  errorsOnly: boolean,
  keepAncestors: boolean,
): Set<string> {
  const byId = new Map(spans.map((span) => [span.span_id, span]))
  const matched = spans.filter((span) => {
    if (kinds.length > 0 && !kinds.includes(span.kind)) return false
    if (errorsOnly && span.status !== 'error' && span.kind !== 'error') return false
    return true
  })
  const visible = new Set(matched.map((span) => span.span_id))
  if (!keepAncestors || (kinds.length === 0 && !errorsOnly)) return visible
  for (const span of matched) {
    let parentId = span.parent_id
    for (let guard = 0; guard < 64 && parentId; guard += 1) {
      if (visible.has(parentId)) break
      visible.add(parentId)
      parentId = byId.get(parentId)?.parent_id ?? null
    }
  }
  return visible
}

export default function TraceTab(props: TraceTabProps): JSX.Element {
  const { source, sessionId, trace, focusSpanId } = props
  const [mode, setMode] = useState<Mode>('timeline')
  const [kinds, setKinds] = useState<SpanKind[]>([])
  const [errorsOnly, setErrorsOnly] = useState(false)
  const [revealed, setRevealed] = useState(0)
  const [picked, setPicked] = useState<string | null>(null)
  const [expanded, setExpanded] = useState<string[]>([])
  const [contents, setContents] = useState<Record<string, ContentState>>({})

  const focused = picked ?? focusSpanId
  const spans = trace.spans
  const visible = visibleSpanIds(spans, kinds, errorsOnly, mode === 'tree')
  const rows = buildRows(spans, mode, visible)
  const focusIndex = focused ? rows.findIndex((row) => row.span.span_id === focused) : -1
  const budget = Math.max(INITIAL_ROWS + revealed * ROW_BATCH, focusIndex + 1)
  const shown = rows.slice(0, budget)
  const hidden = rows.length - shown.length

  useEffect(() => {
    if (!focused) return
    document.getElementById(rowDomId(focused))?.scrollIntoView({ block: 'center' })
  }, [focused, mode])

  const kindCounts = new Map<SpanKind, number>()
  for (const span of spans) kindCounts.set(span.kind, (kindCounts.get(span.kind) ?? 0) + 1)

  const toggleKind = (kind: SpanKind) => {
    setKinds((current) => (current.includes(kind) ? current.filter((item) => item !== kind) : [...current, kind]))
    setRevealed(0)
  }

  const toggleContent = (span: Span) => {
    const alreadyOpen = expanded.includes(span.span_id)
    setExpanded((current) =>
      alreadyOpen ? current.filter((id) => id !== span.span_id) : [...current, span.span_id],
    )
    if (alreadyOpen || contents[span.span_id]) return
    setContents((current) => ({ ...current, [span.span_id]: { status: 'loading' } }))
    fetchSpanContent(source, sessionId, span.span_id)
      .then((content) => setContents((current) => ({ ...current, [span.span_id]: { status: 'ready', content } })))
      .catch((cause: unknown) => {
        const next: ContentState = isMissing(cause) ? { status: 'off' } : { status: 'error', message: messageOf(cause) }
        setContents((current) => ({ ...current, [span.span_id]: next }))
      })
  }

  const focusSpan = (spanId: string) => {
    setPicked(spanId)
    const index = rows.findIndex((row) => row.span.span_id === spanId)
    if (index >= budget) setRevealed(Math.ceil((index + 1 - INITIAL_ROWS) / ROW_BATCH))
  }

  return (
    <>
      <section className="panel">
        <div className="panel__head" style={{ alignItems: 'center', flexWrap: 'wrap', gap: 10 }}>
          <div>
            <p className="lbl" style={{ color: 'var(--accent)' }}>
              Trace
            </p>
            <h2 className="panel__title">
              {`${formatCount(spans.length)} spans, ${formatCount(rows.length)} in view`}
            </h2>
          </div>
          <div style={{ marginLeft: 'auto', display: 'flex', gap: 4 }}>
            {(['timeline', 'tree'] as const).map((option) => (
              <button
                key={option}
                type="button"
                className={`chip${mode === option ? ' is-active' : ''}`}
                style={{ height: 26, fontSize: 11, padding: '0 10px' }}
                onClick={() => setMode(option)}
              >
                {option === 'timeline' ? 'Timeline' : 'Agent tree'}
              </button>
            ))}
          </div>
        </div>
        <div className="panel__body" style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
          <div className="chip-row">
            {CAPABILITY_LABELS.map((entry) => (
              <span
                key={entry.key}
                className="chip"
                style={{ height: 22, fontSize: 9, padding: '0 8px', cursor: 'default' }}
              >
                <span className="chip__group" style={{ fontSize: 9 }}>
                  {entry.label}
                </span>
                <span style={{ color: PROVENANCE_COLOR[trace.capabilities[entry.key]] }}>
                  {trace.capabilities[entry.key]}
                </span>
              </span>
            ))}
          </div>
          <div className="chip-row">
            {[...kindCounts.entries()].map(([kind, count]) => (
              <button
                key={kind}
                type="button"
                className={`chip${kinds.includes(kind) ? ' is-active' : ''}`}
                style={{ height: 24, fontSize: 10, padding: '0 9px' }}
                onClick={() => toggleKind(kind)}
              >
                {kind}
                <span className="chip__count">{formatCount(count)}</span>
              </button>
            ))}
            <button
              type="button"
              className={`chip${errorsOnly ? ' is-active' : ''}`}
              aria-pressed={errorsOnly}
              style={{ height: 24, fontSize: 10, padding: '0 9px' }}
              onClick={() => {
                setErrorsOnly(!errorsOnly)
                setRevealed(0)
              }}
            >
              Errors only
            </button>
          </div>
          <p className="panel__note">
            {mode === 'timeline'
              ? 'Rows in log order, indented by their place in the tree. Every duration and token figure carries the word for where it came from.'
              : 'Rows grouped under their turn and subagent. A row with children shows its subtree summed, labelled with the weakest provenance in that subtree.'}
          </p>
        </div>
      </section>

      <InsightList insights={trace.insights} onFocus={focusSpan} />

      <section className="panel">
        <div className="panel__body" style={{ padding: 0 }}>
          <div role="list" aria-label="Trace spans">
            {shown.map((row) => (
              <TraceRow
                key={row.span.span_id}
                row={row}
                mode={mode}
                focused={row.span.span_id === focused}
                expanded={expanded.includes(row.span.span_id)}
                content={contents[row.span.span_id]}
                onToggle={() => toggleContent(row.span)}
              />
            ))}
          </div>
          {shown.length === 0 && (
            <p style={{ margin: 0, padding: 14, fontSize: 11.5, color: 'var(--fg-muted)' }}>
              No span matches these filters.
            </p>
          )}
          {hidden > 0 && (
            <div style={{ padding: 10 }}>
              <button type="button" className="chip" onClick={() => setRevealed((current) => current + 1)}>
                {`Show ${formatCount(Math.min(ROW_BATCH, hidden))} more spans (${formatCount(hidden)} hidden)`}
              </button>
            </div>
          )}
        </div>
      </section>
    </>
  )
}
