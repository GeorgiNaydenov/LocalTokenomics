import { useCallback, useEffect, useState } from 'react'
import type { JSX, ReactNode } from 'react'
import type {
  Provenance,
  ContextSnapshot,
  Economics,
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
  formatMoney,
  formatTimestamp,
  formatTokens,
  toDayString,
} from './format'
import { BUCKETS, PROVENANCE_COLOR, STATE_BADGE } from './theme'
import ContextTab from './ContextTab'
import EconomicsTab from './EconomicsTab'
import TraceTab from './TraceTab'

export type WorkspaceTab = 'summary' | 'trace' | 'economics' | 'context'

export function ProvenanceChip({
  provenance,
  group,
  title,
}: {
  provenance: Provenance
  group?: string
  title?: string
}) {
  const color = PROVENANCE_COLOR[provenance]
  return (
    <span
      className="badge"
      title={title}
      style={{ height: 18, gap: 5, padding: '0 5px', fontSize: 8.5, color, borderColor: color }}
    >
      {group && <span style={{ color: 'var(--fg-faint)' }}>{group}</span>}
      {provenance}
    </span>
  )
}

export function Unavailable({ hint }: { hint?: string }) {
  return (
    <span style={{ color: 'var(--fg-faint)' }} title={hint}>
      unavailable
    </span>
  )
}

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

function useLazyResource<T>(enabled: boolean, load: (signal: AbortSignal) => Promise<T>): Loadable<T> {
  const [state, setState] = useState<Loadable<T>>({ status: 'idle' })
  useEffect(() => {
    if (!enabled) return
    const controller = new AbortController()
    setState({ status: 'loading' })
    load(controller.signal)
      .then((data) => {
        if (controller.signal.aborted) return
        setState({ status: 'ready', data })
      })
      .catch((cause: unknown) => {
        if (controller.signal.aborted) return
        setState({ status: 'error', message: messageOf(cause) })
      })
    return () => controller.abort()
  }, [enabled, load])
  return state
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

function logSpan(startTime: string, endTime: string): string {
  const startMs = new Date(startTime).getTime()
  const endMs = new Date(endTime).getTime()
  const minutes = Math.max(0, Math.round((endMs - startMs) / 60000))
  if (minutes < 60) return `${minutes} min`
  const hours = Math.floor(minutes / 60)
  const remainder = minutes % 60
  return `${hours}h ${remainder}min`
}

function TokenBucketsSection({ session }: { session: SessionRow }) {
  const tokens = session.tokens
  if (!tokens) {
    return (
      <div className="empty-state" style={{ padding: 16, textAlign: 'left' }}>
        <strong style={{ fontSize: 12.5 }}>This client logs no token counts</strong>
        <span style={{ fontSize: 11, lineHeight: 1.55 }}>
          The session, its requests and its timing are real and counted. Tokens and cost are left blank rather than
          guessed.
        </span>
      </div>
    )
  }
  const cost = session.cost
  return (
    <div>
      <p className="detail-section__title" style={{ margin: '0 0 6px' }}>
        Token buckets
      </p>
      <div style={{ display: 'flex', height: 16, background: 'var(--bg-muted)' }}>
        {BUCKETS.map((bucket) => {
          const pct = tokens.total > 0 ? (tokens[bucket.key] / tokens.total) * 100 : 0
          return (
            <div
              key={bucket.key}
              style={{ width: `${pct}%`, background: bucket.color }}
              title={`${bucket.label} ${formatTokens(tokens[bucket.key])}`}
            />
          )
        })}
      </div>
      {BUCKETS.map((bucket) => (
        <div
          key={bucket.key}
          style={{
            display: 'grid',
            gridTemplateColumns: '14px 1fr auto auto',
            alignItems: 'center',
            gap: 8,
            padding: '5px 0',
            borderBottom: '1px solid var(--border)',
          }}
        >
          <span style={{ width: 9, height: 9, background: bucket.color }} />
          <span style={{ fontSize: 11, color: 'var(--fg-strong)' }}>{bucket.label}</span>
          <span className="num" style={{ fontSize: 11, color: 'var(--fg-muted)' }}>
            {formatTokens(tokens[bucket.key])}
          </span>
          <span className="num" style={{ fontSize: 11, width: 64, textAlign: 'right', color: 'var(--fg-strong)' }}>
            {cost ? formatMoney(cost[bucket.key]) : 'n/a'}
          </span>
        </div>
      ))}
      {tokens.reasoning_output > 0 && (
        <p style={{ margin: '6px 0 0', fontSize: 11, color: 'var(--fg-muted)' }}>
          Reasoning — {formatTokens(tokens.reasoning_output)}, inside the {formatTokens(tokens.output)} output above.
        </p>
      )}
    </div>
  )
}

function MetaGrid({ session }: { session: SessionRow }) {
  const items: { label: string; value: ReactNode }[] = [
    { label: 'Client', value: session.client },
    { label: 'Provider', value: session.provider },
    { label: 'Models', value: session.models.map((model) => <div key={model}>{model}</div>) },
    { label: 'Project', value: session.project ?? '(no project)' },
    { label: 'Working directory', value: session.working_directory ?? 'none recorded' },
    { label: 'Repository', value: session.repository ?? 'none' },
    { label: 'Branch', value: session.branch ?? 'none' },
    { label: 'Requests', value: formatCount(session.request_count) },
    { label: 'Log span', value: logSpan(session.start_time, session.end_time) },
    { label: 'Subagent thread', value: session.is_sidechain ? 'yes' : 'no' },
    { label: 'Machine', value: session.machine },
  ]
  return (
    <div>
      <p className="detail-section__title" style={{ margin: '0 0 6px' }}>
        Where it came from
      </p>
      <dl className="detail-meta-grid" style={{ padding: 12, gap: 12 }}>
        {items.map((item) => (
          <div className="detail-meta-grid__item" key={item.label}>
            <dt style={{ fontSize: 9 }}>{item.label}</dt>
            <dd className="num" style={{ fontSize: 11, fontWeight: 500, wordBreak: 'break-all' }}>
              {item.value}
            </dd>
          </div>
        ))}
      </dl>
    </div>
  )
}

function SummaryTab({ session }: { session: SessionRow }) {
  return (
    <>
      <div>
        <div style={{ display: 'flex', alignItems: 'baseline', justifyContent: 'space-between' }}>
          <p className="detail-section__title" style={{ margin: 0 }}>
            Cost
          </p>
          <span className={STATE_BADGE[session.cost_state]} style={{ fontSize: 9, padding: '1px 5px' }}>
            {session.cost_state}
          </span>
        </div>
        <div className="num" style={{ marginTop: 6, fontSize: 28, fontWeight: 600, color: 'var(--fg-strong)' }}>
          {session.cost ? formatMoney(session.cost.total) : 'not available'}
        </div>
        <p style={{ margin: '5px 0 0', fontSize: 11, lineHeight: 1.5, color: 'var(--fg-muted)' }}>
          {costNote(session)}
        </p>
      </div>

      <TokenBucketsSection session={session} />

      <MetaGrid session={session} />

      <div>
        <p className="detail-section__title" style={{ margin: '0 0 6px' }}>
          Raw log files
        </p>
        {session.raw_source.map((path) => (
          <div
            key={path}
            className="num"
            style={{
              padding: '6px 8px',
              marginBottom: 5,
              background: 'var(--bg-muted)',
              border: '1px solid var(--border)',
              fontSize: 10,
              color: 'var(--fg-muted)',
              wordBreak: 'break-all',
            }}
          >
            {path}
          </div>
        ))}
      </div>
    </>
  )
}

function plural(count: number, word: string): string {
  return `${count} ${word}${count === 1 ? '' : 's'}`
}

function signalsNote(signals: OutcomeSignals): string {
  const parts: string[] = []
  if (signals.aborted_turns > 0) parts.push(plural(signals.aborted_turns, 'aborted turn'))
  if (signals.interrupted_tools > 0) parts.push(plural(signals.interrupted_tools, 'interrupted tool'))
  if (signals.errors > 0) parts.push(plural(signals.errors, 'error'))
  const found = parts.length > 0 ? parts.join(', ') : 'no aborts or errors'
  return `${found} · last turn ${signals.last_turn_status}`
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

  const stored = saved ?? (props.loaded.status === 'ready' ? props.loaded.data : null)
  const current = draft ?? draftOf(stored, props.fallback)

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

  let status: string
  if (saving) status = 'saving…'
  else if (saveError) status = saveError
  else if (props.loaded.status === 'error') status = props.loaded.message
  else if (stored && stored.updated_at) status = `rated ${formatTimestamp(stored.updated_at)}`
  else status = 'not rated yet'

  return (
    <div className="workspace__outcome">
      <div className="chip-row">
        {OUTCOME_LABELS.map((label) => (
          <button
            key={label}
            type="button"
            className={label === current.outcome ? 'chip is-active' : 'chip'}
            onClick={() => save({ ...current, outcome: label })}
            style={{ height: 24, fontSize: 10, padding: '0 9px' }}
          >
            {label}
          </button>
        ))}
        <button
          type="button"
          className="chip"
          aria-expanded={open}
          onClick={() => setOpen(!open)}
          style={{ height: 24, fontSize: 10, padding: '0 9px' }}
        >
          Notes and tags
        </button>
      </div>
      <span style={{ fontSize: 11, color: saveError ? 'var(--rose)' : 'var(--fg-muted)' }}>
        {status}
        {stored ? ` · ${signalsNote(stored.signals)}` : ''}
      </span>
      {open && (
        <div className="workspace__disclosure">
          <label className="field-label">
            Notes
            <textarea
              className="textarea"
              value={current.notes}
              onChange={(event) => setDraft({ ...current, notes: event.target.value })}
              onBlur={() => save(current)}
              style={{ minHeight: 64, fontSize: 12 }}
            />
          </label>
          <label className="field-label">
            Tags, comma separated
            <input
              className="text-input"
              value={current.tagsText}
              onChange={(event) => setDraft({ ...current, tagsText: event.target.value })}
              onBlur={() => save(current)}
              style={{ minHeight: 32, fontSize: 12 }}
            />
          </label>
        </div>
      )}
    </div>
  )
}

function TabPlaceholder(props: { title: string; note: string; detail: string | null }) {
  return (
    <div className="empty-state">
      <strong>{props.title}</strong>
      <span style={{ fontSize: 11.5, lineHeight: 1.55 }}>{props.note}</span>
      {props.detail && (
        <p className="num" style={{ margin: '8px 0 0', fontSize: 11, color: 'var(--fg-faint)' }}>
          {props.detail}
        </p>
      )}
    </div>
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

export default function SessionWorkspace(props: {
  session: SessionRow
  report: Report
  tab: WorkspaceTab
  onSelectTab: (tab: WorkspaceTab) => void
  onClose: () => void
}): JSX.Element {
  const { session, report, tab, onSelectTab, onClose } = props
  const source = session.source
  const sessionId = session.session_id

  const [requested, setRequested] = useState<WorkspaceTab[]>([tab])
  const [focusSpanId, setFocusSpanId] = useState<string | null>(null)

  useEffect(() => {
    const onKey = (event: KeyboardEvent) => {
      if (event.key === 'Escape') onClose()
    }
    document.addEventListener('keydown', onKey)
    return () => document.removeEventListener('keydown', onKey)
  }, [onClose])

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
  const subtitle = `${session.client} · ${modelLabel} · ${formatDay(
    toDayString(session.start_time) ?? session.start_time,
  )} at ${formatClock(session.start_time)}`

  const focusSpan = (spanId: string) => {
    setFocusSpanId(spanId)
    selectTab('trace')
  }

  return (
    <div className="detail-panel-overlay" onClick={onClose}>
      <aside
        className="detail-panel workspace"
        role="dialog"
        aria-modal="true"
        aria-label={`Session ${sessionId}`}
        onClick={(e) => e.stopPropagation()}
      >
        <div className="detail-panel__header" style={{ padding: 14 }}>
          <div style={{ minWidth: 0 }}>
            <p className="lbl" style={{ color: 'var(--accent)' }}>
              Session
            </p>
            <h2 className="num" style={{ margin: '6px 0 0', fontSize: 16, fontWeight: 600, color: 'var(--fg-strong)' }}>
              {sessionId}
            </h2>
            <p style={{ margin: '5px 0 0', fontSize: 11.5, color: 'var(--fg-muted)' }}>{subtitle}</p>
            <OutcomeControl source={source} sessionId={sessionId} fallback={session.outcome} loaded={outcome} />
          </div>
          <button
            type="button"
            className="icon-button"
            onClick={onClose}
            aria-label="Close session"
            style={{ width: 30, height: 30 }}
          >
            ×
          </button>
        </div>

        <div className="tab-strip" role="tablist" aria-label="Session views">
          {TABS.map((entry) => (
            <button
              key={entry.id}
              type="button"
              role="tab"
              id={`workspace-tab-${entry.id}`}
              aria-selected={entry.id === tab}
              aria-controls={`workspace-panel-${entry.id}`}
              className={entry.id === tab ? 'tab-btn is-active' : 'tab-btn'}
              onClick={() => selectTab(entry.id)}
            >
              {entry.label}
            </button>
          ))}
        </div>

        <div className="detail-panel__body" style={{ padding: 0, gap: 0 }}>
          <div
            className="tab-panel workspace__panel"
            role="tabpanel"
            id={`workspace-panel-${tab}`}
            aria-labelledby={`workspace-tab-${tab}`}
          >
            {tab === 'summary' && <SummaryTab session={session} />}
            {tab === 'trace' && (
              <LoadableTab
                state={trace}
                title="Trace"
                note="The trace endpoint did not answer. It lands with the backend package B5."
              >
                {(data) => (
                  <TraceTab source={source} sessionId={sessionId} trace={data} focusSpanId={focusSpanId} />
                )}
              </LoadableTab>
            )}
            {tab === 'economics' && (
              <LoadableTab
                state={economics}
                title="Economics"
                note="The economics endpoint did not answer. It lands with the backend package B5."
              >
                {(data) => <EconomicsTab source={source} sessionId={sessionId} economics={data} />}
              </LoadableTab>
            )}
            {tab === 'context' && (
              <LoadableTab
                state={context}
                title="Context"
                note="The context endpoint did not answer. It lands with the backend package B5."
              >
                {(data) => (
                  <ContextTab source={source} sessionId={sessionId} snapshots={data} onFocusSpan={focusSpan} />
                )}
              </LoadableTab>
            )}
          </div>
        </div>
      </aside>
    </div>
  )
}
