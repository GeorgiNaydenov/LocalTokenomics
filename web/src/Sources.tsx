import type { JSX } from 'react'
import type { Capabilities, Meta, Provenance, Report, SourceInfo } from './api'
import { formatCount, formatDayShort, formatMoney } from './format'
import { Panel, PanelBody, PanelHeader, PanelNote } from '@/components/panel'
import { PartialMarker, ProvenanceBadge, Unavailable } from '@/components/status'
import { SourceDetail } from '@/components/source-card'
import { DisclosurePanel, WarningsList } from '@/components/states'
import { seriesColor } from '@/components/series'
import { StatLabel } from '@/components/stat'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { cn } from '@/design-system/cn'

const CAPABILITY_COLUMNS: { key: keyof Capabilities; label: string }[] = [
  { key: 'trace', label: 'Trace' },
  { key: 'tokens', label: 'Tokens' },
  { key: 'cost', label: 'Cost' },
  { key: 'context', label: 'Context' },
  { key: 'latency', label: 'Latency' },
]

const PROVENANCE_MEANING: Record<Provenance, string> = {
  measured: 'read straight out of the log',
  derived: 'computed from two logged values',
  estimated: 'from a table, not the log',
  inferred: 'read off the model id',
  unavailable: 'the log does not carry it',
}

function CapabilityMatrixPanel({ sources }: { sources: SourceInfo[] }) {
  const undetectedLabels = sources.filter((source) => !source.detected).map((source) => source.label)
  const undetectedNote =
    undetectedLabels.length > 0
      ? ` ${undetectedLabels.join(', ')} ${undetectedLabels.length === 1 ? 'ships' : 'ship'} with a reader, but ${undetectedLabels.length === 1 ? 'it was not' : 'none were'} installed here to check real logs against, so ${undetectedLabels.length === 1 ? 'its' : 'their'} capabilities read unavailable until one is audited on a real install.`
      : ' Every reader listed here was detected and audited against real logs on this machine.'

  return (
    <Panel>
      <PanelHeader
        eyebrow="Capability matrix"
        title={`What each of the ${formatCount(sources.length)} readers can tell you, and how it knows`}
      />
      <div className="scroll-thin overflow-x-auto">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead className="text-left">Source</TableHead>
              {CAPABILITY_COLUMNS.map((column) => (
                <TableHead key={column.key} className="text-left">
                  {column.label}
                </TableHead>
              ))}
            </TableRow>
          </TableHeader>
          <TableBody>
            {sources.map((source) => (
              <TableRow key={source.id}>
                <TableCell className={cn(!source.detected && 'text-muted-foreground')}>
                  {source.label}
                  {source.detected ? null : (
                    <span className="tabular ml-2 text-[10px] text-muted-foreground">
                      not detected
                    </span>
                  )}
                </TableCell>
                {CAPABILITY_COLUMNS.map((column) => {
                  const value = source.capabilities[column.key]
                  return (
                    <TableCell key={column.key}>
                      <ProvenanceBadge
                        provenance={value}
                        title={`${value}: ${PROVENANCE_MEANING[value]}`}
                      />
                    </TableCell>
                  )
                })}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
      <PanelNote>
        Every number this tool shows carries where it came from. Measured is read straight out of a
        log, derived is computed from two logged values, estimated comes from a table rather than
        the log, inferred is read off a model id, and unavailable means the log does not carry it,
        so nothing is shown rather than a zero.{undetectedNote}
      </PanelNote>
    </Panel>
  )
}

function perDay(report: Report, sourceId: string, useCost: boolean) {
  const totals = new Map<string, number>()
  for (const point of report.series) {
    if (point.source !== sourceId) continue
    const value = useCost ? point.cost : point.events
    totals.set(point.day, (totals.get(point.day) ?? 0) + value)
  }
  const days = [...totals.keys()].sort()
  return { days, values: days.map((day) => totals.get(day) ?? 0) }
}

function DetectedSource({
  source,
  index,
  report,
}: {
  source: SourceInfo
  index: number
  report: Report
}) {
  const isFull = source.token_data === 'full'
  const ownSessions = report.sessions.filter((session) => session.source === source.id)
  const priced = ownSessions.some((session) => session.cost !== null)
  const cost = ownSessions.reduce((sum, session) => sum + (session.cost ? session.cost.total : 0), 0)
  const requests = ownSessions.reduce((sum, session) => sum + session.request_count, 0)
  const lastEvent = ownSessions.reduce<string | null>(
    (latest, session) => (!latest || session.end_time > latest ? session.end_time : latest),
    null,
  )
  const showsCost = isFull && priced
  const partialCost = priced && ownSessions.some((session) => session.cost === null)
  const headline = isFull ? (
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
  )
  const trend = perDay(report, source.id, showsCost)

  return (
    <SourceDetail
      source={{
        id: source.id,
        label: source.label,
        path: source.path,
        clients: source.clients,
        hasTokens: isFull,
        headline,
        foot: '',
        color: seriesColor(index),
        trend: trend.values,
        trendLabels: trend.days.map(formatDayShort),
        formatTrend: showsCost ? formatMoney : formatCount,
        trendSeriesLabel: showsCost ? 'Cost' : 'Requests',
      }}
      stats={[
        { label: 'Files', value: formatCount(source.files) },
        { label: 'Sessions', value: formatCount(ownSessions.length) },
        { label: 'Requests', value: formatCount(requests) },
        { label: 'Last event', value: lastEvent ? formatDayShort(lastEvent.slice(0, 10)) : 'none' },
      ]}
    />
  )
}

function UndetectedSection({ sources }: { sources: SourceInfo[] }) {
  return (
    <DisclosurePanel
      title="Available, not detected here"
      summary={`${formatCount(sources.length)} more readers ship with the tool and found nothing here: ${sources
        .map((source) => source.id)
        .join(', ')}`}
    >
      <div className="space-y-3">
        {sources.map((source) => (
          <div
            key={source.id}
            className="grid gap-x-4 gap-y-1 border-t pt-3 lg:grid-cols-[200px_minmax(0,1fr)]"
          >
            <StatLabel className="normal-case tracking-normal">{source.label}</StatLabel>
            <div className="min-w-0 space-y-1">
              <p className="tabular text-[11px] break-all text-muted-foreground">{source.path}</p>
              <p className="tabular text-[11px] text-muted-foreground">{source.root_hint}</p>
            </div>
          </div>
        ))}
        <p className="max-w-prose text-xs leading-relaxed text-muted-foreground">
          These readers ship with the tool but found nothing on this machine, so they stay out of
          the filter rail, the totals, and every chart. Give one a path and it appears everywhere on
          the next scan.
        </p>
      </div>
    </DisclosurePanel>
  )
}

export default function Sources(props: { report: Report; meta: Meta }): JSX.Element {
  const { report, meta } = props
  const detected = meta.sources.filter((source) => source.detected)
  const undetected = meta.sources.filter((source) => !source.detected)
  const withTokens = detected.filter((source) => source.token_data === 'full').length

  return (
    <div className="flex flex-col gap-3">
      <CapabilityMatrixPanel sources={meta.sources} />

      <Panel>
        <PanelHeader
          eyebrow="Readers with data"
          title={`${formatCount(detected.length)} readers found logs, ${formatCount(withTokens)} of them with token counts`}
        />
        <div>
          {detected.map((source, i) => (
            <DetectedSource key={source.id} source={source} index={i} report={report} />
          ))}
        </div>
      </Panel>

      {undetected.length > 0 && <UndetectedSection sources={undetected} />}

      {report.warning_groups.length > 0 && (
        <Panel>
          <PanelHeader
            eyebrow="Scan warnings"
            title={`${formatCount(report.scan_warnings.length)} file or parse warnings, grouped into ${formatCount(report.warning_groups.length)} kind${report.warning_groups.length === 1 ? '' : 's'}`}
          />
          <PanelBody>
            <WarningsList groups={report.warning_groups} />
          </PanelBody>
        </Panel>
      )}
    </div>
  )
}
