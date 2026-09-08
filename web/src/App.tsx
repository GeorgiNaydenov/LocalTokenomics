import { useCallback, useEffect, useState } from 'react'
import type { CostState, FacetGroup, Meta, Query, RateTable, Report, View } from './api'
import { ApiError, fetchMeta, fetchRates, fetchReport, refresh } from './api'
import FilterRail from './FilterRail'
import Header from './Header'
import Overview from './Overview'
import Sessions from './Sessions'
import SessionWorkspace from './SessionWorkspace'
import type { WorkspaceTab } from './SessionWorkspace'
import Sources from './Sources'
import Pricing from './Pricing'
import { useTheme } from './theme'

const TODAY = new Date().toISOString().slice(0, 10)
const FIVE_MINUTES = 5 * 60 * 1000

const BLANK_QUERY: Query = {
  since: null,
  until: null,
  search: '',
  states: [],
  clients: [],
  models: [],
  projects: [],
  includeSidechains: true,
  outcomes: [],
  traced: null,
  hasErrors: null,
}

interface WorkspaceKey {
  source: string
  id: string
  tab: WorkspaceTab
}

function toggleValue<T extends string>(list: T[], value: T): T[] {
  return list.includes(value) ? list.filter((v) => v !== value) : [...list, value]
}

interface ActiveChip {
  key: string
  group: string
  label: string
  onRemove: () => void
}

function buildActiveChips(
  query: Query,
  meta: Meta | null,
  report: Report | null,
  toggleFacet: (group: FacetGroup, value: string) => void,
  patchQuery: (patch: Partial<Query>) => void,
): ActiveChip[] {
  const clientLabel = (id: string) => meta?.clients.find((c) => c.id === id)?.label ?? id
  const modelLabel = (id: string) => report?.by_model.find((b) => b.key === id)?.label ?? id
  const chips: ActiveChip[] = []
  for (const value of query.states) {
    chips.push({ key: `states:${value}`, group: 'state', label: value, onRemove: () => toggleFacet('states', value) })
  }
  for (const value of query.clients) {
    chips.push({
      key: `clients:${value}`,
      group: 'client',
      label: clientLabel(value),
      onRemove: () => toggleFacet('clients', value),
    })
  }
  for (const value of query.models) {
    chips.push({
      key: `models:${value}`,
      group: 'model',
      label: modelLabel(value),
      onRemove: () => toggleFacet('models', value),
    })
  }
  for (const value of query.projects) {
    chips.push({
      key: `projects:${value}`,
      group: 'project',
      label: value,
      onRemove: () => toggleFacet('projects', value),
    })
  }
  for (const value of query.outcomes) {
    chips.push({
      key: `outcomes:${value}`,
      group: 'outcome',
      label: value,
      onRemove: () => patchQuery({ outcomes: query.outcomes.filter((v) => v !== value) }),
    })
  }
  if (query.traced !== null) {
    chips.push({
      key: 'traced',
      group: 'trace',
      label: query.traced ? 'traced only' : 'untraced only',
      onRemove: () => patchQuery({ traced: null }),
    })
  }
  if (query.hasErrors !== null) {
    chips.push({
      key: 'hasErrors',
      group: 'errors',
      label: query.hasErrors ? 'with errors' : 'without errors',
      onRemove: () => patchQuery({ hasErrors: null }),
    })
  }
  if (query.search.trim()) {
    chips.push({ key: 'search', group: 'search', label: query.search.trim(), onRemove: () => patchQuery({ search: '' }) })
  }
  if (!query.includeSidechains) {
    chips.push({
      key: 'threads',
      group: 'threads',
      label: 'main thread only',
      onRemove: () => patchQuery({ includeSidechains: true }),
    })
  }
  return chips
}

function OfflineCard({ onRetry }: { onRetry: () => void }) {
  const [copied, setCopied] = useState(false)

  const handleCopy = () => {
    navigator.clipboard
      .writeText('ai-usage-cost serve')
      .then(() => {
        setCopied(true)
        setTimeout(() => setCopied(false), 2000)
      })
      .catch(() => {})
  }

  return (
    <div className="app" style={{ display: 'grid', placeItems: 'center', padding: 40 }}>
      <div className="offline-card">
        <p className="lbl" style={{ color: 'var(--rose)' }}>
          No server on {location.host}
        </p>
        <h1
          style={{
            margin: '8px 0 10px',
            fontFamily: 'var(--font-display)',
            fontWeight: 700,
            fontSize: 26,
            lineHeight: 1.1,
            color: 'var(--fg-strong)',
          }}
        >
          The dashboard lost the local reader.
        </h1>
        <p style={{ margin: '0 0 18px', lineHeight: 1.6, color: 'var(--fg-muted)' }}>
          Nothing was uploaded and nothing was lost. The last scan is still in your local SQLite store (
          <span className="num" style={{ color: 'var(--fg-strong)' }}>
            ~/.ai-usage-cost/usage.db
          </span>{' '}
          unless you passed --db). Start the reader again and this view reconnects.
        </p>
        <pre
          className="num"
          style={{
            margin: '0 0 18px',
            padding: '12px 14px',
            background: 'var(--bg-muted)',
            border: '1px solid var(--border)',
            fontSize: 11.5,
            color: 'var(--fg-strong)',
            overflow: 'auto',
          }}
        >
          ai-usage-cost serve
        </pre>
        <div style={{ display: 'flex', gap: 8 }}>
          <button type="button" className="btn-primary" style={{ height: 40, minHeight: 40 }} onClick={onRetry}>
            Retry connection
          </button>
          <button type="button" className="btn-ghost" style={{ height: 40, minHeight: 40 }} onClick={handleCopy}>
            {copied ? 'Copied' : 'Copy command'}
          </button>
        </div>
      </div>
    </div>
  )
}

export default function App() {
  const [mode, toggleTheme] = useTheme()

  const [meta, setMeta] = useState<Meta | null>(null)
  const [rates, setRates] = useState<RateTable | null>(null)
  const [report, setReport] = useState<Report | null>(null)
  const [query, setQuery] = useState<Query>(BLANK_QUERY)
  const [view, setView] = useState<View>('overview')
  const [workspace, setWorkspace] = useState<WorkspaceKey | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const [refetching, setRefetching] = useState(false)
  const [rescanning, setRescanning] = useState(false)
  const [reload, setReload] = useState(0)
  const [lastScanAt, setLastScanAt] = useState<number | null>(null)
  const [railOpen, setRailOpen] = useState(false)

  const patchQuery = useCallback((patch: Partial<Query>) => {
    setQuery((q) => ({ ...q, ...patch }))
  }, [])

  const toggleFacet = useCallback((group: FacetGroup, value: string) => {
    setQuery((q) => {
      switch (group) {
        case 'states':
          return { ...q, states: toggleValue(q.states, value as CostState) }
        case 'clients':
          return { ...q, clients: toggleValue(q.clients, value) }
        case 'models':
          return { ...q, models: toggleValue(q.models, value) }
        case 'projects':
          return { ...q, projects: toggleValue(q.projects, value) }
      }
    })
  }, [])

  useEffect(() => {
    const controller = new AbortController()
    setError(null)
    Promise.all([fetchMeta(controller.signal), fetchRates(controller.signal)])
      .then(([nextMeta, nextRates]) => {
        setMeta(nextMeta)
        setRates(nextRates)
        setQuery((q) => (q.since === null && q.until === null ? { ...q, since: nextMeta.first_day, until: TODAY } : q))
      })
      .catch((cause: unknown) => {
        if (controller.signal.aborted) return
        setError(cause instanceof ApiError ? cause.message : String(cause))
        setLoading(false)
      })
    return () => controller.abort()
  }, [reload])

  useEffect(() => {
    if (!meta) return
    const controller = new AbortController()
    setRefetching(true)
    fetchReport(query, controller.signal)
      .then((next) => {
        setReport(next)
        setError(null)
      })
      .catch((cause: unknown) => {
        if (controller.signal.aborted) return
        setError(cause instanceof ApiError ? cause.message : String(cause))
      })
      .finally(() => {
        if (controller.signal.aborted) return
        setRefetching(false)
        setLoading(false)
      })
    return () => controller.abort()
  }, [meta, query])

  const closeWorkspace = useCallback(() => setWorkspace(null), [])

  const selectWorkspaceTab = useCallback((tab: WorkspaceTab) => {
    setWorkspace((open) => (open ? { ...open, tab } : open))
  }, [])

  const doRefresh = useCallback(() => {
    setRescanning(true)
    refresh()
      .then(() => {
        setLastScanAt(Date.now())
        setReload((n) => n + 1)
      })
      .catch((cause: unknown) => {
        setError(cause instanceof ApiError ? cause.message : String(cause))
      })
      .finally(() => setRescanning(false))
  }, [])

  useEffect(() => {
    let interval: ReturnType<typeof setInterval> | null = null
    const start = () => {
      if (interval === null) interval = setInterval(doRefresh, FIVE_MINUTES)
    }
    const stop = () => {
      if (interval !== null) {
        clearInterval(interval)
        interval = null
      }
    }
    const onVisibility = () => {
      if (document.visibilityState !== 'visible') {
        stop()
        return
      }
      if (lastScanAt !== null && Date.now() - lastScanAt > FIVE_MINUTES) doRefresh()
      start()
    }
    if (document.visibilityState === 'visible') start()
    document.addEventListener('visibilitychange', onVisibility)
    return () => {
      stop()
      document.removeEventListener('visibilitychange', onVisibility)
    }
  }, [doRefresh, lastScanAt])

  const isOffline = error !== null && error.includes('Could not reach the ai-usage-cost server')

  if (isOffline) {
    return <OfflineCard onRetry={() => setReload((n) => n + 1)} />
  }

  if (loading) {
    return (
      <div className="app" style={{ display: 'grid', placeItems: 'center', minHeight: '100vh' }}>
        <p className="lbl">Loading ai-usage-cost…</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="app" style={{ display: 'grid', placeItems: 'center', minHeight: '100vh', padding: 24 }}>
        <p style={{ color: 'var(--rose)', maxWidth: '48ch', textAlign: 'center' }}>{error}</p>
      </div>
    )
  }

  const activeChips = buildActiveChips(query, meta, report, toggleFacet, patchQuery)
  const workspaceSession = workspace
    ? (report?.sessions.find((s) => s.session_id === workspace.id && s.source === workspace.source) ?? null)
    : null

  const openSession = (sessionId: string) => {
    const row = report?.sessions.find((s) => s.session_id === sessionId)
    if (!row) return
    setWorkspace({ source: row.source, id: row.session_id, tab: 'summary' })
  }

  return (
    <div className="app">
      <Header
        view={view}
        onSelectView={setView}
        meta={meta}
        ratesAsOf={rates?.as_of ?? meta?.rates_as_of ?? ''}
        filesScanned={meta?.files_scanned ?? 0}
        onRescan={doRefresh}
        rescanning={rescanning}
        lastScanAt={lastScanAt}
        mode={mode}
        onToggleTheme={toggleTheme}
        onOpenRail={() => setRailOpen(true)}
      />

      <div style={{ display: 'flex', alignItems: 'flex-start' }}>
        <FilterRail
          meta={meta}
          report={report}
          query={query}
          onChange={patchQuery}
          onToggleFacet={toggleFacet}
          onReset={() => patchQuery({ ...BLANK_QUERY, since: meta?.first_day ?? TODAY, until: TODAY })}
          today={TODAY}
          open={railOpen}
          onClose={() => setRailOpen(false)}
        />

        <main className="app-main">
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, flexWrap: 'wrap', marginBottom: 14 }}>
            <span className="num" style={{ fontSize: 11, color: 'var(--fg-muted)', opacity: refetching ? 0.5 : 1 }}>
              {report ? `${report.totals.sessions} sessions · ${report.totals.events} requests` : 'loading slice…'}
            </span>
            {activeChips.map((chip) => (
              <button
                key={chip.key}
                type="button"
                className="chip is-active"
                onClick={chip.onRemove}
                style={{ height: 24, fontSize: 11, padding: '0 9px' }}
              >
                <span className="chip__group" style={{ fontSize: 9 }}>
                  {chip.group}
                </span>
                {chip.label}
                <span style={{ marginLeft: 6, opacity: 0.7 }}>×</span>
              </button>
            ))}
          </div>

          {view === 'overview' && report && meta && (
            <Overview report={report} meta={meta} onSelectView={setView} />
          )}
          {view === 'sessions' && report && <Sessions report={report} onOpenSession={openSession} />}
          {view === 'sources' && report && meta && <Sources report={report} meta={meta} />}
          {view === 'pricing' && report && rates && <Pricing report={report} rates={rates} />}
        </main>
      </div>

      {report && workspace && workspaceSession && (
        <SessionWorkspace
          key={`${workspace.source}/${workspace.id}`}
          session={workspaceSession}
          report={report}
          tab={workspace.tab}
          onSelectTab={selectWorkspaceTab}
          onClose={closeWorkspace}
        />
      )}
    </div>
  )
}
