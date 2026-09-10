import * as React from 'react'
import { ArrowUpDownIcon, ChevronDownIcon, ChevronUpIcon } from 'lucide-react'

import { Button } from '@/components/ui/button'
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from '@/components/ui/collapsible'
import type { WarningGroup, WarningSeverity } from '@/api'
import { Skeleton } from '@/components/ui/skeleton'
import { ToggleGroup, ToggleGroupItem } from '@/components/ui/toggle-group'
import { CodeBlock } from '@/components/detail'
import { Panel, PanelBody, PanelHeader } from '@/components/panel'
import { MetricInfo } from '@/components/metric-info'
import { cn } from '@/design-system/cn'
import { formatCount, formatExact, formatMoney } from '@/format'

export type SortDirection = 'asc' | 'desc'

export function ariaSort(
  active: boolean,
  direction: SortDirection,
): 'ascending' | 'descending' | 'none' {
  if (!active) return 'none'
  return direction === 'asc' ? 'ascending' : 'descending'
}

export function SortButton({
  label,
  active,
  direction,
  onClick,
  align = 'left',
  className,
}: {
  label: string
  active: boolean
  direction: SortDirection
  onClick: () => void
  align?: 'left' | 'right'
  className?: string
}) {
  const Icon = !active ? ArrowUpDownIcon : direction === 'asc' ? ChevronUpIcon : ChevronDownIcon

  return (
    <button
      type="button"
      onClick={onClick}
      className={cn(
        'group inline-flex items-center gap-1 text-xs font-medium uppercase tracking-[0.06em] transition-colors',
        active ? 'text-foreground' : 'text-muted-foreground hover:text-foreground',
        align === 'right' && 'flex-row-reverse',
        className,
      )}
    >
      {label}
      <Icon
        className={cn(
          'size-3 transition-opacity',
          active ? 'opacity-100' : 'opacity-0 group-hover:opacity-60',
        )}
      />
    </button>
  )
}

export function EmptyState({
  title,
  description,
  action,
  icon,
  className,
}: {
  title: string
  description?: React.ReactNode
  action?: React.ReactNode
  icon?: React.ReactNode
  className?: string
}) {
  return (
    <div
      className={cn(
        'flex flex-col items-center justify-center gap-3 rounded-md border border-dashed px-6 py-14 text-center',
        className,
      )}
    >
      {icon ? <div className="text-muted-foreground">{icon}</div> : null}
      <p className="text-sm font-medium">{title}</p>
      {description ? (
        <p className="max-w-md text-xs leading-relaxed text-muted-foreground">{description}</p>
      ) : null}
      {action}
    </div>
  )
}

export function ErrorState({
  title = 'Something went wrong',
  message,
  onRetry,
  className,
}: {
  title?: string
  message: string
  onRetry?: () => void
  className?: string
}) {
  return (
    <Panel className={cn('border-destructive/40', className)}>
      <PanelHeader title={title} hint={message} />
      {onRetry ? (
        <PanelBody>
          <Button variant="outline" size="sm" onClick={onRetry}>
            Try again
          </Button>
        </PanelBody>
      ) : null}
    </Panel>
  )
}

export function PanelSkeleton({ rows = 4, className }: { rows?: number; className?: string }) {
  return (
    <Panel className={className}>
      <PanelHeader title={<Skeleton className="h-4 w-40" />} />
      <PanelBody className="space-y-3">
        {Array.from({ length: rows }, (_, index) => (
          <Skeleton key={index} className="h-4" style={{ width: `${92 - index * 11}%` }} />
        ))}
      </PanelBody>
    </Panel>
  )
}

export function DisclosurePanel({
  title,
  summary,
  children,
  className,
}: {
  title: string
  summary: string
  children: React.ReactNode
  className?: string
}) {
  const [open, setOpen] = React.useState(false)

  return (
    <Collapsible
      open={open}
      onOpenChange={setOpen}
      className={cn('rounded-md border border-dashed', className)}
    >
      <CollapsibleTrigger className="flex w-full items-start gap-3 p-card text-left">
        <ChevronDownIcon
          className={cn(
            'mt-0.5 size-4 shrink-0 text-muted-foreground transition-transform',
            open && 'rotate-180',
          )}
        />
        <span className="min-w-0">
          <span className="block text-[11px] font-medium uppercase tracking-[0.08em] text-muted-foreground">
            {title}
          </span>
          <span className="mt-1 block text-xs leading-relaxed text-muted-foreground">{summary}</span>
        </span>
      </CollapsibleTrigger>
      <CollapsibleContent className="border-t px-card py-4">{children}</CollapsibleContent>
    </Collapsible>
  )
}

const WARNING_SEVERITY: Record<WarningSeverity, { color: string; label: string }> = {
  info: { color: 'var(--primary)', label: 'Info' },
  caution: { color: 'var(--warning)', label: 'Caution' },
  critical: { color: 'var(--destructive)', label: 'Critical' },
}

function warningInfo(group: WarningGroup) {
  const parts = [
    group.severity === 'critical'
      ? 'Critical: the affected totals are materially wrong and nothing here has corrected for it.'
      : group.severity === 'caution'
        ? 'Caution: the tool already bounded or partly corrected for this, so the effect on totals is limited.'
        : 'Info: cosmetic — this does not change any total shown.',
  ]
  if (group.total_delta_tokens > 0 || group.total_delta_cost > 0) {
    parts.push(
      `Estimated impact across ${formatCount(group.count)} instance${group.count === 1 ? '' : 's'}: ${formatExact(group.total_delta_tokens)} tokens, about ${formatMoney(group.total_delta_cost)}.`,
    )
  }
  if (group.affected_sessions > 0) {
    parts.push(`Touches ${formatCount(group.affected_sessions)} session${group.affected_sessions === 1 ? '' : 's'}.`)
  }
  if (group.worst_example?.likely_cause) {
    parts.push(`Likely cause: ${group.worst_example.likely_cause}.`)
  }
  return parts.join(' ')
}

function WarningGroupRow({ group }: { group: WarningGroup }) {
  const [expanded, setExpanded] = React.useState(false)
  const meta = WARNING_SEVERITY[group.severity]
  const instances = group.instances.length > 0 ? group.instances : group.warnings.map((message) => ({ message }))

  return (
    <div className="space-y-2 rounded-md border p-3">
      <div className="flex items-baseline justify-between gap-3">
        <div className="flex items-start gap-2">
          <MetricInfo
            content={{ kind: 'simple', text: warningInfo(group) }}
            ariaLabel={`Explain the ${meta.label.toLowerCase()} severity of this warning group`}
            triggerClassName="mt-1 inline-flex"
          >
            <span
              aria-hidden
              className="size-1.5 shrink-0 rounded-full"
              style={{ background: meta.color }}
            />
          </MetricInfo>
          <p className="text-xs leading-relaxed">{group.summary}</p>
        </div>
        {group.count > 1 && (
          <Button variant="ghost" size="xs" onClick={() => setExpanded(!expanded)} className="shrink-0">
            {expanded ? 'Hide files' : `Show ${group.count} files`}
          </Button>
        )}
      </div>
      {(expanded || group.count === 1) && (
        <ul className="space-y-2 border-t pt-2">
          {instances.map((instance, index) => (
            <li
              key={index}
              className="tabular flex gap-2.5 text-[11px] leading-relaxed text-muted-foreground"
            >
              <span aria-hidden className="mt-1.5 size-1 shrink-0 rounded-full bg-warning" />
              {instance.message}
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}

export function WarningsList({ groups, className }: { groups: WarningGroup[]; className?: string }) {
  const [kinds, setKinds] = React.useState<string[]>([])
  const shown = kinds.length === 0 ? groups : groups.filter((group) => kinds.includes(group.kind))

  return (
    <div className={cn('space-y-3', className)}>
      {groups.length > 1 && (
        <ToggleGroup
          type="multiple"
          variant="outline"
          size="sm"
          spacing={1.5}
          value={kinds}
          onValueChange={setKinds}
          className="flex-wrap"
        >
          {groups.map((group) => (
            <ToggleGroupItem key={group.kind} value={group.kind} className="gap-1.5 text-xs">
              {group.label}
              <span className="tabular text-[10px] text-muted-foreground">{group.count}</span>
            </ToggleGroupItem>
          ))}
        </ToggleGroup>
      )}
      <div className="space-y-2">
        {shown.map((group) => (
          <WarningGroupRow key={group.kind} group={group} />
        ))}
      </div>
    </div>
  )
}

export function OfflineCard({
  host,
  command,
  onRetry,
  className,
}: {
  host: string
  command: string
  onRetry: () => void
  className?: string
}) {
  const [copied, setCopied] = React.useState(false)

  const copy = () => {
    navigator.clipboard
      .writeText(command)
      .then(() => {
        setCopied(true)
        setTimeout(() => setCopied(false), 2000)
      })
      .catch(() => undefined)
  }

  return (
    <div className={cn('grid min-h-svh place-items-center p-6', className)}>
      <Panel className="w-full max-w-lg border-t-2 border-t-destructive">
        <PanelBody className="space-y-4">
          <p className="text-[11px] font-medium uppercase tracking-[0.08em] text-destructive">
            No server on {host}
          </p>
          <h1 className="text-xl font-semibold tracking-[-0.01em]">
            The dashboard lost the local reader.
          </h1>
          <p className="text-sm leading-relaxed text-muted-foreground">
            Nothing was uploaded and nothing was lost. The last scan is still in your local SQLite
            store. Start the reader again and this view reconnects.
          </p>
          <CodeBlock>{command}</CodeBlock>
          <div className="flex gap-2">
            <Button onClick={onRetry}>Retry connection</Button>
            <Button variant="outline" onClick={copy}>
              {copied ? 'Copied' : 'Copy command'}
            </Button>
          </div>
        </PanelBody>
      </Panel>
    </div>
  )
}

export function StatSkeleton() {
  return (
    <div className="space-y-4 rounded-md border bg-card p-card">
      <Skeleton className="h-2.5 w-24" />
      <Skeleton className="h-8 w-32" />
      <Skeleton className="h-2.5 w-40" />
    </div>
  )
}
