import { useState } from 'react'
import type { JSX, ReactNode } from 'react'
import { ChevronRightIcon } from 'lucide-react'
import type { ModelRate, ProviderRules, RateTable, Report, UnpricedModelEntry } from './api'
import { formatCount, formatMoney, formatTokens, plural } from './format'
import {
  type CacheField,
  type RateTag,
  bandText,
  cachePrice,
  formatContextWindow,
  matchUnpriced,
  mergedRules,
  peakText,
  periodText,
  priceText,
  providerLabel,
  rateTags,
  stalenessBadge,
  usd,
} from './pricing-format'
import { Panel, PanelBody, PanelHeader, PanelNote } from '@/components/panel'
import { MetricInfo } from '@/components/metric-info'
import { CostStateBadge, MeterRow, Unavailable } from '@/components/status'
import { CodeBlock, MetaGrid } from '@/components/detail'
import { EmptyState } from '@/components/states'
import { StatLabel } from '@/components/stat'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { cn } from '@/design-system/cn'

const REVEAL_BATCH = 20

const RATE_COLUMNS: { label: string; align: 'left' | 'right' }[] = [
  { label: 'Model', align: 'left' },
  { label: 'Provider', align: 'left' },
  { label: 'Input', align: 'right' },
  { label: 'Cache read', align: 'right' },
  { label: 'Cache write 5m', align: 'right' },
  { label: 'Cache write 1h', align: 'right' },
  { label: 'Output', align: 'right' },
  { label: 'Context window', align: 'right' },
  { label: 'State', align: 'right' },
  { label: 'Spend here', align: 'right' },
]

type RateState = 'free' | 'priced' | 'unused'

interface VariantTier {
  tier: string
  text: string
}

export interface EstimatedModel {
  model: string
  parentMatch: string
  parentDisplay: string
  tokens: number
  cost: number
}

interface RateRow {
  rate: ModelRate
  input: string
  output: string
  /** Null means the column cannot be shown: no published figure and no provider block. */
  cacheRead: string | null
  cacheWrite5m: string | null
  cacheWrite1h: string | null
  contextWindow: string | null
  tags: RateTag[]
  variants: VariantTier[]
  bands: string[]
  peak: string | null
  periods: string[]
  estimated: EstimatedModel[]
  spendValue: number
  spendLabel: ReactNode
  state: RateState
}

/** Buckets a rate row prices as its own, by model key (never by display label). */
function ownBuckets(rate: ModelRate, report: Report) {
  return report.by_model.filter((bucket) => {
    const match = report.model_matches[bucket.key]
    return (
      match !== undefined &&
      match.match === rate.match &&
      (match.kind === 'exact' || match.kind === 'suffix')
    )
  })
}

export function estimatedModels(rates: RateTable, report: Report): EstimatedModel[] {
  const result: EstimatedModel[] = []
  for (const bucket of report.by_model) {
    const match = report.model_matches[bucket.key]
    if (match === undefined || match.kind !== 'estimated' || match.match === null) continue
    const parent = rates.models.find((rate) => rate.match === match.match)
    result.push({
      model: bucket.key,
      parentMatch: match.match,
      parentDisplay: parent?.display ?? match.match,
      tokens: bucket.tokens.total,
      cost: bucket.cost.total,
    })
  }
  return result.sort((a, b) => b.cost - a.cost)
}

export function buildRow(
  rate: ModelRate,
  rates: RateTable,
  report: Report,
  estimatedAll: EstimatedModel[] = estimatedModels(rates, report),
): RateRow {
  const rules = mergedRules(rate, rates)
  const isFree = (rules ? rules.free : rate.cache_rules?.free === true) === true
  const spendValue = ownBuckets(rate, report).reduce((sum, bucket) => sum + bucket.cost.total, 0)
  const state: RateState = isFree ? 'free' : spendValue > 0 ? 'priced' : 'unused'
  const cache = (field: CacheField): string | null => {
    if (isFree) return 'free'
    const value = cachePrice(rate, rules, field)
    return value === null ? null : usd(value, 3)
  }

  return {
    rate,
    input: isFree ? 'free' : usd(rate.input),
    output: isFree ? 'free' : usd(rate.output),
    cacheRead: cache('cache_read'),
    cacheWrite5m: cache('cache_write_5m'),
    cacheWrite1h: cache('cache_write_1h'),
    contextWindow: formatContextWindow(rate.context_window),
    tags: rateTags(rate),
    variants: Object.entries(rate.variants).map(([tier, variant]) => ({
      tier,
      text: priceText(variant),
    })),
    bands: rate.bands.map(bandText),
    peak: rate.peak ? peakText(rate.peak) : null,
    periods: rate.periods.map((period) => periodText(period, rate)),
    estimated: estimatedAll.filter((item) => item.parentMatch === rate.match),
    spendValue,
    spendLabel: state === 'unused' ? <Unavailable /> : formatMoney(spendValue),
    state,
  }
}

function StateCell({ state }: { state: RateState }) {
  if (state === 'unused') {
    return (
      <Badge variant="outline" className="text-[10px] text-muted-foreground">
        unused
      </Badge>
    )
  }
  return <CostStateBadge state={state} />
}

function CacheCell({ value }: { value: string | null }) {
  return (
    <TableCell className="tabular text-right text-muted-foreground">
      {value === null ? (
        <Unavailable hint="This provider has no cache rules and the row publishes no absolute cache price." />
      ) : (
        value
      )}
    </TableCell>
  )
}

function TagBadge({ tag }: { tag: RateTag }) {
  const badge = (
    <Badge variant="outline" className={cn('text-[10px]', tag.key === 'unverified' && 'border-warning text-warning')}>
      {tag.label}
    </Badge>
  )
  if (!tag.hint) return badge
  return (
    <MetricInfo content={{ kind: 'simple', text: tag.hint }} ariaLabel={tag.hint}>
      {badge}
    </MetricInfo>
  )
}

function sourceTitle(rate: ModelRate): string {
  if (!rate.source) return 'No source recorded'
  return `${rate.source}${rate.verified ? ` (verified ${rate.verified})` : ' (not verified)'}`
}

function DetailList({ title, items }: { title: string; items: string[] }) {
  if (items.length === 0) return null
  return (
    <div className="space-y-1">
      <StatLabel>{title}</StatLabel>
      <ul className="tabular space-y-0.5 text-[11px]">
        {items.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </div>
  )
}

function hasDetail(row: RateRow): boolean {
  const { rate } = row
  return (
    row.variants.length > 0 ||
    row.bands.length > 0 ||
    row.peak !== null ||
    row.periods.length > 0 ||
    rate.note !== null ||
    rate.released !== null ||
    rate.retired !== null ||
    rate.source !== null
  )
}

function RowDetail({ row }: { row: RateRow }) {
  const { rate } = row
  const meta = [
    { label: 'Released', value: rate.released ?? '-' },
    { label: 'Retired', value: rate.retired ?? '-' },
    { label: 'Verified', value: rate.verified ?? 'never' },
    {
      label: 'Source',
      value: rate.source ? (
        <a
          href={rate.source}
          target="_blank"
          rel="noopener noreferrer"
          className="text-primary underline-offset-4 hover:underline"
        >
          source
        </a>
      ) : (
        '-'
      ),
    },
  ]
  return (
    <div className="max-w-3xl space-y-3 whitespace-normal py-1">
      <MetaGrid items={meta} className="sm:grid-cols-4" />
      {rate.note && <p className="text-xs leading-relaxed text-muted-foreground">{rate.note}</p>}
      <DetailList
        title="Variants"
        items={row.variants.map((variant) => `${variant.tier}: ${variant.text}`)}
      />
      {row.bands.length > 0 && (
        <div className="space-y-1">
          <DetailList title="Input-size bands" items={row.bands} />
          <p className="text-[11px] text-muted-foreground">
            The whole request is billed at the band rate once its input reaches the threshold.
          </p>
        </div>
      )}
      <DetailList title="Peak window" items={row.peak ? [row.peak] : []} />
      <DetailList title="Dated prices" items={row.periods} />
    </div>
  )
}

function ModelCell({ row, open, onToggle }: { row: RateRow; open: boolean; onToggle: () => void }) {
  const { rate } = row
  return (
    <TableCell title={sourceTitle(rate)}>
      <div className="flex items-center gap-1.5">
        <button
          type="button"
          onClick={onToggle}
          aria-expanded={open}
          aria-label={`${open ? 'Hide' : 'Show'} details for ${rate.display}`}
          disabled={!hasDetail(row)}
          className="-ml-1 inline-flex size-5 shrink-0 items-center justify-center rounded-sm text-muted-foreground hover:bg-accent hover:text-accent-foreground focus-visible:ring-[3px] focus-visible:ring-ring/50 focus-visible:outline-none disabled:opacity-30"
        >
          <ChevronRightIcon className={cn('size-3.5 transition-transform', open && 'rotate-90')} />
        </button>
        <span>{rate.display}</span>
        {row.tags.map((tag) => (
          <TagBadge key={tag.key} tag={tag} />
        ))}
      </div>
      <div className="tabular pl-[22px] text-[10px] text-muted-foreground">{rate.match}</div>
      {row.estimated.map((item) => (
        <div
          key={item.model}
          className="tabular mt-1 flex items-center gap-1.5 pl-[22px] text-[10px] text-muted-foreground"
        >
          <Badge variant="outline" className="text-[10px]">
            Estimated
          </Badge>
          {`estimated: ${item.model} ${formatMoney(item.cost)}`}
        </div>
      ))}
    </TableCell>
  )
}

function RateTablePanel({ rates, report }: { rates: RateTable; report: Report }) {
  const [revealed, setRevealed] = useState(0)
  const [expanded, setExpanded] = useState<ReadonlySet<string>>(new Set())

  const toggle = (match: string) =>
    setExpanded((current) => {
      const next = new Set(current)
      if (!next.delete(match)) next.add(match)
      return next
    })

  const estimatedAll = estimatedModels(rates, report)
  const sorted = rates.models
    .map((rate) => buildRow(rate, rates, report, estimatedAll))
    .sort(
      (a, b) =>
        b.spendValue + b.estimated.reduce((s, e) => s + e.cost, 0) -
        (a.spendValue + a.estimated.reduce((s, e) => s + e.cost, 0)),
    )
  const priced = sorted.filter((row) => row.spendValue > 0 || row.estimated.length > 0)
  const zero = sorted.filter((row) => row.spendValue === 0 && row.estimated.length === 0)
  const shownZero = zero.slice(0, revealed)
  const hiddenCount = zero.length - shownZero.length
  const visibleRows = [...priced, ...shownZero]
  const staleness = stalenessBadge(report.rates_age_days)

  return (
    <Panel>
      <PanelHeader
        eyebrow="Rate table"
        title={`Prices per million tokens, as of ${rates.as_of}`}
        hint="Cache prices are the vendor's absolute figures when a row publishes them, otherwise derived from the input rate by the provider's rules. Cost is never stored."
        actions={
          staleness && (
            <Badge
              variant={staleness.level === 'info' ? 'secondary' : 'outline'}
              className={cn(staleness.level === 'caution' && 'border-warning text-warning')}
            >
              {staleness.text}
            </Badge>
          )
        }
      />
      <div className="scroll-thin overflow-x-auto">
        <Table>
          <TableHeader>
            <TableRow>
              {RATE_COLUMNS.map((column) => (
                <TableHead
                  key={column.label}
                  className={column.align === 'right' ? 'text-right' : 'text-left'}
                >
                  {column.label}
                </TableHead>
              ))}
            </TableRow>
          </TableHeader>
          <TableBody>
            {visibleRows.flatMap((row) => {
              const open = expanded.has(row.rate.match)
              const cells = [
                <TableRow key={row.rate.match} style={{ height: 'var(--row-height)' }}>
                  <ModelCell row={row} open={open} onToggle={() => toggle(row.rate.match)} />
                  <TableCell className="text-muted-foreground">
                    {providerLabel(row.rate.provider)}
                  </TableCell>
                  <TableCell className="tabular text-right">{row.input}</TableCell>
                  <CacheCell value={row.cacheRead} />
                  <CacheCell value={row.cacheWrite5m} />
                  <CacheCell value={row.cacheWrite1h} />
                  <TableCell className="tabular text-right">{row.output}</TableCell>
                  <TableCell className="tabular text-right text-muted-foreground">
                    {row.contextWindow ?? <Unavailable />}
                  </TableCell>
                  <TableCell className="text-right">
                    <div className="flex justify-end">
                      <StateCell state={row.state} />
                    </div>
                  </TableCell>
                  <TableCell
                    className={cn(
                      'tabular text-right font-medium',
                      row.state === 'unused' && 'font-normal text-muted-foreground',
                    )}
                  >
                    {row.spendLabel}
                  </TableCell>
                </TableRow>,
              ]
              if (open) {
                cells.push(
                  <TableRow key={`${row.rate.match}:detail`} className="bg-muted/20 hover:bg-muted/20">
                    <TableCell colSpan={RATE_COLUMNS.length}>
                      <RowDetail row={row} />
                    </TableCell>
                  </TableRow>,
                )
              }
              return cells
            })}
          </TableBody>
        </Table>
      </div>
      {hiddenCount > 0 && (
        <PanelBody>
          <Button
            variant="outline"
            size="sm"
            onClick={() => setRevealed((current) => current + REVEAL_BATCH)}
          >
            {`Show ${formatCount(Math.min(REVEAL_BATCH, hiddenCount))} more rates (${formatCount(hiddenCount)} hidden)`}
          </Button>
        </PanelBody>
      )}
    </Panel>
  )
}

function EstimatedPanel({ rates, report }: { rates: RateTable; report: Report }) {
  const items = estimatedModels(rates, report)
  if (items.length === 0) return null
  return (
    <Panel className="border-l-2 border-l-primary">
      <PanelHeader
        eyebrow="Estimated"
        title={`${plural(items.length, 'model')} ${items.length === 1 ? 'is' : 'are'} priced from a sibling row because ${items.length === 1 ? 'it has' : 'they have'} no row of their own`}
      />
      <PanelBody>
        {items.map((item) => (
          <div key={item.model} className="border-b py-1.5 last:border-b-0">
            <div className="flex flex-wrap items-baseline justify-between gap-3">
              <span className="tabular text-[11px]">
                {item.model}
                <span className="text-muted-foreground">{` priced as ${item.parentDisplay}`}</span>
              </span>
              <span className="tabular text-[11px] text-muted-foreground">
                {`${formatTokens(item.tokens)} tokens, ${formatMoney(item.cost)}`}
              </span>
            </div>
            <div className="text-[11px] text-muted-foreground">
              {`Fix: add a row with "match": "${item.model}" to rates.json to price it exactly.`}
            </div>
          </div>
        ))}
      </PanelBody>
    </Panel>
  )
}

function ProviderMultipliers({ providerId, rules }: { providerId: string; rules: ProviderRules }) {
  const items = [
    { label: 'Cache read', value: rules.cache_read },
    { label: 'Cache write, 5 min', value: rules.cache_write_5m },
    { label: 'Cache write, 1 hour', value: rules.cache_write_1h },
    { label: 'Batch tier', value: rules.batch },
  ]
  const max = Math.max(...items.map((item) => item.value), 1)

  return (
    <div className="border-b py-2 last:border-b-0">
      <StatLabel className="mb-1.5">{providerLabel(providerId)}</StatLabel>
      {items.map((item) => (
        <MeterRow
          key={item.label}
          label={item.label}
          value={`${item.value}x`}
          fraction={item.value / max}
          labelWidth={140}
        />
      ))}
    </div>
  )
}

function MultipliersPanel({ rates, report }: { rates: RateTable; report: Report }) {
  const providersPresent = report.by_provider.filter((bucket) => bucket.cost.total > 0)

  return (
    <Panel>
      <PanelHeader
        eyebrow="Multipliers"
        title="Every bucket priced off the base input rate, per provider"
      />
      <PanelBody>
        {providersPresent.length === 0 ? (
          <EmptyState title="No priced activity in this slice yet." />
        ) : (
          providersPresent.map((bucket) => {
            const rules = rates.providers[bucket.key]
            return rules ? <ProviderMultipliers key={bucket.key} providerId={bucket.key} rules={rules} /> : null
          })
        )}
      </PanelBody>
      <PanelNote>
        These rules differ by provider. A discount that holds for one vendor is not universal, so
        each is shown on its own rather than as one shared list. Individual models may publish
        exact cache prices that override these ratios.
      </PanelNote>
    </Panel>
  )
}

function UnpricedBadge({ entry }: { entry: UnpricedModelEntry }) {
  return (
    <Badge variant="outline" className="text-[10px]">
      {entry.status === 'no_list_price' ? 'No list price' : 'Watchlist'}
    </Badge>
  )
}

export function splitUnpriced(
  models: Report['unknown_models'],
  entries: UnpricedModelEntry[],
): {
  listed: { model: Report['unknown_models'][number]; entry: UnpricedModelEntry }[]
  unknown: Report['unknown_models']
  idle: UnpricedModelEntry[]
} {
  const listed: { model: Report['unknown_models'][number]; entry: UnpricedModelEntry }[] = []
  const unknown: Report['unknown_models'] = []
  const used = new Set<string>()
  for (const model of models) {
    const entry = matchUnpriced(model.model, entries)
    if (entry) {
      listed.push({ model, entry })
      used.add(entry.match)
    } else {
      unknown.push(model)
    }
  }
  return { listed, unknown, idle: entries.filter((entry) => !used.has(entry.match)) }
}

function UnpricedPanel({ rates, report }: { rates: RateTable; report: Report }) {
  const { listed, unknown, idle } = splitUnpriced(report.unknown_models, rates.unpriced_models)
  if (listed.length === 0 && unknown.length === 0 && idle.length === 0) return null

  const first = unknown[0]
  const snippet = first
    ? `{"match": "${first.model}", "provider": "...", "display": "...", "input": 0, "output": 0, "context_window": 0, "source": "https://...", "verified": "${rates.as_of}", "status": "ga"}`
    : ''
  const withSpend = listed.length + unknown.length

  return (
    <Panel className="border-l-2 border-l-primary">
      <PanelHeader
        eyebrow="Unpriced"
        title={
          withSpend > 0
            ? `${plural(withSpend, 'model')} with tokens and no rate`
            : 'Known models without a price'
        }
      />
      <PanelBody className="space-y-3">
        {withSpend > 0 && (
          <div>
            {listed.map(({ model, entry }) => (
              <div key={model.model} className="border-b py-1.5 last:border-b-0">
                <div className="flex items-baseline justify-between gap-3">
                  <span className="tabular flex items-center gap-1.5 text-[11px]">
                    {model.model}
                    <UnpricedBadge entry={entry} />
                  </span>
                  <span className="tabular text-[11px] text-muted-foreground">
                    {`${formatTokens(model.tokens)} tokens, ${formatCount(model.events)} events`}
                  </span>
                </div>
                <div className="text-[11px] text-muted-foreground">{entry.note}</div>
              </div>
            ))}
            {unknown.map((model) => (
              <div
                key={model.model}
                className="flex items-baseline justify-between gap-3 border-b py-1.5 last:border-b-0"
              >
                <span className="tabular text-[11px]">{model.model}</span>
                <span className="tabular text-[11px] text-muted-foreground">
                  {`${formatTokens(model.tokens)} tokens, ${formatCount(model.events)} events`}
                </span>
              </div>
            ))}
          </div>
        )}
        {unknown.length > 0 && (
          <>
            <p className="text-xs leading-relaxed text-muted-foreground">
              Tokens are counted and shown, cost stays out of the totals until a rate exists. Add one
              line to rates.json and history reprices.
            </p>
            <CodeBlock>{snippet}</CodeBlock>
          </>
        )}
        {idle.length > 0 && (
          <div className="space-y-1">
            {withSpend > 0 && <StatLabel>Known without a price</StatLabel>}
            {idle.map((entry) => (
              <div key={entry.match} className="border-b py-1.5 last:border-b-0">
                <span className="tabular flex items-center gap-1.5 text-[11px]">
                  {entry.match}
                  <UnpricedBadge entry={entry} />
                </span>
                <div className="text-[11px] text-muted-foreground">{entry.note}</div>
              </div>
            ))}
          </div>
        )}
      </PanelBody>
    </Panel>
  )
}

export default function Pricing(props: { report: Report; rates: RateTable }): JSX.Element {
  const { report, rates } = props

  return (
    <div className="flex flex-col gap-3">
      <EstimatedPanel rates={rates} report={report} />
      <RateTablePanel rates={rates} report={report} />
      <div className="grid grid-cols-1 gap-3 xl:grid-cols-2">
        <MultipliersPanel rates={rates} report={report} />
        <UnpricedPanel rates={rates} report={report} />
      </div>
    </div>
  )
}
