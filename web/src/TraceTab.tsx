import { useEffect, useState } from 'react'
import type { JSX, ReactNode } from 'react'
import type { Capabilities, Insight, Provenance, Span, SpanContent, SpanKind } from './api'
import { ApiError, fetchSpanContent } from './api'
import { formatClock, formatCount, formatDuration, formatExact, formatTokens } from './format'
import type { TraceTabProps } from './SessionWorkspace'
import { Panel, PanelBody, PanelHeader, PanelNote } from '@/components/panel'
import { ProvenanceBadge, Unavailable } from '@/components/status'
import { CodeBlock } from '@/components/detail'
import { EmptyState } from '@/components/states'
import type { TraceSpanRow } from '@/components/trace'
import { InsightList, SPAN_STATUS_COLOR, SpanTimeline } from '@/components/trace'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Toggle } from '@/components/ui/toggle'
import { ToggleGroup, ToggleGroupItem } from '@/components/ui/toggle-group'
import { Tooltip, TooltipContent, TooltipTrigger } from '@/components/ui/tooltip'

type Mode = 'timeline' | 'tree'

const INITIAL_ROWS = 200
const ROW_BATCH = 400

const PROVENANCE_RANK: Record<Provenance, number> = {
  measured: 0,
  derived: 1,
  estimated: 2,
  inferred: 3,
  unavailable: 4,
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
  if (ms === null) return <Unavailable />
  const scope = descendants > 0 ? `summed over ${formatCount(descendants + 1)} spans` : 'this span'
  return (
    <span className="inline-flex items-center gap-1.5">
      <span className="tabular text-foreground">{formatDuration(ms)}</span>
      <ProvenanceBadge
        provenance={provenance}
        title={descendants > 0 ? `Duration, ${scope}: ${provenance}` : undefined}
      />
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
    <span className="inline-flex items-center gap-1.5">
      <Tooltip>
        <TooltipTrigger asChild>
          <span className="tabular cursor-default">{formatTokens(total)}</span>
        </TooltipTrigger>
        <TooltipContent>
          <span className="tabular">{formatExact(total)}</span>
        </TooltipContent>
      </Tooltip>
      <ProvenanceBadge
        provenance={provenance}
        title={descendants > 0 ? `Tokens, ${scope}: ${provenance}` : undefined}
      />
    </span>
  )
}

function ContentBlock({ state }: { state: ContentState }) {
  switch (state.status) {
    case 'loading':
      return <p className="text-[11px] text-muted-foreground">Reading the record…</p>
    case 'off':
      return (
        <p className="max-w-prose text-[11px] leading-relaxed text-muted-foreground">
          Content capture is off (metadata-only). Nothing is read back from your logs until you set
          <span className="tabular"> metadata_only: false</span> in{' '}
          <span className="tabular">~/.ai-usage-cost/config.json</span>. The same answer covers a
          record whose file has moved since the scan.
        </p>
      )
    case 'error':
      return <p className="text-[11px] text-destructive">{state.message}</p>
    case 'ready': {
      const { content, truncated, redactions } = state.content
      return (
        <div className="space-y-1.5">
          <CodeBlock>{content}</CodeBlock>
          <p className="text-[10.5px] text-muted-foreground">
            {truncated ? 'Truncated at the configured byte limit. ' : ''}
            {redactions > 0
              ? `${formatCount(redactions)} secret${redactions === 1 ? '' : 's'} redacted before display.`
              : 'Nothing matched a redaction pattern.'}
          </p>
        </div>
      )
    }
  }
}

function InsightsPanel({
  insights,
  onFocus,
}: {
  insights: Insight[]
  onFocus: (spanId: string) => void
}) {
  if (insights.length === 0) return null

  return (
    <Panel>
      <PanelHeader
        eyebrow="Insights"
        title={`${formatCount(insights.length)} things worth a look in this session`}
      />
      <PanelBody>
        <InsightList
          insights={insights.map((insight) => ({
            kind: insight.kind,
            severity: insight.severity,
            message: insight.message,
            spanId: insight.span_id,
          }))}
          onSelectSpan={onFocus}
        />
      </PanelBody>
      <PanelNote>
        Each line names one worst span. When more than one span shares its finding, the line says
        how many and selecting it jumps to the worst of them.
      </PanelNote>
    </Panel>
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

  const onKindsChange = (next: string[]) => {
    setKinds(next as SpanKind[])
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

  const timelineRows: TraceSpanRow[] = shown.map((row) => {
    const { span, depth } = row
    const rolled = mode === 'tree' && row.descendants > 0
    const descendants = rolled ? row.descendants : 0
    const isOpen = expanded.includes(span.span_id)
    const body: ReactNode[] = []
    if (span.error) {
      body.push(
        <p key="error" className="tabular text-[11px] leading-relaxed text-destructive">
          {span.error}
        </p>,
      )
    }
    if (isOpen && contents[span.span_id]) {
      body.push(<ContentBlock key="content" state={contents[span.span_id]} />)
    }

    return {
      spanId: span.span_id,
      kind: span.kind,
      name: spanLabel(span),
      status: span.status,
      depth,
      clock: formatClock(span.started_at),
      tokens: (
        <TokensCell
          total={rolled ? row.subtreeTokens : (span.tokens?.total ?? 0)}
          provenance={rolled ? row.subtreeTokensProvenance : span.tokens_provenance}
          descendants={descendants}
        />
      ),
      duration: (
        <DurationCell
          ms={rolled ? row.subtreeDuration : span.duration_ms}
          provenance={rolled ? row.subtreeDurationProvenance : span.duration_provenance}
          descendants={descendants}
        />
      ),
      trailing: (
        <>
          <Badge
            variant="outline"
            className="px-1.5 text-[9px]"
            style={{
              borderColor: `color-mix(in oklab, ${SPAN_STATUS_COLOR[span.status]} 35%, transparent)`,
              color: SPAN_STATUS_COLOR[span.status],
            }}
          >
            {span.status}
          </Badge>
          {span.content_path === null ? (
            <span className="w-12 text-right text-[10px] text-muted-foreground">no text</span>
          ) : (
            <Button
              variant="outline"
              size="xs"
              aria-expanded={isOpen}
              className="w-12 text-[10px]"
              onClick={() => toggleContent(span)}
            >
              {isOpen ? 'Hide' : 'Text'}
            </Button>
          )}
        </>
      ),
      content:
        body.length > 0 ? (
          <div className="space-y-2 pb-2" style={{ paddingLeft: depth * 14 + 24 }}>
            {body}
          </div>
        ) : undefined,
    }
  })

  return (
    <>
      <Panel>
        <PanelHeader
          eyebrow="Trace"
          title={`${formatCount(spans.length)} spans, ${formatCount(rows.length)} in view`}
          actions={
            <ToggleGroup
              type="single"
              variant="outline"
              size="sm"
              value={mode}
              onValueChange={(value) => value && setMode(value as Mode)}
            >
              <ToggleGroupItem value="timeline">Timeline</ToggleGroupItem>
              <ToggleGroupItem value="tree">Agent tree</ToggleGroupItem>
            </ToggleGroup>
          }
        />
        <PanelBody className="space-y-3">
          <div className="flex flex-wrap gap-1.5">
            {CAPABILITY_LABELS.map((entry) => (
              <ProvenanceBadge
                key={entry.key}
                provenance={trace.capabilities[entry.key]}
                group={entry.label}
                title={`${entry.label}: this reader reports it as ${trace.capabilities[entry.key]}`}
              />
            ))}
          </div>
          <div className="flex flex-wrap items-center gap-1.5">
            <ToggleGroup
              type="multiple"
              variant="outline"
              size="sm"
              spacing={1.5}
              value={kinds}
              onValueChange={onKindsChange}
              className="flex-wrap"
            >
              {[...kindCounts.entries()].map(([kind, count]) => (
                <ToggleGroupItem key={kind} value={kind} className="gap-1.5 text-xs">
                  {kind}
                  <span className="tabular text-[10px] text-muted-foreground">
                    {formatCount(count)}
                  </span>
                </ToggleGroupItem>
              ))}
            </ToggleGroup>
            <Toggle
              variant="outline"
              size="sm"
              pressed={errorsOnly}
              onPressedChange={(next) => {
                setErrorsOnly(next)
                setRevealed(0)
              }}
              className="px-3 text-xs"
            >
              Errors only
            </Toggle>
          </div>
        </PanelBody>
        <PanelNote>
          {mode === 'timeline'
            ? 'Rows in log order, indented by their place in the tree. Every duration and token figure carries the word for where it came from.'
            : 'Rows grouped under their turn and subagent. A row with children shows its subtree summed, labelled with the weakest provenance in that subtree.'}
        </PanelNote>
      </Panel>

      <InsightsPanel insights={trace.insights} onFocus={focusSpan} />

      <Panel>
        {shown.length === 0 ? (
          <PanelBody>
            <EmptyState
              title="No span matches these filters"
              description="Clear a kind or turn off errors only."
            />
          </PanelBody>
        ) : (
          <PanelBody className="p-2">
            <SpanTimeline spans={timelineRows} rowId={rowDomId} focusedSpanId={focused} />
          </PanelBody>
        )}
        {hidden > 0 && (
          <PanelBody className="pt-0">
            <Button variant="outline" size="sm" onClick={() => setRevealed((current) => current + 1)}>
              {`Show ${formatCount(Math.min(ROW_BATCH, hidden))} more spans (${formatCount(hidden)} hidden)`}
            </Button>
          </PanelBody>
        )}
      </Panel>
    </>
  )
}
