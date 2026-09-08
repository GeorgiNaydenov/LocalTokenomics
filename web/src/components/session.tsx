import type { CostState, OutcomeLabel } from '@/api'
import { Tooltip, TooltipContent, TooltipTrigger } from '@/components/ui/tooltip'
import { cn } from '@/design-system/cn'
import { COST_STATE_META, OutcomeBadge, Unavailable } from '@/components/status'

export function TracedDot({ traced, className }: { traced: boolean; className?: string }) {
  return (
    <Tooltip>
      <TooltipTrigger asChild>
        <span
          tabIndex={0}
          aria-label={traced ? 'Traced' : 'Not traced'}
          className={cn(
            'size-1.5 shrink-0 rounded-full outline-offset-2',
            traced ? 'bg-primary' : 'border border-border',
            className,
          )}
        />
      </TooltipTrigger>
      <TooltipContent>
        {traced
          ? 'Trace spans were captured for this session.'
          : 'No trace spans were captured for this session.'}
      </TooltipContent>
    </Tooltip>
  )
}

export function ErrorCount({ count, className }: { count: number; className?: string }) {
  return (
    <Tooltip>
      <TooltipTrigger asChild>
        <span
          tabIndex={0}
          className={cn(
            'tabular cursor-default rounded-sm outline-offset-2',
            count > 0 ? 'text-destructive' : 'text-muted-foreground',
            className,
          )}
        >
          {count}
        </span>
      </TooltipTrigger>
      <TooltipContent>
        {count === 1 ? '1 error in this session' : `${count} errors in this session`}
      </TooltipContent>
    </Tooltip>
  )
}

export function TokenCell({
  label,
  fraction,
  state,
  className,
}: {
  label: string | null
  fraction: number
  state: CostState
  className?: string
}) {
  if (label === null) {
    return (
      <span className={cn('tabular block text-right', className)}>
        <Unavailable />
      </span>
    )
  }
  return (
    <Tooltip>
      <TooltipTrigger asChild>
        <span
          tabIndex={0}
          className={cn(
            'flex cursor-default items-center justify-end gap-2 rounded-sm outline-offset-2',
            className,
          )}
        >
          <span className="tabular text-muted-foreground">{label}</span>
          <span className="h-2 w-[52px] shrink-0 overflow-hidden rounded-full bg-muted">
            <span
              className="block h-full rounded-full"
              style={{
                width: `${Math.min(100, Math.max(0, fraction * 100))}%`,
                background: COST_STATE_META[state].color,
              }}
            />
          </span>
        </span>
      </TooltipTrigger>
      <TooltipContent>
        <span className="tabular">
          {label} tokens ({Math.round(fraction * 100)}% of the largest row shown)
        </span>
      </TooltipContent>
    </Tooltip>
  )
}

export interface SessionSummary {
  id: string
  state: CostState
  model: string
  extraModels: number
  client: string
  project: string
  started: string
  requests: string
  tokens: string | null
  cost: string | null
  outcome?: OutcomeLabel
  errorCount?: number
  traced?: boolean
}

export function SessionCard({
  session,
  onOpen,
  className,
}: {
  session: SessionSummary
  onOpen: () => void
  className?: string
}) {
  const meta = COST_STATE_META[session.state]
  const errorCount = session.errorCount

  return (
    <div
      className={cn(
        'relative flex w-full flex-col gap-2 rounded-md border bg-card p-3 text-left transition-colors hover:bg-accent',
        className,
      )}
    >
      <button
        type="button"
        onClick={onOpen}
        aria-label={`Open session ${session.id}`}
        className="absolute inset-0 rounded-md outline-offset-2"
      />
      <div className="flex items-center gap-2">
        <span aria-hidden className="size-1.5 rounded-full" style={{ background: meta.color }} />
        <span className="text-xs text-muted-foreground">{meta.label}</span>
        {session.traced === undefined ? null : (
          <>
            <span
              aria-hidden
              className={cn(
                'size-1.5 shrink-0 rounded-full',
                session.traced ? 'bg-primary' : 'border border-border',
              )}
            />
            <span className="sr-only">{session.traced ? 'Traced' : 'Not traced'}</span>
          </>
        )}
        <span className="tabular ml-auto min-w-0 truncate text-[13px] font-medium">{session.id}</span>
      </div>
      {session.outcome ? (
        <div className="flex items-center justify-between gap-2">
          <OutcomeBadge outcome={session.outcome} />
          {errorCount === undefined ? null : (
            <span
              className={cn(
                'tabular text-[11px]',
                errorCount > 0 ? 'text-destructive' : 'text-muted-foreground',
              )}
            >
              {errorCount} errors
            </span>
          )}
        </div>
      ) : null}
      <div className="text-[13px]">
        {session.model}
        {session.extraModels > 0 ? (
          <span className="tabular ml-1.5 text-xs text-muted-foreground">
            +{session.extraModels}
          </span>
        ) : null}
      </div>
      <div className="flex justify-between text-xs text-muted-foreground">
        <span>{session.client}</span>
        <span className="truncate pl-3">{session.project}</span>
      </div>
      <div className="tabular flex justify-between text-[11px] text-muted-foreground">
        <span>{session.started}</span>
        <span>{session.requests} req</span>
      </div>
      <div className="flex items-center justify-between">
        <span className="tabular text-xs text-muted-foreground">
          {session.tokens ?? <Unavailable />}
        </span>
        <span
          className={cn(
            'tabular text-[13px] font-semibold',
            session.cost === null && 'font-normal text-muted-foreground',
          )}
        >
          {session.cost ?? <Unavailable />}
        </span>
      </div>
    </div>
  )
}
