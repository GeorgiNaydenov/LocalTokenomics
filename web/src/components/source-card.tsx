import type { ReactNode } from 'react'

import { Badge } from '@/components/ui/badge'
import { Sparkline } from '@/components/sparkline'
import { StatLabel } from '@/components/stat'
import { cn } from '@/design-system/cn'

export interface SourceSummary {
  id: string
  label: string
  path: string
  clients?: string[]
  hasTokens: boolean
  headline: ReactNode
  foot: string
  color: string
  trend: number[]
  trendLabels?: string[]
  formatTrend?: (value: number) => string
  trendSeriesLabel?: string
}

function TokenDataBadge({ hasTokens }: { hasTokens: boolean }) {
  return (
    <Badge variant={hasTokens ? 'default' : 'outline'} className="text-[10px]">
      {hasTokens ? 'token counts' : 'session only'}
    </Badge>
  )
}

export function SourceCard({ source, className }: { source: SourceSummary; className?: string }) {
  return (
    <div className={cn('flex flex-col gap-2.5 border-r border-b p-4 last:border-r-0', className)}>
      <div className="flex items-center gap-2">
        <span aria-hidden className="size-1.5 rounded-full" style={{ background: source.color }} />
        <span className="text-[13px] font-semibold">{source.label}</span>
        <TokenDataBadge hasTokens={source.hasTokens} />
      </div>
      <p className="tabular text-[10px] leading-relaxed break-all text-muted-foreground">
        {source.path}
      </p>
      <div className="flex items-end justify-between gap-3">
        <div>
          <div className="tabular text-lg font-semibold leading-none">{source.headline}</div>
          <div className="mt-1.5 text-[11px] text-muted-foreground">{source.foot}</div>
        </div>
        <Sparkline
          values={source.trend}
          width={96}
          height={26}
          color={source.color}
          fill
          label={`${source.label} activity over time`}
          labels={source.trendLabels}
          format={source.formatTrend}
          seriesLabel={source.trendSeriesLabel}
          className="w-24"
        />
      </div>
    </div>
  )
}

export function SourceDetail({
  source,
  stats,
  className,
}: {
  source: SourceSummary
  stats: { label: string; value: string }[]
  className?: string
}) {
  return (
    <div
      className={cn(
        'grid gap-x-6 gap-y-4 border-b p-card last:border-b-0 lg:grid-cols-[minmax(180px,220px)_minmax(0,1fr)]',
        className,
      )}
    >
      <div className="space-y-2">
        <div className="flex items-center gap-2">
          <span aria-hidden className="size-1.5 rounded-full" style={{ background: source.color }} />
          <span className="text-[13px] font-semibold">{source.label}</span>
        </div>
        {source.clients?.length ? (
          <p className="tabular text-[11px] text-muted-foreground">{source.clients.join(', ')}</p>
        ) : null}
        <TokenDataBadge hasTokens={source.hasTokens} />
        <div className="tabular pt-1 text-xl font-semibold leading-none">{source.headline}</div>
      </div>
      <div className="min-w-0 space-y-3">
        <p className="tabular text-[11px] break-all text-muted-foreground">{source.path}</p>
        <div className="flex flex-wrap gap-x-8 gap-y-3">
          {stats.map((stat) => (
            <div key={stat.label} className="space-y-0.5">
              <StatLabel>{stat.label}</StatLabel>
              <p className="tabular text-sm font-semibold">{stat.value}</p>
            </div>
          ))}
        </div>
        <Sparkline
          values={source.trend}
          width={96}
          height={30}
          color={source.color}
          fill
          stretch
          label={`${source.label} activity over time`}
          labels={source.trendLabels}
          format={source.formatTrend}
          seriesLabel={source.trendSeriesLabel}
        />
      </div>
    </div>
  )
}
