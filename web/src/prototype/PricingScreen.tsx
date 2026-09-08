import { useState } from 'react'

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
import { CodeBlock } from '@/components/detail'
import { Panel, PanelBody, PanelHeader, PanelNote } from '@/components/panel'
import { MeterRow } from '@/components/status'
import { StatLabel } from '@/components/stat'
import { formatCount, formatMoney, formatTokens } from '@/format'
import { PROVIDER_RULES, RATES, TOTALS, UNKNOWN_MODELS, type RateRow } from './data'

const REVEAL_BATCH = 4

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

function derived(rate: RateRow) {
  const rules = PROVIDER_RULES[rate.provider]
  const free = rate.input === 0 && rate.output === 0
  return {
    free,
    input: free ? 'free' : `$${rate.input.toFixed(2)}`,
    output: free ? 'free' : `$${rate.output.toFixed(2)}`,
    cacheRead: free ? 'free' : `$${(rate.input * (rules?.cache_read ?? 0.1)).toFixed(3)}`,
    cacheWrite: free ? 'free' : `$${(rate.input * (rules?.cache_write_5m ?? 1.25)).toFixed(3)}`,
    state: free ? 'free' : rate.spend > 0 ? 'priced' : 'unused',
  }
}

function RateTablePanel() {
  const [revealed, setRevealed] = useState(0)

  const sorted = [...RATES].sort((a, b) => b.spend - a.spend)
  const priced = sorted.filter((rate) => rate.spend > 0)
  const zero = sorted.filter((rate) => rate.spend === 0)
  const shown = [...priced, ...zero.slice(0, revealed)]
  const hidden = zero.length - Math.min(revealed, zero.length)

  return (
    <Panel>
      <PanelHeader
        eyebrow="Rate table"
        title={`Prices per million tokens, as of ${TOTALS.ratesAsOf}`}
        hint="Cache prices are derived from the input rate by each provider's own rules. Cost is never stored."
      />
      <div className="scroll-thin overflow-x-auto">
        <Table>
          <TableHeader>
            <TableRow>
              {RATE_COLUMNS.map((column) => (
                <TableHead
                  key={column.label}
                  className={column.align === 'right' ? 'text-right' : undefined}
                >
                  {column.label}
                </TableHead>
              ))}
            </TableRow>
          </TableHeader>
          <TableBody>
            {shown.map((rate) => {
              const values = derived(rate)
              return (
                <TableRow key={rate.match} style={{ height: 'var(--row-height)' }}>
                  <TableCell>
                    <div className="flex items-center gap-2">
                      {rate.display}
                      {rate.inherited ? (
                        <Badge variant="outline" className="text-[10px]">
                          inherited
                        </Badge>
                      ) : null}
                    </div>
                    <div className="tabular text-[11px] text-muted-foreground">{rate.match}</div>
                  </TableCell>
                  <TableCell className="text-muted-foreground">{rate.provider}</TableCell>
                  <TableCell className="tabular text-right">{values.input}</TableCell>
                  <TableCell className="tabular text-right text-muted-foreground">
                    {values.cacheRead}
                  </TableCell>
                  <TableCell className="tabular text-right text-muted-foreground">
                    {values.cacheWrite}
                  </TableCell>
                  <TableCell className="tabular text-right">{values.output}</TableCell>
                  <TableCell className="text-right">
                    <Badge variant={values.state === 'priced' ? 'default' : 'outline'}>
                      {values.state}
                    </Badge>
                  </TableCell>
                  <TableCell className="tabular text-right font-medium">
                    {formatMoney(rate.spend)}
                  </TableCell>
                </TableRow>
              )
            })}
          </TableBody>
        </Table>
      </div>
      {hidden > 0 ? (
        <PanelBody>
          <Button
            variant="outline"
            size="sm"
            onClick={() => setRevealed((current) => current + REVEAL_BATCH)}
          >
            Show {Math.min(REVEAL_BATCH, hidden)} more rates ({hidden} hidden)
          </Button>
        </PanelBody>
      ) : null}
    </Panel>
  )
}

function MultipliersPanel() {
  const entries = Object.entries(PROVIDER_RULES)

  return (
    <Panel>
      <PanelHeader
        eyebrow="Multipliers"
        title="Every bucket priced off the base input rate, per provider"
      />
      <PanelBody className="space-y-5">
        {entries.map(([provider, rules]) => {
          const items = [
            { label: 'Cache read', value: rules.cache_read },
            { label: 'Cache write, 5 min', value: rules.cache_write_5m },
            { label: 'Cache write, 1 hour', value: rules.cache_write_1h },
            { label: 'Batch tier', value: rules.batch },
          ]
          const peak = Math.max(...items.map((item) => item.value), 1)
          return (
            <div key={provider} className="space-y-1">
              <StatLabel>{provider}</StatLabel>
              {items.map((item) => (
                <MeterRow
                  key={item.label}
                  label={item.label}
                  value={`${item.value}x`}
                  fraction={item.value / peak}
                  labelWidth={140}
                />
              ))}
            </div>
          )
        })}
      </PanelBody>
      <PanelNote>
        These rules differ by provider &mdash; a discount that holds for one vendor is not
        universal, so each is shown on its own rather than as one shared list.
      </PanelNote>
    </Panel>
  )
}

function UnpricedPanel() {
  if (UNKNOWN_MODELS.length === 0) return null
  const first = UNKNOWN_MODELS[0]

  return (
    <Panel className="border-l-2 border-l-primary">
      <PanelHeader
        eyebrow="Unpriced"
        title={`${formatCount(UNKNOWN_MODELS.length)} model with tokens and no rate`}
      />
      <PanelBody className="space-y-4">
        <div>
          {UNKNOWN_MODELS.map((model) => (
            <div
              key={model.model}
              className="flex items-baseline justify-between gap-3 border-b py-2 last:border-b-0"
            >
              <span className="tabular text-[13px]">{model.model}</span>
              <span className="tabular text-xs text-muted-foreground">
                {formatTokens(model.tokens)} tokens &middot; {formatCount(model.events)} events
              </span>
            </div>
          ))}
        </div>
        <p className="text-xs leading-relaxed text-muted-foreground">
          Tokens are counted and shown, cost stays out of the totals until a rate exists. Add one
          line to rates.json and history reprices.
        </p>
        <CodeBlock>
          {`{"match": "${first.model}", "provider": "...", "display": "...", "input": 0, "output": 0}`}
        </CodeBlock>
      </PanelBody>
    </Panel>
  )
}

export function PricingScreen() {
  return (
    <div className="flex flex-col gap-3">
      <RateTablePanel />
      <div className="grid grid-cols-1 gap-3 xl:grid-cols-2">
        <MultipliersPanel />
        <UnpricedPanel />
      </div>
    </div>
  )
}
