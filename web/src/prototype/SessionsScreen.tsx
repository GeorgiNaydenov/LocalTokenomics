import { useMemo, useState } from 'react'

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { Panel, PanelBody, PanelHeader, PanelNote } from '@/components/panel'
import { SortSelect } from '@/components/filters'
import { SessionCard, TokenCell } from '@/components/session'
import { SortButton, type SortDirection } from '@/components/states'
import { Tooltip, TooltipContent, TooltipTrigger } from '@/components/ui/tooltip'
import { CostStateBadge, OutcomeBadge } from '@/components/status'
import { seriesColor } from '@/components/series'
import { useMediaQuery } from '@/components/use-media-query'
import { formatCount, formatMoney, formatTokens } from '@/format'
import { SESSIONS, SESSION_LIMIT, SORT_OPTIONS, type PrototypeSession } from './data'

type SortKey =
  | 'state'
  | 'outcome'
  | 'id'
  | 'client'
  | 'model'
  | 'project'
  | 'start'
  | 'requests'
  | 'tokens'
  | 'cost'

const COLUMNS: { key: SortKey; label: string; align: 'left' | 'right' }[] = [
  { key: 'state', label: 'State', align: 'left' },
  { key: 'outcome', label: 'Outcome', align: 'left' },
  { key: 'id', label: 'Session', align: 'left' },
  { key: 'client', label: 'Client', align: 'left' },
  { key: 'model', label: 'Model', align: 'left' },
  { key: 'project', label: 'Project', align: 'left' },
  { key: 'start', label: 'Started', align: 'left' },
  { key: 'requests', label: 'Req', align: 'right' },
  { key: 'tokens', label: 'Tokens', align: 'right' },
  { key: 'cost', label: 'Cost', align: 'right' },
]

function tokenTotal(session: PrototypeSession): number {
  if (!session.tokens) return -1
  return Object.values(session.tokens).reduce((a, b) => a + b, 0)
}

function sortValue(session: PrototypeSession, key: SortKey): string | number {
  switch (key) {
    case 'state':
      return session.state
    case 'outcome':
      return session.outcome
    case 'id':
      return session.id
    case 'client':
      return session.client
    case 'model':
      return session.models[0]
    case 'project':
      return session.project
    case 'start':
      return session.started
    case 'requests':
      return session.requests
    case 'tokens':
      return tokenTotal(session)
    case 'cost':
      return session.cost ?? -1
  }
}

function compare(a: string | number, b: string | number): number {
  if (typeof a === 'string' || typeof b === 'string') return String(a).localeCompare(String(b))
  return a - b
}

export function SessionsScreen({ onOpen }: { onOpen: (session: PrototypeSession) => void }) {
  const [sortKey, setSortKey] = useState<SortKey>('cost')
  const [sortDir, setSortDir] = useState<SortDirection>('desc')
  const isPhone = useMediaQuery('(max-width: 639px)')

  const sorted = useMemo(() => {
    const copy = [...SESSIONS]
    copy.sort((a, b) => {
      const result = compare(sortValue(a, sortKey), sortValue(b, sortKey))
      return sortDir === 'desc' ? -result : result
    })
    return copy
  }, [sortKey, sortDir])

  const shown = sorted.slice(0, SESSION_LIMIT)
  const maxTokens = Math.max(...shown.map((session) => Math.max(0, tokenTotal(session))), 1)

  const onHeaderSort = (key: SortKey) => {
    if (key === sortKey) setSortDir((value) => (value === 'desc' ? 'asc' : 'desc'))
    else {
      setSortKey(key)
      setSortDir('desc')
    }
  }

  return (
    <Panel>
      <PanelHeader
        eyebrow="Sessions"
        title={`${formatCount(sorted.length)} sessions, sorted by ${sortKey} ${
          sortDir === 'desc' ? 'high to low' : 'low to high'
        }`}
        actions={
          <SortSelect
            options={SORT_OPTIONS}
            value={`${sortKey}:${sortDir}`}
            onChange={(value) => {
              const [key, dir] = value.split(':')
              setSortKey(key as SortKey)
              setSortDir(dir as SortDirection)
            }}
          />
        }
      />

      {isPhone ? (
        <PanelBody className="flex flex-col gap-2">
          {shown.map((session) => (
            <SessionCard
              key={session.id}
              session={{
                id: session.id,
                state: session.state,
                model: session.models[0],
                extraModels: session.models.length - 1,
                client: session.client,
                project: session.project,
                started: session.startedLabel,
                requests: formatCount(session.requests),
                tokens: session.tokens ? formatTokens(tokenTotal(session)) : null,
                cost: session.cost === null ? null : formatMoney(session.cost),
              }}
              onOpen={() => onOpen(session)}
            />
          ))}
        </PanelBody>
      ) : (
        <div className="scroll-thin overflow-x-auto">
          <Table>
            <TableHeader>
              <TableRow>
                {COLUMNS.map((column) => (
                  <TableHead key={column.key} className={column.align === 'right' ? 'text-right' : undefined}>
                    <SortButton
                      label={column.label}
                      align={column.align}
                      active={sortKey === column.key}
                      direction={sortDir}
                      onClick={() => onHeaderSort(column.key)}
                    />
                  </TableHead>
                ))}
              </TableRow>
            </TableHeader>
            <TableBody>
              {shown.map((session) => (
                <TableRow
                  key={session.id}
                  onClick={() => onOpen(session)}
                  className="cursor-pointer"
                  style={{ height: 'var(--row-height)' }}
                >
                  <TableCell>
                    <CostStateBadge state={session.state} />
                  </TableCell>
                  <TableCell>
                    <span className="inline-flex items-center gap-1.5">
                      <OutcomeBadge outcome={session.outcome} />
                      {session.errorCount > 0 ? (
                        <Tooltip>
                          <TooltipTrigger asChild>
                            <span
                              tabIndex={0}
                              className="tabular cursor-default rounded-sm text-[11px] text-destructive outline-offset-2"
                            >
                              {session.errorCount}!
                            </span>
                          </TooltipTrigger>
                          <TooltipContent>
                            {session.errorCount === 1
                              ? '1 error in this session'
                              : `${session.errorCount} errors in this session`}
                          </TooltipContent>
                        </Tooltip>
                      ) : null}
                    </span>
                  </TableCell>
                  <TableCell className="tabular font-medium">{session.id}</TableCell>
                  <TableCell className="text-muted-foreground">{session.client}</TableCell>
                  <TableCell className="text-muted-foreground">
                    <span className="inline-flex items-center gap-2">
                      <span
                        aria-hidden
                        className="size-1.5 rounded-full"
                        style={{ background: seriesColor(session.slot) }}
                      />
                      {session.models[0]}
                      {session.models.length > 1 ? (
                        <span className="tabular text-[11px]">+{session.models.length - 1}</span>
                      ) : null}
                    </span>
                  </TableCell>
                  <TableCell className="text-muted-foreground">{session.project}</TableCell>
                  <TableCell className="tabular text-muted-foreground">{session.startedLabel}</TableCell>
                  <TableCell className="tabular text-right text-muted-foreground">
                    {formatCount(session.requests)}
                  </TableCell>
                  <TableCell>
                    <TokenCell
                      label={session.tokens ? formatTokens(tokenTotal(session)) : null}
                      fraction={tokenTotal(session) / maxTokens}
                      state={session.state}
                    />
                  </TableCell>
                  <TableCell
                    className={
                      session.cost === null
                        ? 'tabular text-right text-muted-foreground'
                        : 'tabular text-right font-semibold'
                    }
                  >
                    {session.cost === null ? 'n/a' : formatMoney(session.cost)}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      )}

      <PanelNote>
        {shown.length < sorted.length
          ? `Showing the first ${formatCount(shown.length)} of ${formatCount(sorted.length)} sessions. Narrow the filters to see the rest.`
          : `${formatCount(sorted.length)} sessions shown. Click any row for its token buckets and log files.`}
      </PanelNote>
    </Panel>
  )
}
