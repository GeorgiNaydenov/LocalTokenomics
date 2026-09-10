import { useMemo, useState } from 'react'
import type { JSX } from 'react'
import type { Report, SessionRow } from './api'
import {
  formatClock,
  formatCount,
  formatDayShort,
  formatMoney,
  formatTokens,
  sessionDisplayName,
  toDayString,
} from './format'
import { Panel, PanelHeader, PanelNote } from '@/components/panel'
import { CostStateBadge, OutcomeBadge, Unavailable } from '@/components/status'
import { ErrorCount, SessionCard, TokenCell, TracedDot } from '@/components/session'
import { SortSelect } from '@/components/filters'
import { EmptyState, SortButton, ariaSort } from '@/components/states'
import { useMediaQuery } from '@/components/use-media-query'
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
import type { Column } from '@/components/columns'
import { ColumnChooser, useHiddenColumns, visibleColumns } from '@/components/columns'

type SortKey =
  | 'state'
  | 'outcome'
  | 'id'
  | 'client'
  | 'model'
  | 'project'
  | 'start'
  | 'requests'
  | 'errors'
  | 'tokens'
  | 'cost'
type SortDir = 'asc' | 'desc'

const SHOWN_LIMIT = 120

const SORT_OPTIONS: { value: string; key: SortKey; dir: SortDir; label: string }[] = [
  { value: 'cost:desc', key: 'cost', dir: 'desc', label: 'Cost, high to low' },
  { value: 'cost:asc', key: 'cost', dir: 'asc', label: 'Cost, low to high' },
  { value: 'tokens:desc', key: 'tokens', dir: 'desc', label: 'Tokens, high to low' },
  { value: 'start:desc', key: 'start', dir: 'desc', label: 'Newest first' },
  { value: 'start:asc', key: 'start', dir: 'asc', label: 'Oldest first' },
  { value: 'requests:desc', key: 'requests', dir: 'desc', label: 'Most requests' },
  { value: 'errors:desc', key: 'errors', dir: 'desc', label: 'Most errors' },
  { value: 'state:asc', key: 'state', dir: 'asc', label: 'Cost state' },
  { value: 'outcome:asc', key: 'outcome', dir: 'asc', label: 'Outcome A to Z' },
  { value: 'project:asc', key: 'project', dir: 'asc', label: 'Project A to Z' },
]

function modelLabel(modelId: string, report: Report): string {
  return report.by_model.find((bucket) => bucket.key === modelId)?.label ?? modelId
}

function startLabel(startTime: string): string {
  return `${formatDayShort(toDayString(startTime) ?? startTime)} ${formatClock(startTime)}`
}

function sortValue(row: SessionRow, key: SortKey, report: Report): string | number {
  switch (key) {
    case 'state':
      return row.cost_state
    case 'outcome':
      return row.outcome
    case 'errors':
      return row.error_count
    case 'id':
      return row.session_id
    case 'client':
      return row.client
    case 'model':
      return modelLabel(row.models[0], report)
    case 'project':
      return row.project ?? ''
    case 'start':
      return row.start_time
    case 'requests':
      return row.request_count
    case 'tokens':
      return row.tokens ? row.tokens.total : -1
    case 'cost':
      return row.cost ? row.cost.total : -1
  }
}

function compare(a: string | number, b: string | number): number {
  if (typeof a === 'string' || typeof b === 'string') return String(a).localeCompare(String(b))
  return a - b
}

function ModelCell({ row, report }: { row: SessionRow; report: Report }) {
  const extra = row.models.length - 1
  return (
    <Tooltip>
      <TooltipTrigger asChild>
        <span
          tabIndex={0}
          className="inline-flex cursor-default items-center gap-2 rounded-sm outline-offset-2"
        >
          {modelLabel(row.models[0], report)}
          {extra > 0 ? <span className="tabular text-[11px]">+{extra}</span> : null}
        </span>
      </TooltipTrigger>
      <TooltipContent>{row.models.join(', ')}</TooltipContent>
    </Tooltip>
  )
}

function buildSessionColumns(report: Report, maxTokens: number): Column<SessionRow>[] {
  return [
    {
      key: 'state',
      label: 'State',
      align: 'left',
      cell: (row) => (
        <span className="inline-flex items-center gap-2">
          <CostStateBadge state={row.cost_state} />
          <TracedDot traced={row.traced} />
        </span>
      ),
    },
    {
      key: 'outcome',
      label: 'Outcome',
      align: 'left',
      cell: (row) => <OutcomeBadge outcome={row.outcome} />,
    },
    {
      key: 'id',
      label: 'Session',
      align: 'left',
      cellClassName: 'tabular max-w-40 font-medium',
      cell: (row) => (
        <Tooltip>
          <TooltipTrigger asChild>
            <span tabIndex={0} className="block cursor-default truncate rounded-sm outline-offset-2">
              {sessionDisplayName(row)}
            </span>
          </TooltipTrigger>
          <TooltipContent>
            <span className="tabular">{sessionDisplayName(row)}</span>
          </TooltipContent>
        </Tooltip>
      ),
    },
    {
      key: 'client',
      label: 'Client',
      align: 'left',
      cellClassName: 'text-muted-foreground',
      cell: (row) => row.client,
    },
    {
      key: 'model',
      label: 'Model',
      align: 'left',
      cellClassName: 'text-muted-foreground',
      cell: (row) => <ModelCell row={row} report={report} />,
    },
    {
      key: 'project',
      label: 'Project',
      align: 'left',
      cellClassName: 'max-w-36 text-muted-foreground',
      cell: (row) => <span className="block truncate">{row.project ?? '(no project)'}</span>,
    },
    {
      key: 'start',
      label: 'Started',
      align: 'left',
      cellClassName: 'tabular text-muted-foreground',
      cell: (row) => startLabel(row.start_time),
    },
    {
      key: 'requests',
      label: 'Req',
      align: 'right',
      cellClassName: 'tabular text-muted-foreground',
      cell: (row) => formatCount(row.request_count),
    },
    {
      key: 'errors',
      label: 'Errors',
      align: 'right',
      cell: (row) => <ErrorCount count={row.error_count} />,
    },
    {
      key: 'tokens',
      label: 'Tokens',
      align: 'right',
      cell: (row) => (
        <TokenCell
          label={row.tokens ? formatTokens(row.tokens.total) : null}
          fraction={row.tokens ? row.tokens.total / maxTokens : 0}
          state={row.cost_state}
        />
      ),
    },
    {
      key: 'cost',
      label: 'Cost',
      align: 'right',
      cellClassName: 'tabular font-semibold',
      cell: (row) =>
        row.cost ? (
          formatMoney(row.cost.total)
        ) : (
          <span className="font-normal text-muted-foreground">
            <Unavailable />
          </span>
        ),
    },
  ]
}

export default function Sessions(props: {
  report: Report
  onOpenSession: (sessionId: string) => void
}): JSX.Element {
  const { report, onOpenSession } = props
  const [sortKey, setSortKey] = useState<SortKey>('start')
  const [sortDir, setSortDir] = useState<SortDir>('desc')
  const isPhone = useMediaQuery('(max-width: 639px)')

  const sorted = useMemo(() => {
    const copy = [...report.sessions]
    copy.sort((a, b) => {
      const cmp = compare(sortValue(a, sortKey, report), sortValue(b, sortKey, report))
      return sortDir === 'desc' ? -cmp : cmp
    })
    return copy
  }, [report, sortKey, sortDir])

  const shown = sorted.slice(0, SHOWN_LIMIT)
  const maxTokens = Math.max(...shown.map((row) => (row.tokens ? row.tokens.total : 0)), 1)
  const [hiddenColumns, toggleColumn] = useHiddenColumns('auc.columns.sessions')
  const columns = buildSessionColumns(report, maxTokens)
  const shownColumns = visibleColumns(columns, hiddenColumns)

  const onHeaderSort = (key: SortKey) => {
    if (sortKey === key) {
      setSortDir(sortDir === 'desc' ? 'asc' : 'desc')
    } else {
      setSortKey(key)
      setSortDir('desc')
    }
  }

  const onSortSelect = (value: string) => {
    const option = SORT_OPTIONS.find((o) => o.value === value)
    if (!option) return
    setSortKey(option.key)
    setSortDir(option.dir)
  }

  const title = `${formatCount(report.sessions.length)} sessions, sorted by ${sortKey} ${
    sortDir === 'desc' ? 'high to low' : 'low to high'
  }`

  return (
    <Panel>
      <PanelHeader
        eyebrow="Sessions"
        title={title}
        actions={
          <>
            <SortSelect
              options={SORT_OPTIONS}
              value={`${sortKey}:${sortDir}`}
              onChange={onSortSelect}
            />
            {!isPhone && sorted.length > 0 && (
              <ColumnChooser columns={columns} hidden={hiddenColumns} onToggle={toggleColumn} />
            )}
          </>
        }
      />

      {sorted.length === 0 ? (
        <EmptyState
          title="No sessions in this slice"
          description="Widen the date range or clear a filter."
        />
      ) : isPhone ? (
        <div className="flex flex-col gap-2 p-card">
          {shown.map((row) => (
            <SessionCard
              key={row.session_id}
              session={{
                id: sessionDisplayName(row),
                state: row.cost_state,
                model: modelLabel(row.models[0], report),
                extraModels: row.models.length - 1,
                client: row.client,
                project: row.project ?? '(no project)',
                started: startLabel(row.start_time),
                requests: formatCount(row.request_count),
                tokens: row.tokens ? formatTokens(row.tokens.total) : null,
                cost: row.cost ? formatMoney(row.cost.total) : null,
                outcome: row.outcome,
                errorCount: row.error_count,
                traced: row.traced,
              }}
              onOpen={() => onOpenSession(row.session_id)}
            />
          ))}
        </div>
      ) : (
        <div className="scroll-thin overflow-x-auto">
          <Table>
            <TableHeader>
              <TableRow>
                {shownColumns.map((column) => (
                  <TableHead
                    key={column.key}
                    aria-sort={ariaSort(sortKey === column.key, sortDir)}
                    className={column.align === 'right' ? 'text-right' : 'text-left'}
                  >
                    <SortButton
                      label={column.label}
                      align={column.align}
                      active={sortKey === column.key}
                      direction={sortDir}
                      onClick={() => onHeaderSort(column.key as SortKey)}
                      className="w-full"
                    />
                  </TableHead>
                ))}
              </TableRow>
            </TableHeader>
            <TableBody>
              {shown.map((row) => (
                <TableRow
                  key={row.session_id}
                  onClick={() => onOpenSession(row.session_id)}
                  className="cursor-pointer"
                  style={{ height: 'var(--row-height)' }}
                >
                  {shownColumns.map((column) => (
                    <TableCell
                      key={column.key}
                      className={cn(column.align === 'right' && 'text-right', column.cellClassName)}
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

      {sorted.length > 0 ? (
        <PanelNote>
          {shown.length < sorted.length
            ? `Showing the first ${formatCount(shown.length)} of ${formatCount(sorted.length)} sessions. Narrow the filters to see the rest.`
            : `${formatCount(sorted.length)} sessions shown. Click any row to open its trace, economics and context.`}
        </PanelNote>
      ) : null}
    </Panel>
  )
}
