import { useState } from 'react'
import type { JSX } from 'react'
import type { CostState, Meta, Query, Report, SeriesPoint, SessionRow, View } from './api'
import {
  RECENCY_DAYS,
  daySpan,
  formatCount,
  formatDayShort,
  formatDuration,
  formatMoney,
  formatMoneyShort,
  formatPercent,
  formatTokens,
  isRecent,
  logSpanMs,
  sessionDisplayName,
} from './format'
import { TimeChart, type TimeSeriesRow } from '@/components/chart-time'
import { Panel, PanelBody, PanelHeader, PanelNote } from '@/components/panel'
import { worstState } from '@/components/rank'
import { seriesColor, TOKEN_BUCKETS } from '@/components/series'
import { SourceCard } from '@/components/source-card'
import { Sparkline } from '@/components/sparkline'
import { Stat, StatGrid, StatLabel } from '@/components/stat'
import { EmptyState } from '@/components/states'
import {
  BucketBar,
  ComparisonMeter,
  COST_STATE_META,
  Legend,
  MeterRow,
  PartialMarker,
  ProvenanceBadge,
  Unavailable,
} from '@/components/status'
import { ToggleGroup, ToggleGroupItem } from '@/components/ui/toggle-group'
import { cn } from '@/design-system/cn'

type StackBy = 'client' | 'provider' | 'model'
type Metric = 'cost' | 'tokens'

function sortedDays(report: Report): string[] {
  return [...report.by_day].map((bucket) => bucket.key).sort()
}

function sourceTrend(report: Report, days: string[], sourceId: string, useCost: boolean): number[] {
  const totals = new Map<string, number>()
  for (const point of report.series) {
    if (point.source !== sourceId) continue
    totals.set(point.day, (totals.get(point.day) ?? 0) + (useCost ? point.cost : point.events))
  }
  return days.map((day) => totals.get(day) ?? 0)
}

function DetectedSourcesPanel({
  meta,
  report,
  onSelectView,
}: {
  meta: Meta
  report: Report
  onSelectView: (view: View) => void
}) {
  const TOP_SOURCES = 3
  const detected = meta.sources.filter((source) => source.detected)
  const days = sortedDays(report)
  const dayLabels = days.map(formatDayShort)

  const ranked = detected
    .map((source) => {
      const isFull = source.token_data === 'full'
      const ownSessions = report.sessions.filter((session) => session.source === source.id)
      const priced = ownSessions.some((session) => session.cost !== null)
      const cost = ownSessions.reduce(
        (sum, session) => sum + (session.cost ? session.cost.total : 0),
        0,
      )
      const requests = ownSessions.reduce((sum, session) => sum + session.request_count, 0)
      const tokensTotal = ownSessions.reduce(
        (sum, session) => sum + (session.tokens ? session.tokens.total : 0),
        0,
      )
      const lastSeen = ownSessions.reduce(
        (latest, session) => (session.start_time > latest ? session.start_time : latest),
        '',
      )
      const showsCost = isFull && priced
      const partialCost = priced && ownSessions.some((session) => session.cost === null)
      return {
        source, isFull, priced, cost, requests, tokensTotal, lastSeen, showsCost, partialCost,
        sessionCount: ownSessions.length,
      }
    })
    .sort((a, b) => {
      if (a.showsCost !== b.showsCost) return a.showsCost ? -1 : 1
      if (a.showsCost) return b.cost - a.cost
      return b.lastSeen.localeCompare(a.lastSeen)
    })
  const shown = ranked.slice(0, TOP_SOURCES)
  const hiddenCount = meta.sources.length - shown.length

  return (
    <Panel>
      <PanelHeader
        eyebrow="Detected on this machine"
        title={`${detected.length} of ${meta.sources.length} readers found logs`}
        hint="Sources with token counts carry cost. The rest log sessions only, and their cost is never invented."
      />
      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3">
        {shown.map(
          (
            { source, isFull, priced, cost, requests, tokensTotal, showsCost, partialCost, sessionCount },
            index,
          ) => (
          <SourceCard
            key={source.id}
            source={{
              id: source.id,
              label: source.label,
              path: source.path,
              hasTokens: isFull,
              headline: isFull ? (
                priced ? (
                  <span className="inline-flex items-center gap-1.5">
                    {formatMoney(cost)}
                    {partialCost && (
                      <PartialMarker hint="Some sessions from this reader have no priced cost, so this total covers only the priced ones." />
                    )}
                  </span>
                ) : (
                  <Unavailable />
                )
              ) : (
                formatCount(requests)
              ),
              foot: isFull
                ? `${formatCount(sessionCount)} sessions, ${formatTokens(tokensTotal)} tokens`
                : 'requests logged, no token counts',
              color: seriesColor(index),
              trend: sourceTrend(report, days, source.id, showsCost),
              trendLabels: dayLabels,
              formatTrend: showsCost ? formatMoney : formatCount,
              trendSeriesLabel: showsCost ? 'Cost' : 'Requests',
            }}
          />
        ))}
      </div>
      {hiddenCount > 0 ? (
        <button
          type="button"
          onClick={() => onSelectView('sources')}
          className="w-full px-card py-3 text-left text-xs text-muted-foreground hover:text-foreground"
        >
          {`${hiddenCount} more readers aren't shown here, ranked lower by cost and recency, or not found on this machine`}
        </button>
      ) : null}
    </Panel>
  )
}

function KpiRow({ report }: { report: Report }) {
  const days = sortedDays(report)
  const dayLabels = days.map(formatDayShort)
  const byDay = new Map(report.by_day.map((bucket) => [bucket.key, bucket]))
  const costPerDay = days.map((day) => byDay.get(day)?.cost.total ?? 0)
  const cacheReadPerDay = days.map((day) => byDay.get(day)?.tokens.cache_read ?? 0)
  const requestsPerDay = days.map((day) => byDay.get(day)?.events ?? 0)
  const sessionsPerDay = days.map((day) => byDay.get(day)?.sessions ?? 0)
  const cacheSavedPerDay = days.map((day) => byDay.get(day)?.cost.cache_savings ?? 0)

  const totals = report.totals
  const avgFoot =
    totals.sessions > 0
      ? `${formatMoney(totals.cost.total / totals.sessions)} average each`
      : 'none in this slice'
  const cachePriced = totals.cost.no_cache_equivalent > 0
  const cacheSaveFoot = cachePriced
    ? `${formatPercent(totals.cost.cache_savings / totals.cost.no_cache_equivalent)} off the no cache price`
    : 'no priced tokens'

  return (
    <StatGrid className="xl:grid-cols-6">
      <Stat
        label="API equivalent cost"
        value={totals.cost.total}
        format={formatMoney}
        emphasis="hero"
        className="sm:col-span-2"
        hint={`What ${formatCount(totals.events)} requests would cost at published list prices.`}
      >
        <Sparkline
          values={costPerDay}
          width={240}
          height={34}
          color="var(--primary)"
          fill
          stretch
          labels={dayLabels}
          format={formatMoney}
          seriesLabel="Cost"
        />
      </Stat>

      <Stat
        label="Tokens"
        value={totals.tokens.total}
        format={formatTokens}
        hint={`${formatTokens(totals.tokens.cache_read)} of it cache reads`}
      >
        <Sparkline
          values={cacheReadPerDay}
          stretch
          labels={dayLabels}
          format={formatTokens}
          seriesLabel="Cache reads"
        />
      </Stat>

      <Stat
        label="Requests"
        value={totals.events}
        format={formatCount}
        hint={`across ${formatCount(report.files_scanned)} log files`}
      >
        <Sparkline
          values={requestsPerDay}
          stretch
          labels={dayLabels}
          format={formatCount}
          seriesLabel="Requests"
        />
      </Stat>

      <Stat label="Sessions" value={totals.sessions} format={formatCount} hint={avgFoot}>
        <Sparkline
          values={sessionsPerDay}
          stretch
          labels={dayLabels}
          format={formatCount}
          seriesLabel="Sessions"
        />
      </Stat>

      <Stat
        label="Cache saved"
        value={
          cachePriced ? (
            totals.cost.cache_savings
          ) : (
            <Unavailable hint="No priced tokens in this slice, so there is no saving to measure." />
          )
        }
        format={formatMoney}
        hint={cacheSaveFoot}
      >
        {cachePriced ? (
          <Sparkline
            values={cacheSavedPerDay}
            stretch
            labels={dayLabels}
            format={formatMoney}
            seriesLabel="Cache saved"
          />
        ) : null}
      </Stat>
    </StatGrid>
  )
}

function OutcomeRow({ report }: { report: Report }) {
  const sessions = report.sessions
  const rated = sessions.filter((session) => session.outcome !== 'unrated')
  const successful = rated.filter((session) => session.outcome === 'successful')
  const tokens = successful.reduce(
    (sum, session) => sum + (session.tokens ? session.tokens.total : 0),
    0,
  )
  const cost = successful.reduce(
    (sum, session) => sum + (session.cost ? session.cost.total : 0),
    0,
  )
  const costPartial = successful.some((session) => session.cost === null)
  const noneRatedFoot = `Nothing is rated yet, so there is no rate to show. Rate a session in its workspace, then rescan: ${formatCount(sessions.length)} sessions are unrated.`
  const noneSuccessfulFoot =
    rated.length > 0
      ? 'No rated session in this slice came out successful.'
      : 'Available once a session is rated successful.'

  return (
    <StatGrid className="xl:grid-cols-3">
      <Stat
        label="Success rate"
        value={
          rated.length > 0 ? formatPercent(successful.length / rated.length) : <Unavailable />
        }
        hint={
          rated.length > 0
            ? `${formatCount(successful.length)} of ${formatCount(rated.length)} rated sessions succeeded, ${formatCount(sessions.length - rated.length)} still unrated`
            : noneRatedFoot
        }
      />
      <Stat
        label="Tokens per success"
        value={successful.length > 0 ? formatTokens(tokens / successful.length) : <Unavailable />}
        hint={
          successful.length > 0
            ? `${formatTokens(tokens)} across ${formatCount(successful.length)} successful sessions`
            : noneSuccessfulFoot
        }
      />
      <Stat
        label="Cost per success"
        value={
          successful.length > 0 ? (
            <span className="inline-flex items-center gap-1.5">
              {formatMoney(cost / successful.length)}
              {costPartial && (
                <PartialMarker hint="Some successful sessions have no priced cost, so only the priced ones are averaged in." />
              )}
            </span>
          ) : (
            <Unavailable />
          )
        }
        hint={
          successful.length > 0
            ? `${formatMoney(cost)} of list price bought ${formatCount(successful.length)} successful sessions`
            : noneSuccessfulFoot
        }
      />
    </StatGrid>
  )
}

function HeavyRow({
  session,
  report,
  value,
}: {
  session: SessionRow
  report: Report
  value: string
}) {
  const model = session.models[0] ?? '(no model)'
  const label = report.by_model.find((bucket) => bucket.key === model)?.label ?? model

  return (
    <div className="flex items-baseline gap-3 py-1">
      <div className="min-w-0 flex-1">
        <div className="tabular truncate text-xs font-medium">{sessionDisplayName(session)}</div>
        <div className="truncate text-[11px] text-muted-foreground">{`${session.client}, ${label}`}</div>
      </div>
      <div className="tabular shrink-0 text-[13px] font-medium">{value}</div>
    </div>
  )
}

function HeaviestSessionsPanel({ report }: { report: Report }) {
  const byCost = [...report.sessions]
    .filter((session) => session.cost !== null)
    .sort((a, b) => (b.cost?.total ?? 0) - (a.cost?.total ?? 0))
    .slice(0, 6)
  const bySpan = [...report.sessions]
    .filter((session) => logSpanMs(session) > 0)
    .sort((a, b) => logSpanMs(b) - logSpanMs(a))
    .slice(0, 6)

  return (
    <Panel>
      <PanelHeader
        eyebrow="Heaviest sessions"
        title={
          byCost.length > 0
            ? `The costliest session is ${formatMoney(byCost[0].cost?.total ?? 0)}`
            : 'No priced session in this slice'
        }
      />
      <PanelBody>
        <div className="grid grid-cols-1 gap-x-6 lg:grid-cols-2">
          <div>
            <StatLabel className="pb-2">Most expensive</StatLabel>
            {byCost.map((session) => (
              <HeavyRow
                key={`cost-${session.source}-${session.session_id}`}
                session={session}
                report={report}
                value={formatMoney(session.cost?.total ?? 0)}
              />
            ))}
            {byCost.length === 0 ? (
              <Unavailable hint="No session in this slice carried a priced token count, so there is nothing to rank." />
            ) : null}
          </div>
          <div>
            <div className="flex items-center gap-2 pb-2">
              <StatLabel>Longest log span</StatLabel>
              <ProvenanceBadge
                provenance="derived"
                title="The last log record minus the first, so it counts every idle minute between prompts."
              />
            </div>
            {bySpan.map((session) => (
              <HeavyRow
                key={`span-${session.source}-${session.session_id}`}
                session={session}
                report={report}
                value={formatDuration(logSpanMs(session))}
              />
            ))}
            {bySpan.length === 0 ? (
              <Unavailable hint="No session in this slice has both a start and a later end time." />
            ) : null}
          </div>
        </div>
      </PanelBody>
      <PanelNote>
        Cost is the list price of the session&rsquo;s own requests. The span is the last log record
        minus the first, derived, so it counts every idle minute between prompts and is not working
        time. Outcomes come from the last scan, so a rating shows up here after the next rescan.
      </PanelNote>
    </Panel>
  )
}

function TimeChartPanel({
  report,
  meta,
  query,
}: {
  report: Report
  meta: Meta
  query: Query
}) {
  const [stackBy, setStackBy] = useState<StackBy>('client')
  const [metric, setMetric] = useState<Metric>('cost')

  const clientLabel = (id: string) => meta.clients.find((client) => client.id === id)?.label ?? id
  const modelLabel = (id: string) => report.by_model.find((bucket) => bucket.key === id)?.label ?? id

  const keyOf = (point: SeriesPoint) =>
    stackBy === 'client' ? point.client : stackBy === 'provider' ? point.provider : point.model
  const labelOf = (point: SeriesPoint) =>
    stackBy === 'client'
      ? clientLabel(point.client)
      : stackBy === 'provider'
        ? point.provider
        : modelLabel(point.model)

  const rows: TimeSeriesRow[] = report.series.map((point) => ({
    day: point.day,
    key: keyOf(point),
    label: labelOf(point),
    value: metric === 'cost' ? point.cost : point.tokens,
  }))

  const days = query.since && query.until ? daySpan(query.since, query.until) : sortedDays(report)

  return (
    <Panel>
      <PanelHeader
        eyebrow={metric === 'cost' ? 'Cost over time' : 'Tokens over time'}
        title={`Daily totals stacked by ${stackBy}, ${days.length} days`}
        actions={
          <div className="flex flex-wrap items-center gap-2">
            <ToggleGroup
              type="single"
              variant="outline"
              size="sm"
              value={stackBy}
              onValueChange={(value) => value && setStackBy(value as StackBy)}
            >
              <ToggleGroupItem value="client">Client</ToggleGroupItem>
              <ToggleGroupItem value="provider">Provider</ToggleGroupItem>
              <ToggleGroupItem value="model">Model</ToggleGroupItem>
            </ToggleGroup>
            <ToggleGroup
              type="single"
              variant="outline"
              size="sm"
              value={metric}
              onValueChange={(value) => value && setMetric(value as Metric)}
            >
              <ToggleGroupItem value="cost">Cost</ToggleGroupItem>
              <ToggleGroupItem value="tokens">Tokens</ToggleGroupItem>
            </ToggleGroup>
          </div>
        }
      />
      <PanelBody>
        {rows.length === 0 ? (
          <EmptyState
            title="No requests in this slice"
            description="Widen the date range or clear a filter."
          />
        ) : (
          <TimeChart
            days={days}
            rows={rows}
            format={metric === 'cost' ? formatMoney : formatTokens}
            formatAxis={metric === 'cost' ? formatMoneyShort : formatTokens}
            formatDay={formatDayShort}
          />
        )}
      </PanelBody>
      <PanelNote>
        Bars are one day. The dashed line is the slice mean. Gaps are days with no logged requests.
      </PanelNote>
    </Panel>
  )
}

function modelFallbackStates(report: Report): Map<string, CostState> {
  const statesByModel = new Map<string, Set<CostState>>()
  for (const session of report.sessions) {
    const states = session.cost_states.length > 0 ? session.cost_states : [session.cost_state]
    for (const model of session.models) {
      const set = statesByModel.get(model) ?? new Set<CostState>()
      for (const state of states) set.add(state)
      statesByModel.set(model, set)
    }
  }
  const unknownModels = new Set(report.unknown_models.map((unknown) => unknown.model))
  const result = new Map<string, CostState>()
  for (const [model, states] of statesByModel) {
    if (unknownModels.has(model)) {
      result.set(model, 'unpriced')
      continue
    }
    const nonPriced = [...states].filter((state) => state !== 'priced')
    result.set(model, nonPriced.length > 0 ? worstState(nonPriced) : 'unavailable')
  }
  return result
}

const UNATTRIBUTED = '(no project)'

function projectFallbackStates(report: Report): Map<string, CostState> {
  const statesByProject = new Map<string, Set<CostState>>()
  for (const session of report.sessions) {
    const key = session.project ?? UNATTRIBUTED
    const states = session.cost_states.length > 0 ? session.cost_states : [session.cost_state]
    const set = statesByProject.get(key) ?? new Set<CostState>()
    for (const state of states) set.add(state)
    statesByProject.set(key, set)
  }
  const result = new Map<string, CostState>()
  for (const [project, states] of statesByProject) {
    const nonPriced = [...states].filter((state) => state !== 'priced')
    result.set(project, nonPriced.length > 0 ? worstState(nonPriced) : 'unavailable')
  }
  return result
}

function CostByModelPanel({ report, meta, today }: { report: Report; meta: Meta; today: string }) {
  const sorted = [...report.by_model].sort((a, b) => b.cost.total - a.cost.total)
  const [showAll, setShowAll] = useState(false)
  const recent = sorted.filter((bucket) => isRecent(meta.model_last_seen[bucket.key], today))
  const stale = sorted.filter((bucket) => !isRecent(meta.model_last_seen[bucket.key], today))
  const buckets = showAll ? sorted : recent.length > 0 ? recent : sorted
  const maxCost = Math.max(...buckets.map((bucket) => bucket.cost.total), 0.01)
  const fallbackStates = modelFallbackStates(report)
  const totalCost = report.totals.cost.total
  const top = buckets[0]
  const headline = top
    ? `${top.label} carries ${totalCost > 0 ? formatPercent(top.cost.total / totalCost) : '0%'} of the spend`
    : 'No priced models in this slice'

  return (
    <Panel>
      <PanelHeader eyebrow="Cost by model" title={headline} />
      <PanelBody className="py-3">
        {buckets.map((bucket, index) => {
          const priced = bucket.cost.total > 0
          const state = priced ? null : (fallbackStates.get(bucket.key) ?? 'unavailable')

          return (
            <MeterRow
              key={bucket.key}
              label={bucket.label}
              meta={
                state
                  ? `${formatCount(bucket.sessions)} sessions, ${state}`
                  : `${formatCount(bucket.sessions)} sessions`
              }
              value={
                priced ? (
                  formatMoney(bucket.cost.total)
                ) : state === 'free' ? (
                  '$0.00'
                ) : (
                  <Unavailable />
                )
              }
              share={
                priced
                  ? totalCost > 0
                    ? formatPercent(bucket.cost.total / totalCost)
                    : '0%'
                  : undefined
              }
              fraction={
                priced ? (bucket.cost.total / maxCost) * 0.92 : state === 'free' ? 0 : null
              }
              color={priced ? seriesColor(index) : COST_STATE_META[state ?? 'unavailable'].color}
            />
          )
        })}
      </PanelBody>
      <PanelNote>
        Bars are absolute spend, the number beside each bar is its share. Free and unpriced models
        keep their row so nothing disappears from view.
        {!showAll && stale.length > 0 && recent.length > 0 && (
          <>
            {' '}
            <button
              type="button"
              className="font-medium text-primary hover:underline"
              onClick={() => setShowAll(true)}
            >
              {`Show ${formatCount(stale.length)} more not used in ${RECENCY_DAYS} days`}
            </button>
          </>
        )}
      </PanelNote>
    </Panel>
  )
}

function TokenMixPanel({ report }: { report: Report }) {
  const buckets = report.by_model.filter((bucket) => bucket.tokens.total > 0)
  const totals = report.totals.tokens
  const cacheShare = totals.input_total > 0 ? totals.cache_read / totals.input_total : 0

  return (
    <Panel>
      <PanelHeader
        eyebrow="Token mix"
        title={`${formatPercent(cacheShare)} cache hit ratio`}
      />
      <PanelBody className="space-y-3">
        <Legend
          items={TOKEN_BUCKETS.map((segment) => ({
            key: segment.key,
            label: segment.label,
            color: segment.color,
            value: segment.multiplier,
          }))}
        />
        <div className="space-y-3 pt-1">
          {buckets.map((bucket) => (
            <div key={bucket.key} className="space-y-1.5">
              <div className="flex justify-between gap-3 text-xs">
                <span className="truncate">{bucket.label}</span>
                <span className="tabular text-muted-foreground">
                  {formatTokens(bucket.tokens.total)}
                </span>
              </div>
              <BucketBar
                formatValue={formatTokens}
                segments={TOKEN_BUCKETS.map((segment) => ({
                  key: segment.key,
                  label: segment.label,
                  value: bucket.tokens[segment.key],
                  color: segment.color,
                }))}
              />
            </div>
          ))}
        </div>
      </PanelBody>
      <PanelNote>
        Cache reads bill at a tenth of the input price, so the widest band is also the cheapest.
        Output is the narrow band that costs the most.
      </PanelNote>
    </Panel>
  )
}

function CacheSavingsPanel({ report }: { report: Report }) {
  const cost = report.totals.cost
  const priced = cost.no_cache_equivalent > 0
  const negative = cost.cache_savings < 0
  const magnitude = priced
    ? formatPercent(Math.abs(cost.cache_savings) / cost.no_cache_equivalent)
    : ''
  const headline = !priced
    ? 'No priced tokens in this slice'
    : negative
      ? `Caching added ${magnitude} to the bill`
      : `Caching cut the bill by ${magnitude}`
  const scale = Math.max(cost.no_cache_equivalent, cost.total, 0.01)

  return (
    <Panel>
      <PanelHeader eyebrow="Cache savings" title={headline} />
      <PanelBody className="space-y-4">
        <ComparisonMeter
          caption="Same tokens billed with no cache discount"
          value={formatMoney(cost.no_cache_equivalent)}
          fraction={priced ? cost.no_cache_equivalent / scale : null}
          color="var(--muted-foreground)"
        />
        <ComparisonMeter
          caption="Actually billed at cache rates"
          value={formatMoney(cost.total)}
          fraction={priced ? cost.total / scale : null}
          color={negative ? 'var(--destructive)' : undefined}
        />
        <div className="flex items-baseline gap-3 border-t pt-4">
          {priced ? (
            <span
              className={cn(
                'tabular text-2xl font-semibold',
                negative ? 'text-destructive' : 'text-success',
              )}
            >
              {formatMoney(cost.cache_savings)}
            </span>
          ) : (
            <Unavailable hint="No priced tokens in this slice, so there is no saving to measure." />
          )}
          <span className="text-xs leading-relaxed text-muted-foreground">
            {negative
              ? 'more than the same tokens would have cost with every read and write at full input price.'
              : 'saved against the same tokens billed with every read and write at full input price.'}
          </span>
        </div>
      </PanelBody>
    </Panel>
  )
}

const TOP_PROJECTS = 5

function ByProjectPanel({ report }: { report: Report }) {
  const sorted = [...report.by_project].sort((a, b) => b.cost.total - a.cost.total)
  const [showAll, setShowAll] = useState(false)
  const buckets = showAll ? sorted : sorted.slice(0, TOP_PROJECTS)
  const hidden = sorted.length - buckets.length
  const maxCost = Math.max(...buckets.map((bucket) => bucket.cost.total), 0.01)
  const fallbackStates = projectFallbackStates(report)
  const headline = sorted.length
    ? `${sorted.length} projects, led by ${sorted[0].label}`
    : 'No sessions in this slice'

  return (
    <Panel>
      <PanelHeader eyebrow="By project" title={headline} />
      <PanelBody className="py-3">
        {buckets.map((bucket, index) => {
          const priced = bucket.cost.total > 0
          const state = priced ? null : (fallbackStates.get(bucket.key) ?? 'unavailable')

          return (
            <MeterRow
              key={bucket.key}
              label={bucket.label}
              meta={
                state
                  ? `${formatCount(bucket.sessions)} sessions, ${state}`
                  : `${formatCount(bucket.sessions)} sessions, ${formatCount(bucket.events)} req`
              }
              value={
                priced ? (
                  formatMoney(bucket.cost.total)
                ) : state === 'free' ? (
                  '$0.00'
                ) : (
                  <Unavailable />
                )
              }
              fraction={priced ? bucket.cost.total / maxCost : state === 'free' ? 0 : null}
              color={seriesColor(index)}
            />
          )
        })}
      </PanelBody>
      <PanelNote>
        Attributed from each session&rsquo;s working directory. Sessions without one land in (no
        project).
        {!showAll && hidden > 0 && (
          <>
            {' '}
            <button
              type="button"
              className="font-medium text-primary hover:underline"
              onClick={() => setShowAll(true)}
            >
              {`Show ${formatCount(hidden)} more`}
            </button>
          </>
        )}
      </PanelNote>
    </Panel>
  )
}

export default function Overview(props: {
  report: Report
  meta: Meta
  query: Query
  today: string
  onSelectView: (view: View) => void
}): JSX.Element {
  const { report, meta, query, today, onSelectView } = props

  return (
    <div className="flex flex-col gap-3">
      <DetectedSourcesPanel meta={meta} report={report} onSelectView={onSelectView} />
      <KpiRow report={report} />
      <OutcomeRow report={report} />
      <HeaviestSessionsPanel report={report} />
      <TimeChartPanel report={report} meta={meta} query={query} />
      <div className="grid grid-cols-1 gap-3 xl:grid-cols-2">
        <CostByModelPanel report={report} meta={meta} today={today} />
        <TokenMixPanel report={report} />
      </div>
      <div className="grid grid-cols-1 gap-3 xl:grid-cols-2">
        <CacheSavingsPanel report={report} />
        <ByProjectPanel report={report} />
      </div>
    </div>
  )
}
