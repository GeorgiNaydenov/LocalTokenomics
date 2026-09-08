import { useState } from 'react'
import type { JSX, ReactNode } from 'react'
import type { EconRow, Provenance, TokenUsage } from './api'
import type { EconomicsTabProps } from './SessionWorkspace'
import { formatCount, formatDuration, formatExact, formatMoney, formatPercent, formatTokens } from './format'
import { Panel, PanelBody, PanelHeader, PanelNote } from '@/components/panel'
import { CostStateBadge, ProvenanceBadge, Unavailable } from '@/components/status'
import { EmptyState } from '@/components/states'
import { Stat, StatGrid, StatLabel } from '@/components/stat'
import { useMediaQuery } from '@/components/use-media-query'
import { Button } from '@/components/ui/button'
import { Tooltip, TooltipContent, TooltipTrigger } from '@/components/ui/tooltip'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { cn } from '@/design-system/cn'

const REVEAL_BATCH = 40

const DURATION_NOTE: Record<Provenance, string> = {
  measured: 'The log records a start and an end for this work.',
  derived: 'Wall-clock gap between log records. The API never reports its own latency here.',
  estimated: 'Estimated from a table, not from this log.',
  inferred: 'Inferred from the model id, not from this log.',
  unavailable: 'This client logs no timing for these spans.',
}

function DurationCell({ row }: { row: EconRow }) {
  if (row.duration_ms === null) {
    return <Unavailable hint={DURATION_NOTE[row.duration_provenance]} />
  }
  return (
    <span className="inline-flex flex-wrap items-center justify-end gap-1.5">
      <span className="tabular">{formatDuration(row.duration_ms)}</span>
      <ProvenanceBadge
        group="time"
        provenance={row.duration_provenance}
        title={DURATION_NOTE[row.duration_provenance]}
      />
    </span>
  )
}

function CostCell({ row }: { row: EconRow }) {
  const partial = row.cost !== null && row.cost_state !== 'priced' && row.cost_state !== 'free'
  return (
    <span className="inline-flex flex-wrap items-center justify-end gap-1.5">
      {row.cost === null ? (
        <Unavailable className="whitespace-normal" hint="No model call in this row carried a priced token count." />
      ) : (
        <span className="tabular text-foreground">{formatMoney(row.cost.total)}</span>
      )}
      {partial && (
        <Tooltip>
          <TooltipTrigger asChild>
            <span tabIndex={0} className="cursor-default rounded-sm text-[10px] text-muted-foreground outline-offset-2">
              partial
            </span>
          </TooltipTrigger>
          <TooltipContent className="max-w-64">
            Only the priced model calls in this row are in that figure.
          </TooltipContent>
        </Tooltip>
      )}
      <CostStateBadge state={row.cost_state} />
    </span>
  )
}

function hasTokens(row: EconRow): row is EconRow & { tokens: TokenUsage } {
  if (row.model_calls === 0 || row.tokens === null) return false
  return row.tokens.total > 0 || row.cost_state !== 'unavailable'
}

function TokensCell({ row }: { row: EconRow }) {
  if (!hasTokens(row)) {
    return <Unavailable hint="No model call in this row logged a token count, so this is an absence rather than a zero." />
  }
  return (
    <Tooltip>
      <TooltipTrigger asChild>
        <span tabIndex={0} className="tabular cursor-default rounded-sm outline-offset-2">
          {formatTokens(row.tokens.total)}
        </span>
      </TooltipTrigger>
      <TooltipContent>
        <span className="tabular">{formatExact(row.tokens.total)}</span>
      </TooltipContent>
    </Tooltip>
  )
}

function RetriesCell({ row }: { row: EconRow }) {
  if (row.retries === null) {
    return (
      <Unavailable
        className="whitespace-normal"
        hint="This client does not log retry attempts, so this is not a zero."
      />
    )
  }
  return <span className="tabular">{formatCount(row.retries)}</span>
}

function AmplificationCell({ row }: { row: EconRow }) {
  if (row.amplification === null) {
    return <Unavailable className="whitespace-normal" hint="Needs model calls with both input and output tokens." />
  }
  return <span className="tabular">{`${row.amplification.toFixed(1)}x`}</span>
}

function CacheCell({ row }: { row: EconRow }) {
  if (row.cache_hit_ratio === null) {
    return <Unavailable className="whitespace-normal" hint="No input tokens counted for this row." />
  }
  return <span className="tabular">{formatPercent(row.cache_hit_ratio)}</span>
}

interface Column {
  key: string
  label: string
  align: 'left' | 'right'
  cell: (row: EconRow) => ReactNode
}

function labelColumn(label: string): Column {
  return {
    key: 'label',
    label,
    align: 'left',
    cell: (row) => (
      <Tooltip>
        <TooltipTrigger asChild>
          <span
            tabIndex={0}
            className="tabular inline-block max-w-56 cursor-default truncate rounded-sm align-bottom text-foreground outline-offset-2"
          >
            {row.label}
          </span>
        </TooltipTrigger>
        <TooltipContent>
          <span className="tabular">{row.key}</span>
        </TooltipContent>
      </Tooltip>
    ),
  }
}

const COUNT_COLUMNS: Column[] = [
  { key: 'model_calls', label: 'Model calls', align: 'right', cell: (row) => <span className="tabular">{formatCount(row.model_calls)}</span> },
  { key: 'tool_calls', label: 'Tool calls', align: 'right', cell: (row) => <span className="tabular">{formatCount(row.tool_calls)}</span> },
]

const ERROR_COLUMN: Column = {
  key: 'errors',
  label: 'Errors',
  align: 'right',
  cell: (row) => (
    <span className={cn('tabular', row.errors > 0 ? 'text-destructive' : 'text-muted-foreground')}>
      {formatCount(row.errors)}
    </span>
  ),
}

const DURATION_COLUMN: Column = { key: 'duration', label: 'Duration', align: 'right', cell: (row) => <DurationCell row={row} /> }
const TOKENS_COLUMN: Column = { key: 'tokens', label: 'Tokens', align: 'right', cell: (row) => <TokensCell row={row} /> }
const COST_COLUMN: Column = { key: 'cost', label: 'Cost', align: 'right', cell: (row) => <CostCell row={row} /> }

const TURN_COLUMNS: Column[] = [
  labelColumn('Turn'),
  ...COUNT_COLUMNS,
  TOKENS_COLUMN,
  COST_COLUMN,
  DURATION_COLUMN,
  ERROR_COLUMN,
  { key: 'retries', label: 'Retries', align: 'right', cell: (row) => <RetriesCell row={row} /> },
]

const MODEL_COLUMNS: Column[] = [
  labelColumn('Model'),
  COUNT_COLUMNS[0],
  TOKENS_COLUMN,
  COST_COLUMN,
  DURATION_COLUMN,
  { key: 'cache', label: 'Cache hit', align: 'right', cell: (row) => <CacheCell row={row} /> },
  { key: 'amplification', label: 'Amplification', align: 'right', cell: (row) => <AmplificationCell row={row} /> },
  {
    key: 'rate',
    label: 'Tokens/s',
    align: 'right',
    cell: (row) =>
      row.tokens_per_second === null ? (
        <Unavailable hint="Needs measured tokens and a measured duration on the same call. No source logs both today." />
      ) : (
        <span className="tabular">{row.tokens_per_second.toFixed(1)}</span>
      ),
  },
]

const TOOL_COLUMNS: Column[] = [
  labelColumn('Tool'),
  COUNT_COLUMNS[1],
  DURATION_COLUMN,
  ERROR_COLUMN,
]

function EconCard({ row, columns }: { row: EconRow; columns: Column[] }) {
  const [first, ...rest] = columns
  return (
    <div className="space-y-2 rounded-md border bg-card p-3">
      <div>{first.cell(row)}</div>
      {rest.map((column) => (
        <div key={column.key} className="flex items-center justify-between gap-2.5 text-xs">
          <StatLabel>{column.label}</StatLabel>
          <span className="text-right text-muted-foreground">{column.cell(row)}</span>
        </div>
      ))}
    </div>
  )
}

function EconPanel(props: {
  eyebrow: string
  title: string
  note: string
  columns: Column[]
  rows: EconRow[]
  empty: string
  isPhone: boolean
}) {
  const [revealed, setRevealed] = useState(REVEAL_BATCH)
  const shown = props.rows.slice(0, revealed)
  const hidden = props.rows.length - shown.length

  return (
    <Panel>
      <PanelHeader eyebrow={props.eyebrow} title={props.title} />
      {props.rows.length === 0 ? (
        <PanelBody>
          <EmptyState title={props.empty} />
        </PanelBody>
      ) : props.isPhone ? (
        <PanelBody className="space-y-2">
          {shown.map((row) => (
            <EconCard key={row.key} row={row} columns={props.columns} />
          ))}
        </PanelBody>
      ) : (
        <div className="scroll-thin overflow-x-auto">
          <Table>
            <TableHeader>
              <TableRow>
                {props.columns.map((column) => (
                  <TableHead
                    key={column.key}
                    className={cn('whitespace-nowrap', column.align === 'right' && 'text-right')}
                  >
                    {column.label}
                  </TableHead>
                ))}
              </TableRow>
            </TableHeader>
            <TableBody>
              {shown.map((row) => (
                <TableRow key={row.key} style={{ height: 'var(--row-height)' }}>
                  {props.columns.map((column) => (
                    <TableCell
                      key={column.key}
                      className={cn(
                        'whitespace-nowrap text-muted-foreground',
                        column.align === 'right' && 'text-right',
                      )}
                    >
                      {column.cell(row)}
                    </TableCell>
                  ))}
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      )}
      {hidden > 0 && (
        <PanelBody>
          <Button variant="outline" size="sm" onClick={() => setRevealed(revealed + REVEAL_BATCH)}>
            {`Show ${Math.min(REVEAL_BATCH, hidden)} more (${formatCount(hidden)} hidden)`}
          </Button>
        </PanelBody>
      )}
      <PanelNote>{props.note}</PanelNote>
    </Panel>
  )
}

function retryFoot(source: string): string {
  if (source === 'claude-code') return 'Retry attempts and api_error records, when the log carries them.'
  return `${source} writes no retry field, so this is absent rather than zero.`
}

export default function EconomicsTab(props: EconomicsTabProps): JSX.Element {
  const isPhone = useMediaQuery('(max-width: 639px)')
  const totals = props.economics.totals

  return (
    <div className="flex flex-col gap-3">
      <StatGrid className="xl:grid-cols-2">
        <Stat
          label="Tokens"
          value={<TokensCell row={totals} />}
          hint={
            hasTokens(totals)
              ? `${formatTokens(totals.tokens.input_total)} in, ${formatTokens(totals.tokens.output)} out across ${formatCount(totals.model_calls)} model calls.`
              : `This client logs no token counts. Its ${formatCount(totals.model_calls)} model calls are real; their tokens are not recorded.`
          }
        />
        <Stat
          label="Cost"
          value={
            totals.cost === null ? (
              <Unavailable className="whitespace-normal" hint="No priced model call in this session." />
            ) : (
              formatMoney(totals.cost.total)
            )
          }
          hint={`List prices from the rate table. State is ${totals.cost_state}, the worst of this session's model calls.`}
        />
        <Stat
          label="Duration"
          value={<DurationCell row={totals} />}
          hint="Summed over the session's turns, not wall clock between the first and last record."
        />
        <Stat
          label="Calls"
          value={<span className="tabular">{formatCount(totals.model_calls + totals.tool_calls)}</span>}
          hint={`${formatCount(totals.model_calls)} model, ${formatCount(totals.tool_calls)} tool, ${formatCount(totals.errors)} errored.`}
        />
        <Stat label="Retries" value={<RetriesCell row={totals} />} hint={retryFoot(props.source)} />
        <Stat
          label="Amplification"
          value={<AmplificationCell row={totals} />}
          hint="Input tokens read per output token produced."
        />
        <Stat
          label="Cache hit ratio"
          value={<CacheCell row={totals} />}
          hint="Share of input tokens served from the prompt cache."
        />
        <Stat
          label="Tokens per second"
          value={
            totals.tokens_per_second === null ? (
              <Unavailable
                className="whitespace-normal"
                hint="Needs measured tokens and a measured duration on the same call."
              />
            ) : (
              <span className="tabular">{totals.tokens_per_second.toFixed(1)}</span>
            )
          }
          hint="Only measured tokens over a measured duration count. No client here logs both on one call, so it stays blank."
        />
      </StatGrid>

      {hasTokens(totals) && (
        <p className="text-xs leading-relaxed text-muted-foreground">
          {totals.tokens.reasoning_output > 0
            ? `Reasoning: ${formatTokens(totals.tokens.reasoning_output)}, already inside the ${formatTokens(totals.tokens.output)} output above, never a fifth bucket.`
            : 'No reasoning tokens are logged for this session. When they are, they sit inside output, not beside it.'}
        </p>
      )}

      <EconPanel
        eyebrow="Per turn"
        title={`${formatCount(props.economics.by_turn.length)} turns, in the order they ran`}
        note="A turn is one prompt and everything it caused. Cost is the sum of its priced model calls; a row marked partial has model calls that no rate matched. The state badge on a row is the worst cost state among its model calls."
        columns={TURN_COLUMNS}
        rows={props.economics.by_turn}
        empty="No turns carry spans for this session."
        isPhone={isPhone}
      />

      <EconPanel
        eyebrow="Per model"
        title={`${formatCount(props.economics.by_model.length)} models, heaviest first`}
        note="Sorted by tokens. A model with no rate entry still shows its tokens; its cost stays out."
        columns={MODEL_COLUMNS}
        rows={props.economics.by_model}
        empty="No model call in this session carried a model id."
        isPhone={isPhone}
      />

      <EconPanel
        eyebrow="Per tool"
        title={`${formatCount(props.economics.by_tool.length)} tools, most called first`}
        note="Tools carry no tokens of their own, so this table counts calls, time and errors only. Their cost lands on the model call that read the result."
        columns={TOOL_COLUMNS}
        rows={props.economics.by_tool}
        empty="No tool calls in this session."
        isPhone={isPhone}
      />
    </div>
  )
}
