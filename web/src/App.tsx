import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import type { Meta, Report, ReportQuery } from './api'
import { ApiError, fetchMeta, fetchReport, refresh as refreshApi } from './api'
import { CostByModel } from './charts/CostByModel'
import type { Metric, StackBy } from './charts/CostOverTime'
import { CostOverTime } from './charts/CostOverTime'
import { TokenMix } from './charts/TokenMix'
import { Card, CardHeader } from './components/Card'
import { Segmented } from './components/Controls'
import { FilterBar } from './components/FilterBar'
import { Header } from './components/Header'
import { KpiRow } from './components/KpiRow'
import { CacheSavings } from './components/CacheSavings'
import { Notices } from './components/Notices'
import { ProjectBreakdown } from './components/ProjectBreakdown'
import { SessionsTable } from './components/SessionsTable'
import { DashboardSkeleton, EmptyState, ErrorState } from './components/States'
import { formatCount, formatTimestamp } from './format'
import { useTheme } from './theme'

const EMPTY_QUERY: ReportQuery = {
  since: null,
  until: null,
  clients: [],
  providers: [],
  models: [],
  projects: [],
  includeSidechains: true,
}

function fullQuery(meta: Meta): ReportQuery {
  return {
    since: meta.first_day,
    until: meta.last_day,
    clients: meta.clients.map((client) => client.id),
    providers: [...meta.providers],
    models: [...meta.models],
    projects: [...meta.projects],
    includeSidechains: true,
  }
}

function clampRange(
  since: string | null,
  until: string | null,
  meta: Meta,
): { since: string | null; until: string | null } {
  const first = meta.first_day
  const last = meta.last_day
  if (!first || !last || !since || !until) return { since: first, until: last }
  const next = {
    since: since < first ? first : since > last ? last : since,
    until: until > last ? last : until < first ? first : until,
  }
  return next.since <= next.until ? next : { since: first, until: last }
}

function sameQuery(a: ReportQuery, b: ReportQuery): boolean {
  return (
    a.since === b.since &&
    a.until === b.until &&
    a.includeSidechains === b.includeSidechains &&
    a.clients.join() === b.clients.join() &&
    a.providers.join() === b.providers.join() &&
    a.models.join() === b.models.join() &&
    a.projects.join() === b.projects.join()
  )
}

export default function App() {
  const [mode, toggleTheme] = useTheme()

  const [meta, setMeta] = useState<Meta | null>(null)
  const [query, setQuery] = useState<ReportQuery>(EMPTY_QUERY)
  const [report, setReport] = useState<Report | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const [refetching, setRefetching] = useState(false)
  const [refreshing, setRefreshing] = useState(false)
  const [reload, setReload] = useState(0)
  const [dismissed, setDismissed] = useState(false)

  const [stackBy, setStackBy] = useState<StackBy>('model')
  const [metric, setMetric] = useState<Metric>('cost')

  const ready = useRef(false)

  useEffect(() => {
    const controller = new AbortController()
    setLoading(true)
    setError(null)
    fetchMeta(controller.signal)
      .then((next) => {
        setMeta(next)
        setQuery(fullQuery(next))
        ready.current = true
      })
      .catch((cause: unknown) => {
        if (controller.signal.aborted) return
        setError(cause instanceof ApiError ? cause.message : String(cause))
        setLoading(false)
      })
    return () => controller.abort()
  }, [reload])

  useEffect(() => {
    if (!meta || !ready.current) return
    const controller = new AbortController()
    setRefetching(true)
    fetchReport(query, meta, controller.signal)
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

  const onRefresh = useCallback(() => {
    setRefreshing(true)
    refreshApi()
      .then((next) => {
        setQuery((current) => {
          const untouchedRange =
            !meta || (current.since === meta.first_day && current.until === meta.last_day)
          const range = untouchedRange
            ? { since: next.first_day, until: next.last_day }
            : clampRange(current.since, current.until, next)
          const clients = current.clients.filter((client) =>
            next.clients.some((item) => item.id === client),
          )
          const providers = current.providers.filter((provider) =>
            next.providers.includes(provider),
          )
          const models = current.models.filter((model) => next.models.includes(model))
          const projects = current.projects.filter((project) => next.projects.includes(project))
          return {
            ...range,
            clients: clients.length ? clients : next.clients.map((client) => client.id),
            providers: providers.length ? providers : [...next.providers],
            models: models.length ? models : [...next.models],
            projects: projects.length ? projects : [...next.projects],
            includeSidechains: current.includeSidechains,
          }
        })
        setMeta(next)
        setError(null)
      })
      .catch((cause: unknown) => {
        setError(cause instanceof ApiError ? cause.message : String(cause))
      })
      .finally(() => setRefreshing(false))
  }, [meta])

  const onReset = useCallback(() => {
    if (meta) setQuery(fullQuery(meta))
  }, [meta])

  const modelIndex = useCallback(
    (model: string) => (meta ? meta.models.indexOf(model) : -1),
    [meta],
  )
  const clientIndex = useCallback(
    (client: string) => (meta ? meta.clients.findIndex((item) => item.id === client) : -1),
    [meta],
  )
  const clientLabel = useCallback(
    (client: string) => meta?.clients.find((item) => item.id === client)?.label ?? client,
    [meta],
  )
  const providerIndex = useCallback(
    (provider: string) => (meta ? meta.providers.indexOf(provider) : -1),
    [meta],
  )
  const providerLabel = useCallback((provider: string) => provider, [])
  const identityIndex = useCallback(
    (dimension: StackBy, key: string) =>
      dimension === 'client'
        ? clientIndex(key)
        : dimension === 'provider'
          ? providerIndex(key)
          : modelIndex(key),
    [clientIndex, providerIndex, modelIndex],
  )
  const modelLabels = useRef(new Map<string, string>())
  for (const bucket of report?.by_model ?? []) modelLabels.current.set(bucket.key, bucket.label)
  const modelLabel = useCallback((model: string) => modelLabels.current.get(model) ?? model, [])
  const labelFor = useCallback(
    (dimension: StackBy, key: string) =>
      dimension === 'client'
        ? clientLabel(key)
        : dimension === 'provider'
          ? providerLabel(key)
          : modelLabel(key),
    [clientLabel, providerLabel, modelLabel],
  )
  const clientOrder = useMemo(() => meta?.clients.map((client) => client.id) ?? [], [meta])

  const dirty = useMemo(
    () => (meta ? !sameQuery(query, fullQuery(meta)) : false),
    [meta, query],
  )

  const hasData = report !== null && report.totals.events > 0
  const noticeVisible =
    !dismissed &&
    report !== null &&
    (report.unknown_models.length > 0 || report.warnings.length > 0)

  return (
    <div className="min-h-screen bg-page">
      <Header
        meta={meta}
        ratesAsOf={report?.rates_as_of ?? meta?.rates_as_of ?? ''}
        mode={mode}
        onToggleTheme={toggleTheme}
        onRefresh={onRefresh}
        refreshing={refreshing}
      />

      <main className="mx-auto max-w-[1440px] px-5 py-5 lg:px-8">
        {error && !report ? (
          <ErrorState message={error} onRetry={() => setReload((value) => value + 1)} />
        ) : loading || !report ? (
          <DashboardSkeleton />
        ) : (
          <div
            className="space-y-4 transition-opacity duration-150"
            style={{ opacity: refetching ? 0.55 : 1 }}
          >
            <FilterBar
              meta={meta}
              query={query}
              onChange={setQuery}
              onReset={onReset}
              dirty={dirty}
              modelLabel={modelLabel}
            />

            {error ? (
              <p className="rounded-xl border border-border bg-warn-soft px-4 py-3 text-[13px] text-ink">
                {error}
              </p>
            ) : null}

            {noticeVisible ? (
              <Notices report={report} onDismiss={() => setDismissed(true)} />
            ) : null}

            {!hasData ? (
              <EmptyState onReset={onReset} />
            ) : (
              <>
                <KpiRow report={report} clientOrder={clientOrder} mode={mode} />

                <CacheSavings totals={report.totals} />

                <Card>
                  <CardHeader
                    title={metric === 'cost' ? 'Cost over time' : 'Tokens over time'}
                    hint={`Daily totals, stacked by ${stackBy}. Days with no activity read as zero.`}
                    actions={
                      <>
                        <Segmented
                          label="Stack"
                          value={stackBy}
                          onChange={setStackBy}
                          options={[
                            { value: 'client', label: 'Client' },
                            { value: 'provider', label: 'Provider' },
                            { value: 'model', label: 'Model' },
                          ]}
                        />
                        <Segmented
                          label="Show"
                          value={metric}
                          onChange={setMetric}
                          options={[
                            { value: 'cost', label: 'Cost' },
                            { value: 'tokens', label: 'Tokens' },
                          ]}
                        />
                      </>
                    }
                  />
                  <CostOverTime
                    series={report.series}
                    stackBy={stackBy}
                    metric={metric}
                    identityIndex={identityIndex}
                    labelFor={labelFor}
                    mode={mode}
                  />
                </Card>

                <div className="grid grid-cols-1 gap-4 xl:grid-cols-2">
                  <Card>
                    <CardHeader
                      title="Cost by model"
                      hint="API-equivalent spend for each model in this slice."
                    />
                    <CostByModel
                      buckets={report.by_model}
                      identityIndex={modelIndex}
                      mode={mode}
                    />
                  </Card>

                  <Card>
                    <CardHeader
                      title="Token mix"
                      hint="Where each model’s tokens went. Cache reads dominate — they bill at a tenth of the input price."
                    />
                    <TokenMix buckets={report.by_model} mode={mode} />
                  </Card>
                </div>

                <Card>
                  <CardHeader
                    title="By project"
                    hint="Attributed from each session's working directory. Sessions without one land in (no project)."
                  />
                  <ProjectBreakdown buckets={report.by_project} />
                </Card>

                <Card>
                  <CardHeader
                    title="Sessions"
                    hint={`${formatCount(report.sessions.length)} sessions in this slice — click a column header to re-sort.`}
                  />
                  <SessionsTable
                    report={report}
                    clientLabel={clientLabel}
                    clientIndex={clientIndex}
                    providerLabel={providerLabel}
                    providerIndex={providerIndex}
                    modelLabel={modelLabel}
                    modelIndex={modelIndex}
                    mode={mode}
                  />
                </Card>
              </>
            )}

            <p className="pt-1 pb-2 text-center text-[12px] text-muted">
              Report generated {formatTimestamp(report.generated_at)} · list prices as of{' '}
              {report.rates_as_of} · nothing left this machine.
            </p>
          </div>
        )}
      </main>
    </div>
  )
}
