import { useState } from 'react'

import { ToggleGroup, ToggleGroupItem } from '@/components/ui/toggle-group'
import { TimeChart, type TimeSeriesRow } from '@/components/chart-time'
import { Panel, PanelBody, PanelHeader, PanelNote } from '@/components/panel'
import { seriesColor, TOKEN_BUCKETS } from '@/components/series'
import { Sparkline } from '@/components/sparkline'
import { Stat, StatGrid } from '@/components/stat'
import {
  BucketBar,
  ComparisonMeter,
  COST_STATE_META,
  Legend,
  MeterRow,
} from '@/components/status'
import { SourceCard } from '@/components/source-card'
import {
  formatCount,
  formatDayShort,
  formatMoney,
  formatMoneyShort,
  formatPercent,
  formatTokens,
} from '@/format'
import {
  DAYS,
  MODELS,
  PROJECTS,
  PROTOTYPE_SLICE,
  PROJECT_PEAK,
  SERIES,
  SOURCES,
  TOTALS,
  sourceTrend,
} from './data'

const DAY_LABELS = DAYS.map(formatDayShort)

type StackBy = 'client' | 'provider' | 'model'
type Metric = 'cost' | 'tokens'

function DetectedSources({ onSeeAll }: { onSeeAll: () => void }) {
  const detected = SOURCES.filter((source) => source.detected)
  const missing = SOURCES.length - detected.length

  return (
    <Panel>
      <PanelHeader
        eyebrow="Detected on this machine"
        title={`${detected.length} of ${SOURCES.length} readers found logs`}
        hint="Sources with token counts carry cost. The rest log sessions only, and their cost is never invented."
      />
      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3">
        {detected.map((source) => (
          <SourceCard
            key={source.id}
            source={{
              id: source.id,
              label: source.label,
              path: source.path,
              hasTokens: source.hasTokens,
              color: seriesColor(source.slot),
              headline: source.hasTokens ? formatMoney(source.cost) : formatCount(source.requests),
              foot: source.hasTokens
                ? `${formatCount(source.sessions)} sessions logged`
                : 'requests logged, no token counts',
              trend: sourceTrend(source.id, source.hasTokens),
              trendLabels: DAY_LABELS,
              formatTrend: source.hasTokens ? formatMoney : formatCount,
              trendSeriesLabel: source.hasTokens ? 'Cost' : 'Requests',
            }}
          />
        ))}
      </div>
      {missing > 0 ? (
        <button
          type="button"
          onClick={onSeeAll}
          className="w-full px-card py-3 text-left text-xs text-muted-foreground hover:text-foreground"
        >
          {missing} more readers ship with the tool and aren&rsquo;t found here
        </button>
      ) : null}
    </Panel>
  )
}

function KpiRow() {
  const costPerDay = PROTOTYPE_SLICE.costPerDay
  const averagePerSession = TOTALS.cost / TOTALS.sessions

  return (
    <StatGrid className="xl:grid-cols-6">
      <Stat
        label="API equivalent cost"
        value={TOTALS.cost}
        format={formatMoney}
        emphasis="hero"
        className="sm:col-span-2"
        hint={`What ${formatCount(TOTALS.requests)} requests would cost at published list prices.`}
      >
        <Sparkline
          values={costPerDay}
          width={240}
          height={34}
          color="var(--primary)"
          fill
          stretch
          labels={DAY_LABELS}
          format={formatMoney}
          seriesLabel="Cost"
        />
      </Stat>

      <Stat
        label="Tokens"
        value={TOTALS.tokens.total}
        format={formatTokens}
        hint={`${formatTokens(TOTALS.tokens.cache_read)} of it cache reads`}
      >
        <Sparkline values={PROTOTYPE_SLICE.cacheReadPerDay} stretch labels={DAY_LABELS} format={formatTokens} seriesLabel="Cache reads" />
      </Stat>
      <Stat
        label="Requests"
        value={TOTALS.requests}
        format={formatCount}
        hint={`across ${formatCount(TOTALS.files)} log files`}
      >
        <Sparkline values={PROTOTYPE_SLICE.requestsPerDay} stretch labels={DAY_LABELS} format={formatCount} seriesLabel="Requests" />
      </Stat>
      <Stat
        label="Sessions"
        value={TOTALS.sessions}
        format={formatCount}
        hint={`${formatMoney(averagePerSession)} average each`}
      >
        <Sparkline values={PROTOTYPE_SLICE.sessionsPerDay} stretch labels={DAY_LABELS} format={formatCount} seriesLabel="Sessions" />
      </Stat>
      <Stat
        label="Cache saved"
        value={TOTALS.cacheSavings}
        format={formatMoney}
        hint={`${formatPercent(TOTALS.cacheSavings / TOTALS.noCacheEquivalent)} off the no cache price`}
      >
        <Sparkline values={PROTOTYPE_SLICE.cacheSavedPerDay} stretch labels={DAY_LABELS} format={formatMoney} seriesLabel="Cache saved" />
      </Stat>
    </StatGrid>
  )
}

function TimeChartPanel() {
  const [stackBy, setStackBy] = useState<StackBy>('client')
  const [metric, setMetric] = useState<Metric>('cost')

  const labelFor = (point: (typeof SERIES)[number]) => {
    if (stackBy === 'client') return PROTOTYPE_SLICE.clientLabel(point.client)
    if (stackBy === 'provider') return point.provider
    return PROTOTYPE_SLICE.modelLabel(point.model)
  }

  const rows: TimeSeriesRow[] = SERIES.map((point) => ({
    day: point.day,
    key: stackBy === 'client' ? point.client : stackBy === 'provider' ? point.provider : point.model,
    label: labelFor(point),
    value: metric === 'cost' ? point.cost : point.tokens,
  }))

  const format = metric === 'cost' ? formatMoney : formatTokens
  const formatAxis = metric === 'cost' ? formatMoneyShort : formatTokens

  return (
    <Panel>
      <PanelHeader
        eyebrow={metric === 'cost' ? 'Cost over time' : 'Tokens over time'}
        title={`Daily totals stacked by ${stackBy}, ${DAYS.length} days`}
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
        <TimeChart
          days={DAYS}
          rows={rows}
          format={format}
          formatAxis={formatAxis}
          formatDay={formatDayShort}
        />
      </PanelBody>
      <PanelNote>
        Bars are one day. The dashed line is the slice mean. Gaps are days with no logged requests.
      </PanelNote>
    </Panel>
  )
}

function CostByModelPanel() {
  const ranked = [...MODELS].sort((a, b) => b.cost - a.cost)
  const peak = Math.max(...ranked.map((model) => model.cost), 0.01)
  const top = ranked[0]

  return (
    <Panel>
      <PanelHeader
        eyebrow="Cost by model"
        title={`${top.label} carries ${formatPercent(top.cost / TOTALS.cost)} of the spend`}
      />
      <PanelBody className="py-3">
        {ranked.map((model, index) => {
          const priced = model.cost > 0
          return (
            <MeterRow
              key={model.key}
              label={model.label}
              meta={
                priced
                  ? `${formatCount(model.sessions)} sessions`
                  : `${formatCount(model.sessions)} sessions · ${model.state}`
              }
              value={priced ? formatMoney(model.cost) : model.state === 'free' ? '$0.00' : 'n/a'}
              share={priced ? formatPercent(model.cost / TOTALS.cost) : undefined}
              fraction={priced ? (model.cost / peak) * 0.92 : 0}
              color={priced ? seriesColor(index) : COST_STATE_META[model.state].color}
            />
          )
        })}
      </PanelBody>
      <PanelNote>
        Bars are absolute spend, the number beside each bar is its share. Free and unpriced models
        keep their row so nothing disappears from view.
      </PanelNote>
    </Panel>
  )
}

function TokenMixPanel() {
  const withTokens = MODELS.filter(
    (model) => Object.values(model.tokens).reduce((a, b) => a + b, 0) > 0,
  )
  const cacheShare = TOTALS.tokens.cache_read / TOTALS.tokens.total

  return (
    <Panel>
      <PanelHeader
        eyebrow="Token mix"
        title={`${formatPercent(cacheShare)} of all tokens are cache reads`}
      />
      <PanelBody className="space-y-3">
        <Legend
          items={TOKEN_BUCKETS.map((bucket) => ({
            key: bucket.key,
            label: bucket.label,
            color: bucket.color,
            value: bucket.multiplier,
          }))}
        />
        <div className="space-y-3 pt-1">
          {withTokens.map((model) => {
            const total = Object.values(model.tokens).reduce((a, b) => a + b, 0)
            return (
              <div key={model.key} className="space-y-1.5">
                <div className="flex justify-between gap-3 text-xs">
                  <span className="truncate">{model.label}</span>
                  <span className="tabular text-muted-foreground">{formatTokens(total)}</span>
                </div>
                <BucketBar
                  formatValue={formatTokens}
                  segments={TOKEN_BUCKETS.map((bucket) => ({
                    key: bucket.key,
                    label: bucket.label,
                    value: model.tokens[bucket.key],
                    color: bucket.color,
                  }))}
                />
              </div>
            )
          })}
        </div>
      </PanelBody>
      <PanelNote>
        Cache reads bill at a tenth of the input price, so the widest band is also the cheapest.
        Output is the narrow band that costs the most.
      </PanelNote>
    </Panel>
  )
}

function CacheSavingsPanel() {
  const share = TOTALS.cost / TOTALS.noCacheEquivalent

  return (
    <Panel>
      <PanelHeader
        eyebrow="Cache savings"
        title={`Caching cut the bill by ${formatPercent(TOTALS.cacheSavings / TOTALS.noCacheEquivalent)}`}
      />
      <PanelBody className="space-y-4">
        <ComparisonMeter
          caption="Same tokens billed with no cache discount"
          value={formatMoney(TOTALS.noCacheEquivalent)}
          fraction={1}
          color="var(--muted-foreground)"
        />
        <ComparisonMeter
          caption="Actually billed at cache rates"
          value={formatMoney(TOTALS.cost)}
          fraction={share}
        />
        <div className="flex items-baseline gap-3 border-t pt-4">
          <span className="tabular text-2xl font-semibold text-success">
            {formatMoney(TOTALS.cacheSavings)}
          </span>
          <span className="text-xs leading-relaxed text-muted-foreground">
            saved against the same tokens billed with every read and write at full input price.
          </span>
        </div>
      </PanelBody>
    </Panel>
  )
}

function ByProjectPanel() {
  return (
    <Panel>
      <PanelHeader
        eyebrow="By project"
        title={`${PROJECTS.length} projects, led by ${PROJECTS[0].label}`}
      />
      <PanelBody className="py-3">
        {PROJECTS.map((project, index) => (
          <MeterRow
            key={project.key}
            label={project.label}
            meta={`${formatCount(project.sessions)} sessions · ${formatCount(project.events)} req`}
            value={formatMoney(project.cost)}
            fraction={project.cost / PROJECT_PEAK}
            color={seriesColor(index)}
          />
        ))}
      </PanelBody>
      <PanelNote>
        Attributed from each session&rsquo;s working directory. Sessions without one land in (no
        project).
      </PanelNote>
    </Panel>
  )
}

export function OverviewScreen({ onSeeSources }: { onSeeSources: () => void }) {
  return (
    <div className="flex flex-col gap-3">
      <DetectedSources onSeeAll={onSeeSources} />
      <KpiRow />
      <TimeChartPanel />
      <div className="grid grid-cols-1 gap-3 xl:grid-cols-2">
        <CostByModelPanel />
        <TokenMixPanel />
      </div>
      <div className="grid grid-cols-1 gap-3 xl:grid-cols-2">
        <CacheSavingsPanel />
        <ByProjectPanel />
      </div>
    </div>
  )
}
