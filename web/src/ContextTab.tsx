import { useState } from 'react'
import type { JSX } from 'react'
import type { ContextSnapshot, Provenance } from './api'
import type { ContextTabProps } from './SessionWorkspace'
import { formatClock, formatCount, formatExact, formatPercent, formatTokens } from './format'
import { Panel, PanelBody, PanelHeader, PanelNote } from '@/components/panel'
import { ComparisonMeter, ProvenanceBadge, Unavailable } from '@/components/status'
import { EmptyState } from '@/components/states'
import { ContextOccupancy, HIGH_OCCUPANCY } from '@/components/trace'
import type { OccupancyPoint } from '@/components/trace'
import { Button } from '@/components/ui/button'
import { Tooltip, TooltipContent, TooltipTrigger } from '@/components/ui/tooltip'

const REVEAL_BATCH = 60
const MAX_CONTRIBUTORS = 6

const CAPACITY_NOTE: Record<Provenance, string> = {
  measured: 'The client logged this model’s context window for this call.',
  derived: 'Computed from other logged values on this call.',
  estimated: 'Read from the rate table for this model, not from the log.',
  inferred: 'Inferred from the model id: a [1m] suffix means a one million token window.',
  unavailable: 'No context window is known for this model, so no bar is drawn.',
}

const OCCUPANCY_NOTE: Record<Provenance, string> = {
  measured: 'Both the input total and the capacity came straight from the log.',
  derived: 'Logged input tokens over the logged context window.',
  estimated: 'Logged input tokens over an estimated capacity, so the percentage is only as good as that estimate.',
  inferred: 'Logged input tokens over a capacity inferred from the model id.',
  unavailable: 'Needs both an input total and a capacity; one of them is missing.',
}

function shortId(spanId: string): string {
  return spanId.length > 16 ? `${spanId.slice(0, 6)}…${spanId.slice(-6)}` : spanId
}

function deltaLabel(delta: number): string {
  return `${delta >= 0 ? '+' : '−'}${formatTokens(Math.abs(delta))}`
}

function OccupancyMeter({ snapshot }: { snapshot: ContextSnapshot }) {
  if (snapshot.occupancy === null || snapshot.capacity === null) {
    return (
      <div className="flex flex-wrap items-baseline gap-2 text-[11px]">
        <Unavailable hint={OCCUPANCY_NOTE[snapshot.occupancy_provenance]} />
        <span className="text-muted-foreground">
          {snapshot.capacity === null ? 'no capacity known for this model' : 'no input total on this call'}
        </span>
      </div>
    )
  }

  return (
    <ComparisonMeter
      value={`${formatPercent(snapshot.occupancy)} of ${formatTokens(snapshot.capacity)}`}
      fraction={snapshot.occupancy}
      color={snapshot.occupancy >= HIGH_OCCUPANCY ? 'var(--warning)' : 'var(--primary)'}
    />
  )
}

function SnapshotRow({
  snapshot,
  onFocusSpan,
}: {
  snapshot: ContextSnapshot
  onFocusSpan: (spanId: string) => void
}) {
  const contributors = snapshot.added_span_ids.slice(0, MAX_CONTRIBUTORS)
  const restCount = snapshot.added_span_ids.length - contributors.length

  return (
    <>
      {snapshot.compacted_before && (
        <div className="flex items-center gap-2 py-1 text-[10.5px] text-warning">
          <span aria-hidden="true">{'⇥'}</span>
          compacted before this call: the context was replaced, so the drop below is not the model forgetting
          <span aria-hidden className="h-px flex-1 bg-border" />
        </div>
      )}
      <div className="space-y-2.5 rounded-md border bg-card p-3">
        <div className="flex flex-wrap items-baseline gap-2">
          <span className="tabular text-[11px] text-muted-foreground">
            {formatClock(snapshot.started_at)}
          </span>
          <span className="text-xs text-foreground">{snapshot.model ?? 'no model id'}</span>
          <span className="ml-auto flex flex-wrap items-center gap-2.5 text-[11px]">
            {snapshot.input_total === null ? (
              <Unavailable hint="This call logs no input token count." />
            ) : (
              <Tooltip>
                <TooltipTrigger asChild>
                  <span tabIndex={0} className="tabular cursor-default rounded-sm outline-offset-2">
                    {`${formatTokens(snapshot.input_total)} in`}
                  </span>
                </TooltipTrigger>
                <TooltipContent>
                  <span className="tabular">{formatExact(snapshot.input_total)}</span>
                </TooltipContent>
              </Tooltip>
            )}
            <span className="tabular text-muted-foreground">
              {snapshot.delta_input === null ? (
                <Unavailable hint="The first call of this session or agent has nothing to compare against. This is an absence, not a zero." />
              ) : (
                `${deltaLabel(snapshot.delta_input)} since the previous call`
              )}
            </span>
          </span>
        </div>

        <OccupancyMeter snapshot={snapshot} />

        <div className="flex flex-wrap items-center gap-1.5">
          <ProvenanceBadge
            group="capacity"
            provenance={snapshot.capacity_provenance}
            title={CAPACITY_NOTE[snapshot.capacity_provenance]}
          />
          <ProvenanceBadge
            group="occupancy"
            provenance={snapshot.occupancy_provenance}
            title={OCCUPANCY_NOTE[snapshot.occupancy_provenance]}
          />
          <ProvenanceBadge
            group="tokens"
            provenance={snapshot.tokens_provenance}
            title={
              snapshot.tokens_provenance === 'measured'
                ? 'The input total came from the client’s own usage record.'
                : 'The input total did not come straight from a usage record.'
            }
          />
          {contributors.map((spanId) => (
            <Button
              key={spanId}
              variant="outline"
              size="xs"
              onClick={() => onFocusSpan(spanId)}
              className="tabular gap-1.5 text-[10px]"
            >
              <span className="text-muted-foreground">added</span>
              {shortId(spanId)}
            </Button>
          ))}
          {restCount > 0 && (
            <span className="text-[10px] text-muted-foreground">{`+${formatCount(restCount)} more contributors`}</span>
          )}
          {snapshot.added_span_ids.length === 0 && (
            <span className="text-[10px] text-muted-foreground">
              no new records between this call and the last
            </span>
          )}
        </div>
      </div>
    </>
  )
}

export default function ContextTab(props: ContextTabProps): JSX.Element {
  const [revealed, setRevealed] = useState(REVEAL_BATCH)
  const snapshots = props.snapshots

  if (snapshots.length === 0) {
    return (
      <EmptyState
        title="No context snapshots"
        description="A snapshot needs a model call with an input token count. This session has none, so occupancy is left blank rather than drawn as an empty bar."
      />
    )
  }

  const shown = snapshots.slice(0, revealed)
  const hidden = snapshots.length - shown.length
  const points: OccupancyPoint[] = snapshots.map((snapshot) => ({
    spanId: snapshot.span_id,
    startedAt: snapshot.started_at,
    occupancy: snapshot.occupancy,
    inputTotal: snapshot.input_total,
    capacity: snapshot.capacity,
    compactedBefore: snapshot.compacted_before,
  }))

  return (
    <div className="flex flex-col gap-3">
      <Panel>
        <PanelHeader
          eyebrow="Context"
          title={`${formatCount(snapshots.length)} model calls, occupancy over the session`}
        />
        <PanelBody>
          <ContextOccupancy
            points={points}
            formatPercent={formatPercent}
            formatTokens={formatTokens}
            formatClock={formatClock}
          />
        </PanelBody>
        {props.source === 'claude-code' && (
          <PanelNote>
            Claude Code logs no context window and no server-side context. Capacity here is
            estimated from the rate table for the model, and the contributors below are
            reconstructed from the records visible in the log between one call and the next. The
            real prompt the server assembled may hold more than this.
          </PanelNote>
        )}
      </Panel>

      <div className="flex flex-col gap-2">
        {shown.map((snapshot) => (
          <SnapshotRow key={snapshot.span_id} snapshot={snapshot} onFocusSpan={props.onFocusSpan} />
        ))}
      </div>

      {hidden > 0 && (
        <Button
          variant="outline"
          size="sm"
          className="self-start"
          onClick={() => setRevealed(revealed + REVEAL_BATCH)}
        >
          {`Show ${Math.min(REVEAL_BATCH, hidden)} more calls (${formatCount(hidden)} hidden)`}
        </Button>
      )}
    </div>
  )
}
