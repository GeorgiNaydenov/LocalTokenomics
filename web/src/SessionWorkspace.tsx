import { useCallback, useEffect, useId, useRef, useState } from 'react'
import type { JSX, PointerEvent, ReactNode } from 'react'
import type {
  Capabilities,
  ContextSnapshot,
  Economics,
  Meta,
  Outcome,
  OutcomeLabel,
  OutcomeSignals,
  Report,
  SessionRow,
  Trace,
} from './api'
import { ApiError, fetchContext, fetchEconomics, fetchOutcome, fetchTrace, putOutcome } from './api'
import {
  formatClock,
  formatCount,
  formatDay,
  formatDuration,
  formatMoney,
  formatTimestamp,
  formatTokens,
  logSpanMs,
  plural,
  sessionDisplayName,
  toDayString,
} from './format'
import { BucketBar, CostStateBadge, Unavailable } from '@/components/status'
import { MetaGrid, PathList, Section } from '@/components/detail'
import { EmptyState } from '@/components/states'
import { TOKEN_BUCKETS } from '@/components/series'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { ToggleGroup, ToggleGroupItem } from '@/components/ui/toggle-group'
import { cn } from '@/design-system/cn'
import ContextTab from './ContextTab'
import EconomicsTab from './EconomicsTab'
import TraceTab from './TraceTab'
import { Sheet, SheetContent, SheetDescription, SheetTitle } from '@/components/ui/sheet'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Maximize2Icon, Minimize2Icon, XIcon } from 'lucide-react'
import { useWorkspacePanel } from '@/components/workspace-panel'

export type WorkspaceTab = 'summary' | 'trace' | 'economics' | 'context'

export interface TraceTabProps {
  source: string
  sessionId: string
  trace: Trace
  focusSpanId: string | null
}

export interface EconomicsTabProps {
  source: string
  sessionId: string
  economics: Economics
  capabilities: Capabilities | null
}

export interface ContextTabProps {
  source: string
  sessionId: string
  snapshots: ContextSnapshot[]
  onFocusSpan: (spanId: string) => void
}

const TABS: { id: WorkspaceTab; label: string }[] = [
  { id: 'summary', label: 'Summary' },
  { id: 'trace', label: 'Trace' },
  { id: 'economics', label: 'Economics' },
  { id: 'context', label: 'Context' },
]

const OUTCOME_LABELS: OutcomeLabel[] = ['successful', 'partial', 'failed', 'abandoned', 'unrated']

type Loadable<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'ready'; data: T }
  | { status: 'error'; message: string }

function messageOf(cause: unknown): string {
  return cause instanceof ApiError ? cause.message : String(cause)
}

type Settled<T> = { load: (signal: AbortSignal) => Promise<T>; result: Loadable<T> }

function useLazyResource<T>(enabled: boolean, load: (signal: AbortSignal) => Promise<T>): Loadable<T> {
  const [settled, setSettled] = useState<Settled<T> | null>(null)
  useEffect(() => {
    if (!enabled) return
    const controller = new AbortController()
    load(controller.signal)
      .then((data) => {
        if (controller.signal.aborted) return
        setSettled({ load, result: { status: 'ready', data } })
      })
      .catch((cause: unknown) => {
        if (controller.signal.aborted) return
        setSettled({ load, result: { status: 'error', message: messageOf(cause) } })
      })
    return () => controller.abort()
  }, [enabled, load])
  if (!enabled) return { status: 'idle' }
  return settled && settled.load === load ? settled.result : { status: 'loading' }
}

function costNote(session: SessionRow): string {
  switch (session.cost_state) {
    case 'priced': {
      let note = `${formatCount(session.request_count)} requests priced from the rate table at list prices.`
      const others = session.cost_states.filter((state) => state !== 'priced')
      if (others.length > 0) {
        note += ` Some of these requests are ${others.join(' or ')} instead and are not included in this total.`
      }
      return note
    }
    case 'free':
      return 'A local runtime, so the provider is marked free and this counts at zero.'
    case 'unpriced':
      return 'Tokens are counted, no rate entry matches this model, so cost stays out of totals.'
    case 'unavailable':
      return 'This client logs no token counts, so cost is left blank instead of guessed.'
  }
}

function TokenBucketsSection({ session }: { session: SessionRow }) {
  const tokens = session.tokens
  if (!tokens) {
    return (
      <EmptyState
        title="This client logs no token counts"
        description="The session, its requests and its timing are real and counted. Tokens and cost are left blank rather than guessed."
      />
    )
  }
  const cost = session.cost
  return (
    <Section title="Token buckets">
      <BucketBar
        segments={TOKEN_BUCKETS.map((bucket) => ({
          key: bucket.key,
          label: bucket.label,
          value: tokens[bucket.key],
          color: bucket.color,
        }))}
        formatValue={formatTokens}
      />
      <div>
        {TOKEN_BUCKETS.map((bucket) => (
          <div
            key={bucket.key}
            className="grid grid-cols-[14px_minmax(0,1fr)_auto_64px] items-center gap-2 border-b py-1.5 last:border-b-0"
          >
            <span aria-hidden className="size-2.5 rounded-full" style={{ background: bucket.color }} />
            <span className="text-[11px]">{bucket.label}</span>
            <span className="tabular text-[11px] text-muted-foreground">
              {formatTokens(tokens[bucket.key])}
            </span>
            <span className="tabular text-right text-[11px]">
              {cost ? formatMoney(cost[bucket.key]) : <Unavailable />}
            </span>
          </div>
        ))}
      </div>
      {tokens.reasoning_output > 0 && (
        <p className="text-[11px] text-muted-foreground">
          Reasoning: {formatTokens(tokens.reasoning_output)}, inside the{' '}
          {formatTokens(tokens.output)} output above.
        </p>
      )}
    </Section>
  )
}

function SessionOrigin({ session }: { session: SessionRow }) {
  const items: { label: string; value: ReactNode }[] = [
    { label: 'Client', value: session.client },
    { label: 'Provider', value: session.provider },
    { label: 'Models', value: session.models.map((model) => <div key={model}>{model}</div>) },
    { label: 'Project', value: session.project ?? '(no project)' },
    { label: 'Working directory', value: session.working_directory ?? 'none recorded' },
    { label: 'Repository', value: session.repository ?? 'none' },
    { label: 'Branch', value: session.branch ?? 'none' },
    { label: 'Requests', value: formatCount(session.request_count) },
    { label: 'Log span', value: formatDuration(logSpanMs(session)) },
    { label: 'Subagent thread', value: session.is_sidechain ? 'yes' : 'no' },
    { label: 'Machine', value: session.machine },
  ]
  return (
    <Section title="Where it came from">
      <MetaGrid items={items} className="sm:grid-cols-3" />
    </Section>
  )
}

function SummaryTab({ session }: { session: SessionRow }) {
  return (
    <div className="flex flex-col gap-4">
      <Section title="Cost" action={<CostStateBadge state={session.cost_state} />}>
        <div className="tabular text-[28px] font-semibold leading-none">
          {session.cost ? formatMoney(session.cost.total) : <Unavailable hint={costNote(session)} />}
        </div>
        <p className="text-[11px] leading-relaxed text-muted-foreground">{costNote(session)}</p>
      </Section>

      <TokenBucketsSection session={session} />

      <SessionOrigin session={session} />

      <Section title="Raw log files">
        <PathList paths={session.raw_source} />
      </Section>
    </div>
  )
}

function signalsNote(signals: OutcomeSignals): string {
  const parts: string[] = []
  if (signals.aborted_turns > 0) parts.push(plural(signals.aborted_turns, 'aborted turn'))
  if (signals.interrupted_tools > 0) parts.push(plural(signals.interrupted_tools, 'interrupted tool'))
  if (signals.errors > 0) parts.push(plural(signals.errors, 'error'))
  const found = parts.length > 0 ? parts.join(', ') : 'no aborts or errors'
  return `${found}, last turn ${signals.last_turn_status}`
}

interface OutcomeDraft {
  outcome: OutcomeLabel
  notes: string
  tagsText: string
}

function draftOf(stored: Outcome | null, fallback: OutcomeLabel): OutcomeDraft {
  if (!stored) return { outcome: fallback, notes: '', tagsText: '' }
  return { outcome: stored.outcome, notes: stored.notes, tagsText: stored.tags.join(', ') }
}

function parseTags(text: string): string[] {
  return text
    .split(',')
    .map((tag) => tag.trim())
    .filter((tag) => tag.length > 0)
}

function OutcomeControl(props: { source: string; sessionId: string; fallback: OutcomeLabel; loaded: Loadable<Outcome> }) {
  const [saved, setSaved] = useState<Outcome | null>(null)
  const [draft, setDraft] = useState<OutcomeDraft | null>(null)
  const [saving, setSaving] = useState(false)
  const [saveError, setSaveError] = useState<string | null>(null)
  const [open, setOpen] = useState(false)
  const fieldId = useId()

  const stored = saved ?? (props.loaded.status === 'ready' ? props.loaded.data : null)
  const persisted = draftOf(stored, props.fallback)
  const current = draft ?? persisted

  const save = (next: OutcomeDraft) => {
    setDraft(next)
    setSaving(true)
    setSaveError(null)
    putOutcome(props.source, props.sessionId, {
      outcome: next.outcome,
      notes: next.notes,
      tags: parseTags(next.tagsText),
    })
      .then((outcome) => {
        setSaved(outcome)
        setDraft(null)
      })
      .catch((cause: unknown) => setSaveError(messageOf(cause)))
      .finally(() => setSaving(false))
  }

  const saveEdited = () => {
    if (current.notes === persisted.notes && current.tagsText === persisted.tagsText) return
    save(current)
  }

  let status: string
  if (saving) status = 'saving…'
  else if (saveError) status = saveError
  else if (props.loaded.status === 'error') status = props.loaded.message
  else if (stored && stored.updated_at) status = `rated ${formatTimestamp(stored.updated_at)}`
  else status = 'not rated yet'

  return (
    <div className="flex flex-col gap-2">
      <div className="flex flex-wrap items-center gap-2">
        <ToggleGroup
          type="single"
          variant="outline"
          size="sm"
          spacing={1.5}
          value={current.outcome}
          onValueChange={(value) => value && save({ ...current, outcome: value as OutcomeLabel })}
          className="flex-wrap"
        >
          {OUTCOME_LABELS.map((label) => (
            <ToggleGroupItem key={label} value={label} className="text-xs">
              {label}
            </ToggleGroupItem>
          ))}
        </ToggleGroup>
        <Button variant="outline" size="sm" aria-expanded={open} onClick={() => setOpen(!open)}>
          Notes and tags
        </Button>
        <span className={cn('text-[11px]', saveError ? 'text-destructive' : 'text-muted-foreground')}>
          {status}
          {stored ? `; ${signalsNote(stored.signals)}` : ''}
        </span>
      </div>
      {open && (
        <div className="grid gap-3 rounded-md border p-3 sm:grid-cols-2">
          <div className="space-y-1.5">
            <Label htmlFor={`${fieldId}-notes`}>Notes</Label>
            <Textarea
              id={`${fieldId}-notes`}
              value={current.notes}
              onChange={(event) => setDraft({ ...current, notes: event.target.value })}
              onBlur={saveEdited}
              className="min-h-16"
            />
          </div>
          <div className="space-y-1.5">
            <Label htmlFor={`${fieldId}-tags`}>Tags, comma separated</Label>
            <Input
              id={`${fieldId}-tags`}
              value={current.tagsText}
              onChange={(event) => setDraft({ ...current, tagsText: event.target.value })}
              onBlur={saveEdited}
            />
          </div>
        </div>
      )}
    </div>
  )
}

function TabPlaceholder(props: { title: string; note: string; detail: string | null }) {
  return (
    <EmptyState
      title={props.title}
      description={
        <>
          {props.note}
          {props.detail && <span className="tabular mt-2 block">{props.detail}</span>}
        </>
      }
    />
  )
}

function LoadableTab<T>(props: {
  state: Loadable<T>
  title: string
  note: string
  children: (data: T) => ReactNode
}): JSX.Element {
  switch (props.state.status) {
    case 'idle':
    case 'loading':
      return <TabPlaceholder title={props.title} note="Loading…" detail={null} />
    case 'error':
      return <TabPlaceholder title={props.title} note={props.note} detail={props.state.message} />
    case 'ready':
      return <>{props.children(props.state.data)}</>
  }
}

const RESIZE_STEP = 24

function ResizeHandle(props: { width: number; onWidth: (width: number) => void; onDraggingChange: (dragging: boolean) => void }) {
  const origin = useRef<{ x: number; width: number } | null>(null)

  const endDrag = () => {
    origin.current = null
    props.onDraggingChange(false)
  }

  return (
    <div
      role="separator"
      aria-orientation="vertical"
      aria-label="Resize session panel"
      aria-valuenow={Math.round(props.width)}
      tabIndex={0}
      onPointerDown={(event: PointerEvent<HTMLDivElement>) => {
        origin.current = { x: event.clientX, width: props.width }
        props.onDraggingChange(true)
        event.currentTarget.setPointerCapture(event.pointerId)
      }}
      onPointerMove={(event: PointerEvent<HTMLDivElement>) => {
        if (!origin.current) return
        props.onWidth(origin.current.width - (event.clientX - origin.current.x))
      }}
      onPointerUp={endDrag}
      onPointerCancel={endDrag}
      onKeyDown={(event) => {
        if (event.key === 'ArrowLeft') props.onWidth(props.width + RESIZE_STEP)
        if (event.key === 'ArrowRight') props.onWidth(props.width - RESIZE_STEP)
      }}
      className="absolute inset-y-0 left-0 z-10 w-1.5 -translate-x-1/2 cursor-col-resize touch-none rounded-full outline-offset-2 hover:bg-primary/30 active:bg-primary/50"
    />
  )
}

export default function SessionWorkspace(props: {
  session: SessionRow
  report: Report
  meta: Meta
  tab: WorkspaceTab
  docked: boolean
  onSelectTab: (tab: WorkspaceTab) => void
  onClose: () => void
}): JSX.Element {
  const { session, report, meta, tab, docked, onSelectTab, onClose } = props
  const source = session.source
  const sessionId = session.session_id
  const capabilities = meta.sources.find((entry) => entry.id === source)?.capabilities ?? null

  const [requested, setRequested] = useState<WorkspaceTab[]>([tab])
  const [focusSpanId, setFocusSpanId] = useState<string | null>(null)
  const { width, setWidth, fullscreen, toggleFullscreen } = useWorkspacePanel()
  const [dragging, setDragging] = useState(false)

  const selectTab = (next: WorkspaceTab) => {
    setRequested((seen) => (seen.includes(next) ? seen : [...seen, next]))
    onSelectTab(next)
  }

  const loadOutcome = useCallback(
    (signal: AbortSignal) => fetchOutcome(source, sessionId, signal),
    [source, sessionId],
  )
  const loadTrace = useCallback((signal: AbortSignal) => fetchTrace(source, sessionId, signal), [source, sessionId])
  const loadEconomics = useCallback(
    (signal: AbortSignal) => fetchEconomics(source, sessionId, signal),
    [source, sessionId],
  )
  const loadContext = useCallback(
    (signal: AbortSignal) => fetchContext(source, sessionId, signal),
    [source, sessionId],
  )

  const outcome = useLazyResource<Outcome>(true, loadOutcome)
  const trace = useLazyResource<Trace>(requested.includes('trace'), loadTrace)
  const economics = useLazyResource<Economics>(requested.includes('economics'), loadEconomics)
  const context = useLazyResource<ContextSnapshot[]>(requested.includes('context'), loadContext)

  const modelLabel = report.by_model.find((bucket) => bucket.key === session.models[0])?.label ?? session.models[0]
  const subtitle = `${session.client} on ${modelLabel}, started ${formatDay(
    toDayString(session.start_time) ?? session.start_time,
  )} at ${formatClock(session.start_time)}`

  const focusSpan = (spanId: string) => {
    setFocusSpanId(spanId)
    selectTab('trace')
  }

  useEffect(() => {
    if (!docked) return
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') onClose()
    }
    document.addEventListener('keydown', onKeyDown)
    return () => document.removeEventListener('keydown', onKeyDown)
  }, [docked, onClose])

  const body = (
    <>
      <div className="flex flex-col gap-1 border-b p-card">
        <div className="flex items-start justify-between gap-2">
          <div className="flex min-w-0 flex-col gap-1">
            <p className="text-[11px] font-medium uppercase tracking-[0.08em] text-primary">Session</p>
            {docked ? (
              <h2 className="tabular text-base font-semibold break-all">
                {sessionDisplayName(session)}
              </h2>
            ) : (
              <SheetTitle className="tabular text-base font-semibold break-all">
                {sessionDisplayName(session)}
              </SheetTitle>
            )}
            {docked ? (
              <p className="text-[11px] text-muted-foreground">{subtitle}</p>
            ) : (
              <SheetDescription className="text-[11px]">{subtitle}</SheetDescription>
            )}
          </div>
          {docked && (
            <div className="flex shrink-0 items-center gap-1">
              <Button
                variant="ghost"
                size="icon-sm"
                aria-label={fullscreen ? 'Exit fullscreen' : 'Fullscreen'}
                aria-pressed={fullscreen}
                onClick={toggleFullscreen}
              >
                {fullscreen ? <Minimize2Icon /> : <Maximize2Icon />}
              </Button>
              <Button variant="ghost" size="icon-sm" aria-label="Close session" onClick={onClose}>
                <XIcon />
              </Button>
            </div>
          )}
        </div>
        <OutcomeControl source={source} sessionId={sessionId} fallback={session.outcome} loaded={outcome} />
      </div>

      <Tabs
        value={tab}
        onValueChange={(next) => selectTab(next as WorkspaceTab)}
        className="flex min-h-0 flex-1 flex-col gap-0"
      >
        <TabsList
          variant="line"
          className="w-full justify-start gap-4 overflow-x-auto border-b px-card"
          aria-label="Session views"
        >
          {TABS.map((entry) => (
            <TabsTrigger key={entry.id} value={entry.id}>
              {entry.label}
            </TabsTrigger>
          ))}
        </TabsList>

        <div className="scroll-thin min-h-0 flex-1 overflow-y-auto p-card">
          <TabsContent value="summary">
            <SummaryTab session={session} />
          </TabsContent>
          <TabsContent value="trace" className="space-y-2">
            <LoadableTab
              state={trace}
              title="Trace"
              note="The trace endpoint did not answer."
            >
              {(data) => (
                <TraceTab source={source} sessionId={sessionId} trace={data} focusSpanId={focusSpanId} />
              )}
            </LoadableTab>
          </TabsContent>
          <TabsContent value="economics">
            <LoadableTab
              state={economics}
              title="Economics"
              note="The economics endpoint did not answer."
            >
              {(data) => (
                <EconomicsTab
                  source={source}
                  sessionId={sessionId}
                  economics={data}
                  capabilities={capabilities}
                />
              )}
            </LoadableTab>
          </TabsContent>
          <TabsContent value="context">
            <LoadableTab
              state={context}
              title="Context"
              note="The context endpoint did not answer."
            >
              {(data) => (
                <ContextTab source={source} sessionId={sessionId} snapshots={data} onFocusSpan={focusSpan} />
              )}
            </LoadableTab>
          </TabsContent>
        </div>
      </Tabs>
    </>
  )

  if (docked) {
    return (
      <aside
        aria-label="Session workspace"
        className={cn(
          'relative flex shrink-0 flex-col bg-background [--card-padding:1rem]',
          fullscreen
            ? 'fixed inset-0 z-50 h-screen w-screen'
            : 'sticky top-[52px] h-[calc(100vh-52px)] border-l',
          dragging && 'select-none',
        )}
        style={fullscreen ? undefined : { width }}
      >
        {!fullscreen && <ResizeHandle width={width} onWidth={setWidth} onDraggingChange={setDragging} />}
        {body}
      </aside>
    )
  }

  return (
    <Sheet open onOpenChange={(next) => { if (!next) onClose() }}>
      <SheetContent side="right" className="flex w-full flex-col gap-0 p-0 [--card-padding:1rem] sm:max-w-full">
        {body}
      </SheetContent>
    </Sheet>
  )
}
