import { useState } from 'react'
import type { JSX, ReactNode } from 'react'
import type { ModelRate, ProviderRules, RateTable, Report } from './api'
import { formatCount, formatMoney, formatTokens } from './format'
import { Panel, PanelBody, PanelHeader, PanelNote } from '@/components/panel'
import { CostStateBadge, MeterRow, Unavailable } from '@/components/status'
import { CodeBlock } from '@/components/detail'
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

const DEFAULT_RULES: ProviderRules = { cache_read: 0.1, cache_write_5m: 1.25, cache_write_1h: 2.0, batch: 0.5, free: false }
const REVEAL_BATCH = 20

const RATE_COLUMNS: { label: string; align: 'left' | 'right' }[] = [
  { label: 'Model', align: 'left' },
  { label: 'Provider', align: 'left' },
  { label: 'Input', align: 'right' },
  { label: 'Cache read', align: 'right' },
  { label: 'Cache write 5m', align: 'right' },
  { label: 'Output', align: 'right' },
  { label: 'State', align: 'right' },
  { label: 'Spend here', align: 'right' },
]

type RateState = 'free' | 'priced' | 'unused'

interface RateRow {
  rate: ModelRate
  input: string
  output: string
  cacheRead: string
  cacheWrite5m: string
  spendValue: number
  spendLabel: ReactNode
  state: RateState
}

function effectiveRules(rate: ModelRate, rates: RateTable): ProviderRules {
  return rate.cache_rules ?? rates.providers[rate.provider] ?? DEFAULT_RULES
}

function buildRow(rate: ModelRate, rates: RateTable, report: Report): RateRow {
  const providerRules = rates.providers[rate.provider]
  const isFree = providerRules?.free === true
  const rules = effectiveRules(rate, rates)
  const bucket = report.by_model.find((b) => b.label === rate.display)
  const spendValue = bucket ? bucket.cost.total : 0
  const state: RateState = isFree ? 'free' : spendValue > 0 ? 'priced' : 'unused'

  return {
    rate,
    input: isFree ? 'free' : `$${rate.input.toFixed(2)}`,
    output: isFree ? 'free' : `$${rate.output.toFixed(2)}`,
    cacheRead: isFree ? 'free' : `$${(rate.input * rules.cache_read).toFixed(3)}`,
    cacheWrite5m: isFree ? 'free' : `$${(rate.input * rules.cache_write_5m).toFixed(3)}`,
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

function RateTablePanel({ rates, report }: { rates: RateTable; report: Report }) {
  const [revealed, setRevealed] = useState(0)

  const sorted = rates.models.map((rate) => buildRow(rate, rates, report)).sort((a, b) => b.spendValue - a.spendValue)
  const priced = sorted.filter((row) => row.spendValue > 0)
  const zero = sorted.filter((row) => row.spendValue === 0)
  const shownZero = zero.slice(0, revealed)
  const hiddenCount = zero.length - shownZero.length
  const visibleRows = [...priced, ...shownZero]

  return (
    <Panel>
      <PanelHeader
        eyebrow="Rate table"
        title={`Prices per million tokens, as of ${rates.as_of}`}
        hint="Cache prices are derived from the input rate by each provider's own rules. Cost is never stored."
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
            {visibleRows.map((row) => (
              <TableRow key={row.rate.match} style={{ height: 'var(--row-height)' }}>
                <TableCell>
                  <div className="flex items-center gap-2">
                    {row.rate.display}
                    {row.rate.inherited && (
                      <Badge variant="outline" className="text-[10px]">
                        inherited
                      </Badge>
                    )}
                  </div>
                  <div className="tabular text-[10px] text-muted-foreground">{row.rate.match}</div>
                </TableCell>
                <TableCell className="text-muted-foreground">{row.rate.provider}</TableCell>
                <TableCell className="tabular text-right">{row.input}</TableCell>
                <TableCell className="tabular text-right text-muted-foreground">
                  {row.cacheRead}
                </TableCell>
                <TableCell className="tabular text-right text-muted-foreground">
                  {row.cacheWrite5m}
                </TableCell>
                <TableCell className="tabular text-right">{row.output}</TableCell>
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
              </TableRow>
            ))}
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
            {`Show ${Math.min(REVEAL_BATCH, hiddenCount)} more rates (${hiddenCount} hidden)`}
          </Button>
        </PanelBody>
      )}
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
  const providerLabel = providerId.charAt(0).toUpperCase() + providerId.slice(1)

  return (
    <div className="border-b py-2 last:border-b-0">
      <StatLabel className="mb-1.5">{providerLabel}</StatLabel>
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
        each is shown on its own rather than as one shared list.
      </PanelNote>
    </Panel>
  )
}

function UnpricedPanel({ report }: { report: Report }) {
  const models = report.unknown_models
  if (models.length === 0) return null

  const first = models[0]
  const snippet = `{"match": "${first.model}", "provider": "...", "display": "...", "input": 0, "output": 0}`

  return (
    <Panel className="border-l-2 border-l-primary">
      <PanelHeader
        eyebrow="Unpriced"
        title={`${formatCount(models.length)} model with tokens and no rate`}
      />
      <PanelBody className="space-y-3">
        <div>
          {models.map((model) => (
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
        <p className="text-xs leading-relaxed text-muted-foreground">
          Tokens are counted and shown, cost stays out of the totals until a rate exists. Add one
          line to rates.json and history reprices.
        </p>
        <CodeBlock>{snippet}</CodeBlock>
      </PanelBody>
    </Panel>
  )
}

export default function Pricing(props: { report: Report; rates: RateTable }): JSX.Element {
  const { report, rates } = props

  return (
    <div className="flex flex-col gap-3">
      <RateTablePanel rates={rates} report={report} />
      <div className="grid grid-cols-1 gap-3 xl:grid-cols-2">
        <MultipliersPanel rates={rates} report={report} />
        <UnpricedPanel report={report} />
      </div>
    </div>
  )
}
