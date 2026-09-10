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
import { worstProvenance } from '@/components/rank'
import type { TraceSpanRow } from '@/components/trace'
import { InsightList, SPAN_KIND_GLYPH, SPAN_STATUS_COLOR, SpanTimeline } from '@/components/trace'
import { SortSelect } from '@/components/filters'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { Toggle } from '@/components/ui/toggle'
import { ToggleGroup, ToggleGroupItem } from '@/components/ui/toggle-group'
import { Tooltip, TooltipContent, TooltipTrigger } from '@/components/ui/tooltip'

type Mode = 'timeline' | 'tree' | 'turns'

const INITIAL_ROWS = 200
const ROW_BATCH = 400

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
  if (ms === null) {
    return (
      <Unavailable
        hint={
          descendants > 0
            ? 'Neither this span nor any of its descendants carries a start and end time in the log.'
            : 'This span carries no timing in the log.'
        }
      />
    )
  }
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
  if (provenance === 'unavailable') {
    return (
      <Unavailable
        hint={
          descendants > 0
            ? 'Neither this span nor any of its descendants carries a token count in the log.'
            : 'This span carries no token count in the log.'
        }
      />
    )
  }
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

interface InsightTurn {
  key: string
  spanId: string
  label: string
}

interface TurnIndex {
  byId: Map<string, Span>
  anchors: Map<string, string>
  order: Map<string, number>
}

function buildTurnIndex(spans: Span[]): TurnIndex {
  const byId = new Map(spans.map((span) => [span.span_id, span]))
  const anchors = new Map<string, string>()
  const order = new Map<string, number>()
  const turns = spans.filter((span) => span.kind === 'turn').sort((a, b) => a.seq - b.seq)
  turns.forEach((span, index) => {
    const key = span.turn_id ?? span.span_id
    anchors.set(key, span.span_id)
    order.set(key, index + 1)
  })
  return { byId, anchors, order }
}

function resolveTurnFromIndex(spanId: string, index: TurnIndex): InsightTurn | null {
  let cursor = index.byId.get(spanId)
  const seen = new Set<string>()
  for (let guard = 0; cursor && guard < 64; guard += 1) {
    if (seen.has(cursor.span_id)) return null
    seen.add(cursor.span_id)
    const key = cursor.turn_id ?? (cursor.kind === 'turn' ? cursor.span_id : null)
    if (key !== null) {
      const anchorSpanId = index.anchors.get(key)
      const turnNumber = index.order.get(key)
      if (anchorSpanId && turnNumber) return { key, spanId: anchorSpanId, label: `Turn ${turnNumber}` }
      return null
    }
    cursor = cursor.parent_id ? index.byId.get(cursor.parent_id) : undefined
  }
  return null
}

export function resolveInsightTurn(spanId: string, spans: Span[]): InsightTurn | null {
  return resolveTurnFromIndex(spanId, buildTurnIndex(spans))
}

export function summarizeInsightTurns(insights: Insight[], spans: Span[]): string | null {
  const totalTurns = spans.filter((span) => span.kind === 'turn').length
  if (totalTurns === 0) return null
  const index = buildTurnIndex(spans)
  const weightByTurn = new Map<string, { label: string; weight: number }>()
  let totalWeight = 0
  for (const insight of insights) {
    const turn = resolveTurnFromIndex(insight.span_id, index)
    if (!turn) continue
    const weight = insight.count > 0 ? insight.count : 1
    totalWeight += weight
    const entry = weightByTurn.get(turn.key)
    if (entry) entry.weight += weight
    else weightByTurn.set(turn.key, { label: turn.label, weight })
  }
  const turnsWithInsights = weightByTurn.size
  const turnWord = totalTurns === 1 ? 'turn' : 'turns'
  if (turnsWithInsights === 0) {
    return `None of this session's insights could be tied to a turn, out of ${formatCount(totalTurns)} ${turnWord} total.`
  }
  const base = `${formatCount(turnsWithInsights)} of ${formatCount(totalTurns)} ${turnWord} carry at least one insight.`
  if (totalWeight === 0) return base
  const ranked = [...weightByTurn.values()].sort((a, b) => b.weight - a.weight)
  let dominant: typeof ranked = []
  let cumulative = 0
  for (let k = 0; k < Math.min(2, ranked.length); k += 1) {
    cumulative += ranked[k].weight
    if (cumulative / totalWeight > 0.5) {
      dominant = ranked.slice(0, k + 1)
      break
    }
  }
  if (dominant.length > 0 && dominant.length < turnsWithInsights) {
    const names = dominant.map((entry) => entry.label).join(' and ')
    const share = dominant.reduce((sum, entry) => sum + entry.weight, 0) / totalWeight
    return `${base} ${names} account${dominant.length === 1 ? 's' : ''} for ${Math.round(share * 100)}% of them.`
  }
  return base
}

function InsightsPanel({
  insights,
  spans,
  onFocus,
}: {
  insights: Insight[]
  spans: Span[]
  onFocus: (spanId: string) => void
}) {
  if (insights.length === 0) return null

  const summary = summarizeInsightTurns(insights, spans)

  return (
    <Panel>
      <PanelHeader
        eyebrow="Insights"
        title={`${formatCount(insights.length)} things worth a look in this session`}
      />
      <PanelBody className="space-y-2">
        {summary ? <p className="text-[11px] leading-relaxed text-muted-foreground">{summary}</p> : null}
        <InsightList
          insights={insights.map((insight) => {
            const turn = resolveInsightTurn(insight.span_id, spans)
            return {
              kind: insight.kind,
              severity: insight.severity,
              message: insight.message,
              spanId: insight.span_id,
              turnLabel: turn?.label,
              turnSpanId: turn?.spanId,
            }
          })}
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
  minStart: number | null
  maxEnd: number | null
}

export function spanWindow(span: Span): { start: number | null; end: number | null } {
  const parsedStart = Date.parse(span.started_at)
  const start = Number.isFinite(parsedStart) ? parsedStart : null
  if (span.ended_at) {
    const parsedEnd = Date.parse(span.ended_at)
    return { start, end: Number.isFinite(parsedEnd) ? parsedEnd : null }
  }
  if (start !== null && span.duration_ms !== null) return { start, end: start + span.duration_ms }
  return { start, end: null }
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
    const window = spanWindow(span)
    const placeholder: Subtree = {
      descendants: 0,
      tokens: span.tokens?.total ?? 0,
      tokensProvenance: span.tokens_provenance,
      duration: span.duration_ms,
      durationProvenance: span.duration_provenance,
      minStart: window.start,
      maxEnd: window.end,
    }
    subtrees.set(span.span_id, placeholder)
    let descendants = 0
    let tokens = span.tokens?.total ?? 0
    let minStart = window.start
    let maxEnd = window.end
    const tokenSources: Provenance[] = span.tokens ? [span.tokens_provenance] : []
    for (const child of children.get(span.span_id) ?? []) {
      const sub = collect(child)
      descendants += sub.descendants + 1
      tokens += sub.tokens
      if (sub.tokensProvenance !== 'unavailable') tokenSources.push(sub.tokensProvenance)
      if (sub.minStart !== null) minStart = minStart === null ? sub.minStart : Math.min(minStart, sub.minStart)
      if (sub.maxEnd !== null) maxEnd = maxEnd === null ? sub.maxEnd : Math.max(maxEnd, sub.maxEnd)
    }
    const impliedDuration = minStart !== null && maxEnd !== null && maxEnd > minStart ? maxEnd - minStart : null
    const duration = span.duration_ms !== null ? span.duration_ms : impliedDuration
    const durationProvenance =
      span.duration_ms !== null ? span.duration_provenance : impliedDuration !== null ? 'derived' : 'unavailable'
    const result: Subtree = {
      descendants,
      tokens,
      tokensProvenance: tokenSources.length > 0 ? worstProvenance(tokenSources) : 'unavailable',
      duration,
      durationProvenance,
      minStart,
      maxEnd,
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

const UNATTRIBUTED_TURN_KEY = 'unattributed'
const UNATTRIBUTED_TURN_LABEL = 'Outside any turn'
const TURN_TOOL_KINDS: SpanKind[] = ['tool_call', 'retrieval', 'subagent']
const TURN_TOP_N = 5

interface TurnTokens {
  inputTotal: number
  output: number
}

export interface TurnRollup {
  key: string
  turnId: string | null
  label: string | null
  ordinal: number
  span: Span | null
  spanIds: string[]
  startedAt: string | null
  spanCount: number
  duration: number | null
  durationProvenance: Provenance
  kindCounts: [SpanKind, number][]
  tokens: TurnTokens | null
  tokensProvenance: Provenance
  models: string[]
  errorCount: number
  isSidechain: boolean
}

function turnToolResultParents(spans: Span[]): Set<string> {
  const parents = new Set<string>()
  for (const span of spans) {
    if (span.kind === 'tool_result' && span.parent_id) parents.add(span.parent_id)
  }
  return parents
}

function isTurnErrorSpan(span: Span, toolResultParents: Set<string>): boolean {
  if (span.kind === 'error') return true
  if (span.status !== 'error') return false
  if (span.kind === 'tool_result') return true
  if (TURN_TOOL_KINDS.includes(span.kind)) return !toolResultParents.has(span.span_id)
  return true
}

function parseTurnStart(value: string): number {
  const parsed = Date.parse(value)
  return Number.isFinite(parsed) ? parsed : Number.POSITIVE_INFINITY
}

function turnRollupOf(
  key: string,
  turnId: string | null,
  group: Span[],
  toolResultParents: Set<string>,
): Omit<TurnRollup, 'ordinal'> {
  const turnSpan = turnId !== null ? (group.find((span) => span.kind === 'turn') ?? null) : null
  const children = turnId !== null ? group.filter((span) => span.kind !== 'turn') : group
  const earliestChild = children.reduce<Span | null>((earliest, span) => {
    if (!earliest) return span
    return parseTurnStart(span.started_at) < parseTurnStart(earliest.started_at) ? span : earliest
  }, null)

  const kindCounts = new Map<SpanKind, number>()
  for (const span of children) kindCounts.set(span.kind, (kindCounts.get(span.kind) ?? 0) + 1)

  const modelCalls = children.filter((span) => span.kind === 'model_call')
  const tokensProvenance = worstProvenance(modelCalls.map((span) => span.tokens_provenance))
  const tokens: TurnTokens | null =
    tokensProvenance === 'unavailable'
      ? null
      : modelCalls.reduce(
          (sum, span) => ({
            inputTotal: sum.inputTotal + (span.tokens?.input_total ?? 0),
            output: sum.output + (span.tokens?.output ?? 0),
          }),
          { inputTotal: 0, output: 0 },
        )

  const models = [
    ...new Set(modelCalls.map((span) => span.model).filter((model): model is string => model !== null)),
  ]

  return {
    key,
    turnId,
    label: turnId === null ? UNATTRIBUTED_TURN_LABEL : null,
    span: turnSpan,
    spanIds: group.map((span) => span.span_id),
    startedAt: turnSpan ? turnSpan.started_at : (earliestChild?.started_at ?? null),
    spanCount: group.length,
    duration: turnSpan ? turnSpan.duration_ms : null,
    durationProvenance: turnSpan ? turnSpan.duration_provenance : 'unavailable',
    kindCounts: [...kindCounts.entries()],
    tokens,
    tokensProvenance,
    models,
    errorCount: group.filter((span) => isTurnErrorSpan(span, toolResultParents)).length,
    isSidechain: turnSpan ? turnSpan.is_sidechain : children.some((span) => span.is_sidechain),
  }
}

export function groupSpansByTurn(spans: Span[]): TurnRollup[] {
  const groups = new Map<string, Span[]>()
  const unattributed: Span[] = []
  for (const span of spans) {
    if (span.turn_id) {
      const bucket = groups.get(span.turn_id)
      if (bucket) bucket.push(span)
      else groups.set(span.turn_id, [span])
    } else {
      unattributed.push(span)
    }
  }

  const toolResultParents = turnToolResultParents(spans)
  const turns = [...groups.entries()].map(([turnId, group]) => turnRollupOf(turnId, turnId, group, toolResultParents))
  turns.sort((a, b) => parseTurnStart(a.startedAt ?? '') - parseTurnStart(b.startedAt ?? ''))

  const ordered =
    unattributed.length > 0
      ? [...turns, turnRollupOf(UNATTRIBUTED_TURN_KEY, null, unattributed, toolResultParents)]
      : turns

  return ordered.map((rollup, index) => ({ ...rollup, ordinal: index + 1 }))
}

type TurnSort = 'spans' | 'duration' | 'errors' | 'chronological'

const TURN_SORT_OPTIONS: { value: TurnSort; label: string }[] = [
  { value: 'spans', label: 'By span count' },
  { value: 'duration', label: 'By duration' },
  { value: 'errors', label: 'By errors' },
  { value: 'chronological', label: 'Chronological' },
]

const TURN_SORT_COMPARE: Record<TurnSort, (a: TurnRollup, b: TurnRollup) => number> = {
  chronological: (a, b) => a.ordinal - b.ordinal,
  duration: (a, b) => (b.duration ?? -1) - (a.duration ?? -1),
  spans: (a, b) => b.spanCount - a.spanCount,
  errors: (a, b) => b.errorCount - a.errorCount,
}

function TurnTokensCell({ tokens, provenance }: { tokens: TurnTokens | null; provenance: Provenance }) {
  if (tokens === null) {
    return <Unavailable hint="No model_call span in this turn carries a token count in the log." />
  }
  return (
    <span className="inline-flex items-center gap-1.5">
      <span className="tabular">{`${formatTokens(tokens.inputTotal)} in / ${formatTokens(tokens.output)} out`}</span>
      <ProvenanceBadge provenance={provenance} />
    </span>
  )
}

function TurnBreakdown({ counts }: { counts: [SpanKind, number][] }) {
  if (counts.length === 0) return <span className="text-muted-foreground">--</span>
  return (
    <span className="inline-flex flex-wrap items-center gap-x-1.5 gap-y-0.5">
      {counts.map(([kind, count]) => (
        <Tooltip key={kind}>
          <TooltipTrigger asChild>
            <span className="tabular inline-flex items-center gap-0.5 rounded-sm border px-1 text-[10px] text-muted-foreground">
              <span>{SPAN_KIND_GLYPH[kind]}</span>
              {formatCount(count)}
            </span>
          </TooltipTrigger>
          <TooltipContent>{`${formatCount(count)} ${kind.replace('_', ' ')}`}</TooltipContent>
        </Tooltip>
      ))}
    </span>
  )
}

function TurnRollupTable({
  rollups,
  sort,
  onSortChange,
  showAll,
  onShowAll,
  onJump,
}: {
  rollups: TurnRollup[]
  sort: TurnSort
  onSortChange: (sort: TurnSort) => void
  showAll: boolean
  onShowAll: () => void
  onJump: (rollup: TurnRollup) => void
}) {
  const sorted = [...rollups].sort(TURN_SORT_COMPARE[sort])
  const shown = showAll ? sorted : sorted.slice(0, TURN_TOP_N)
  const hidden = sorted.length - shown.length

  return (
    <>
      <PanelBody className="flex flex-wrap items-center justify-between gap-2">
        <span className="text-[11px] text-muted-foreground">
          {showAll
            ? `All ${formatCount(sorted.length)} turns`
            : `Top ${formatCount(shown.length)} of ${formatCount(sorted.length)} turns`}
        </span>
        <SortSelect options={TURN_SORT_OPTIONS} value={sort} onChange={(value) => onSortChange(value as TurnSort)} />
      </PanelBody>
      <PanelBody className="p-2 pt-0">
        <div className="scroll-thin overflow-x-auto">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>#</TableHead>
                <TableHead>Started</TableHead>
                <TableHead>Duration</TableHead>
                <TableHead>Spans</TableHead>
                <TableHead>Tokens</TableHead>
                <TableHead>Model</TableHead>
                <TableHead className="text-right">Errors</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {shown.map((rollup) => (
                <TableRow
                  key={rollup.key}
                  tabIndex={0}
                  role="button"
                  aria-label={`Jump to turn ${rollup.ordinal}${rollup.label ? ` (${rollup.label})` : ''} in the timeline`}
                  className="cursor-pointer outline-offset-[-2px]"
                  onClick={() => onJump(rollup)}
                  onKeyDown={(event) => {
                    if (event.key !== 'Enter' && event.key !== ' ') return
                    event.preventDefault()
                    onJump(rollup)
                  }}
                >
                  <TableCell className="tabular text-muted-foreground">{rollup.ordinal}</TableCell>
                  <TableCell className="tabular text-muted-foreground">
                    <span className="inline-flex items-center gap-1.5">
                      {rollup.label && (
                        <Badge variant="outline" className="px-1.5 text-[9px]">
                          {rollup.label}
                        </Badge>
                      )}
                      {rollup.startedAt ? formatClock(rollup.startedAt) : <Unavailable />}
                      {rollup.isSidechain && (
                        <Badge variant="outline" className="px-1 text-[9px]">
                          sidechain
                        </Badge>
                      )}
                    </span>
                  </TableCell>
                  <TableCell>
                    <DurationCell ms={rollup.duration} provenance={rollup.durationProvenance} descendants={0} />
                  </TableCell>
                  <TableCell>
                    <span className="inline-flex items-center gap-1.5">
                      <span className="tabular text-muted-foreground">{formatCount(rollup.spanCount)}</span>
                      <TurnBreakdown counts={rollup.kindCounts} />
                    </span>
                  </TableCell>
                  <TableCell>
                    <TurnTokensCell tokens={rollup.tokens} provenance={rollup.tokensProvenance} />
                  </TableCell>
                  <TableCell className="text-muted-foreground">
                    {rollup.models.length === 0 ? '--' : rollup.models.join(', ')}
                  </TableCell>
                  <TableCell className="text-right tabular">
                    {rollup.errorCount > 0 ? (
                      <span style={{ color: 'var(--destructive)' }}>{formatCount(rollup.errorCount)}</span>
                    ) : (
                      <span className="text-muted-foreground">0</span>
                    )}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </PanelBody>
      {hidden > 0 && (
        <PanelBody className="pt-0">
          <Button variant="outline" size="sm" onClick={onShowAll}>
            {`Show all ${formatCount(sorted.length)} turns`}
          </Button>
        </PanelBody>
      )}
    </>
  )
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
  const [turnSort, setTurnSort] = useState<TurnSort>('spans')
  const [turnShowAll, setTurnShowAll] = useState(false)

  const focused = picked ?? focusSpanId
  const spans = trace.spans
  const visible = mode === 'turns' ? new Set<string>() : visibleSpanIds(spans, kinds, errorsOnly, mode === 'tree')
  const rows = mode === 'turns' ? [] : buildRows(spans, mode, visible)
  const turnRollups = mode === 'turns' ? groupSpansByTurn(spans) : []
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

  const selectSpan = (spanId: string) => {
    focusSpan(spanId)
    const span = spans.find((entry) => entry.span_id === spanId)
    if (span && span.content_path !== null && !expanded.includes(spanId)) toggleContent(span)
  }

  const jumpToTurn = (rollup: TurnRollup) => {
    const spanId = rollup.span?.span_id ?? rollup.spanIds[0]
    if (!spanId) return
    setMode('timeline')
    setKinds([])
    setErrorsOnly(false)
    setRevealed(0)
    setPicked(spanId)
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
          title={
            mode === 'turns'
              ? `${formatCount(spans.length)} spans, ${formatCount(turnRollups.length)} turns`
              : `${formatCount(spans.length)} spans, ${formatCount(rows.length)} in view`
          }
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
              <ToggleGroupItem value="turns">By turn</ToggleGroupItem>
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
            : mode === 'tree'
              ? 'Rows grouped under their turn and subagent. A row with children shows its subtree summed, labelled with the weakest provenance in that subtree.'
              : 'One row per turn, built only from the spans above. Duration and tokens use the turn’s own figures, never a re-summed total. Select a row to jump to that turn in the Timeline.'}
        </PanelNote>
      </Panel>

      <InsightsPanel insights={trace.insights} spans={spans} onFocus={focusSpan} />

      <Panel>
        {mode === 'turns' ? (
          turnRollups.length === 0 ? (
            <PanelBody>
              <EmptyState
                title="No turns in this trace"
                description="Every span here is outside a turn, or the trace carries no spans."
              />
            </PanelBody>
          ) : (
            <TurnRollupTable
              rollups={turnRollups}
              sort={turnSort}
              onSortChange={(next) => {
                setTurnSort(next)
                setTurnShowAll(false)
              }}
              showAll={turnShowAll}
              onShowAll={() => setTurnShowAll(true)}
              onJump={jumpToTurn}
            />
          )
        ) : shown.length === 0 ? (
          <PanelBody>
            <EmptyState
              title="No span matches these filters"
              description="Clear a kind or turn off errors only."
            />
          </PanelBody>
        ) : (
          <PanelBody className="p-2">
            <SpanTimeline
              spans={timelineRows}
              rowId={rowDomId}
              focusedSpanId={focused}
              onSelectSpan={selectSpan}
            />
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
