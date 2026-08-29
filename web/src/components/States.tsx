import { Card } from './Card'
import { Button } from './Controls'

export function DashboardSkeleton() {
  return (
    <div className="space-y-4" aria-busy="true" aria-label="Loading usage data">
      <div className="skeleton h-[86px] rounded-xl" />
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-12">
        <div className="skeleton h-[212px] rounded-xl lg:col-span-6" />
        <div className="skeleton h-[212px] rounded-xl lg:col-span-2" />
        <div className="skeleton h-[212px] rounded-xl lg:col-span-2" />
        <div className="skeleton h-[212px] rounded-xl lg:col-span-2" />
      </div>
      <div className="skeleton h-[168px] rounded-xl" />
      <div className="skeleton h-[392px] rounded-xl" />
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <div className="skeleton h-[300px] rounded-xl" />
        <div className="skeleton h-[300px] rounded-xl" />
      </div>
    </div>
  )
}

export function ErrorState({ message, onRetry }: { message: string; onRetry: () => void }) {
  return (
    <Card className="mx-auto max-w-xl text-center">
      <p className="mx-auto mb-3 flex h-9 w-9 items-center justify-center rounded-full bg-warn-soft text-warn">
        <svg width="18" height="18" viewBox="0 0 16 16" aria-hidden>
          <path
            d="M8 1.6 15 14H1L8 1.6Z"
            fill="none"
            stroke="currentColor"
            strokeWidth="1.5"
            strokeLinejoin="round"
          />
          <path d="M8 6v3.4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
          <circle cx="8" cy="11.6" r="0.9" fill="currentColor" />
        </svg>
      </p>
      <h2 className="text-[15px] font-semibold text-ink">Can’t load the report</h2>
      <p className="mx-auto mt-1.5 max-w-md text-[13px] leading-relaxed text-ink-2">{message}</p>
      <p className="mt-3 text-[12px] text-muted">
        Start it with{' '}
        <code className="rounded bg-surface-2 px-1.5 py-0.5">ai-usage-cost serve</code>.
      </p>
      <div className="mt-4">
        <Button variant="solid" onClick={onRetry}>
          Try again
        </Button>
      </div>
    </Card>
  )
}

export function EmptyState({ onReset }: { onReset: () => void }) {
  return (
    <Card className="text-center">
      <h2 className="text-[15px] font-semibold text-ink">Nothing matches these filters</h2>
      <p className="mx-auto mt-1.5 max-w-md text-[13px] leading-relaxed text-ink-2">
        No priced requests fall inside this date range and dimension selection. Widen the range or
        clear a filter.
      </p>
      <div className="mt-4">
        <Button variant="solid" onClick={onReset}>
          Reset filters
        </Button>
      </div>
    </Card>
  )
}
