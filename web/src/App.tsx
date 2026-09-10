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
import { formatCount, today } from './format'
import { cn } from '@/design-system/cn'
import { FilterChips } from '@/components/filters'
import { StatLabel } from '@/components/stat'
import { ErrorState, OfflineCard } from '@/components/states'
import { useMediaQuery } from '@/components/use-media-query'

const TODAY = today()
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
  const [settledQuery, setSettledQuery] = useState<Query | null>(null)
  const [rescanning, setRescanning] = useState(false)
  const [reload, setReload] = useState(0)
  const [lastScanAt, setLastScanAt] = useState<number | null>(null)
  const [railOpen, setRailOpen] = useState(false)
  const canDock = useMediaQuery('(min-width: 1024px)')

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
    Promise.all([fetchMeta(controller.signal), fetchRates(controller.signal)])
      .then(([nextMeta, nextRates]) => {
        setMeta(nextMeta)
        setRates(nextRates)
        setError(null)
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
        setSettledQuery(query)
        setLoading(false)
      })
    return () => controller.abort()
  }, [meta, query])

  const refetching = meta !== null && settledQuery !== query

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
    return (
      <OfflineCard
        host={location.host}
        command="ai-usage-cost serve"
        onRetry={() => setReload((n) => n + 1)}
      />
    )
  }

  if (loading) {
    return (
      <div className="grid min-h-svh place-items-center">
        <StatLabel>Loading LocalTokenomics…</StatLabel>
      </div>
    )
  }

  if (error) {
    return (
      <div className="grid min-h-svh place-items-center p-6">
        <ErrorState message={error} className="w-full max-w-lg" />
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
    <div className="min-h-svh bg-background text-foreground">
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

      <div className="flex items-start">
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
          docked={workspaceSession === null}
        />

        <main className="min-w-0 flex-1 p-3 sm:px-[18px] sm:pb-10 sm:pt-4">
          <div className="mb-3.5 flex flex-wrap items-center gap-2">
            <span className={cn('tabular text-[11px] text-muted-foreground', refetching && 'opacity-50')}>
              {report
                ? `${formatCount(report.totals.sessions)} sessions, ${formatCount(report.totals.events)} requests`
                : 'loading slice…'}
            </span>
            <FilterChips filters={activeChips} />
          </div>

          {view === 'overview' && report && meta && (
            <Overview report={report} meta={meta} query={query} today={TODAY} onSelectView={setView} />
          )}
          {view === 'sessions' && report && (
            <Sessions report={report} onOpenSession={openSession} />
          )}
          {view === 'sources' && report && meta && <Sources report={report} meta={meta} />}
          {view === 'pricing' && report && rates && (
            <Pricing report={report} rates={rates} />
          )}
        </main>

        {report && meta && workspace && workspaceSession && (
          <SessionWorkspace
            key={`${workspace.source}/${workspace.id}`}
            session={workspaceSession}
            report={report}
            meta={meta}
            tab={workspace.tab}
            docked={canDock}
            onSelectTab={selectWorkspaceTab}
            onClose={closeWorkspace}
          />
        )}
      </div>
    </div>
  )
}
