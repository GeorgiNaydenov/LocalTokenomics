import type { Bucket } from '../api'
import { formatCount, formatExact, formatMoney, formatPercent, formatTokens } from '../format'

/**
 * One series, so one colour for every bar -- length already encodes magnitude.
 * Rendered as a table so the numbers are readable without hovering anything.
 */
export function ProjectBreakdown({ buckets }: { buckets: Bucket[] }) {
  const rows = [...buckets].sort((a, b) => b.cost.total - a.cost.total)
  if (rows.length === 0) {
    return (
      <p className="rounded-lg border border-dashed border-border px-4 py-8 text-center text-[13px] text-muted">
        No project attribution in this slice. Codex sessions are not tagged with a project.
      </p>
    )
  }

  const max = Math.max(...rows.map((bucket) => bucket.cost.total), 0)
  const grand = rows.reduce((sum, bucket) => sum + bucket.cost.total, 0)

  return (
    <div className="overflow-x-auto thin-scroll">
      <table className="w-full min-w-[560px] border-collapse text-[13px]">
        <thead>
          <tr className="border-b border-border text-[11px] tracking-wide text-muted uppercase">
            <th className="py-2 pr-3 text-left font-medium">Project</th>
            <th className="py-2 pr-3 text-left font-medium">Share of cost</th>
            <th className="py-2 pr-3 text-right font-medium">Requests</th>
            <th className="py-2 pr-3 text-right font-medium">Sessions</th>
            <th className="py-2 pr-3 text-right font-medium">Tokens</th>
            <th className="py-2 text-right font-medium">Cost</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((bucket) => (
            <tr key={bucket.key} className="border-b border-border last:border-0">
              <td className="max-w-[220px] truncate py-2.5 pr-3 font-medium text-ink" title={bucket.label}>
                {bucket.label}
              </td>
              <td className="w-[42%] py-2.5 pr-3">
                <span className="flex items-center gap-2.5">
                  <span className="h-2.5 flex-1 overflow-hidden rounded-full bg-surface-2">
                    <span
                      className="block h-full rounded-full"
                      style={{
                        width: `${max > 0 ? Math.max((bucket.cost.total / max) * 100, 1) : 0}%`,
                        background: 'var(--meter-fill)',
                      }}
                    />
                  </span>
                  <span className="tnum w-9 shrink-0 text-right text-[12px] text-muted">
                    {grand > 0 ? formatPercent(bucket.cost.total / grand) : '0%'}
                  </span>
                </span>
              </td>
              <td className="tnum py-2.5 pr-3 text-right text-ink-2">{formatCount(bucket.events)}</td>
              <td className="tnum py-2.5 pr-3 text-right text-ink-2">
                {formatCount(bucket.sessions)}
              </td>
              <td
                className="tnum py-2.5 pr-3 text-right text-ink-2"
                title={formatExact(bucket.tokens.total)}
              >
                {formatTokens(bucket.tokens.total)}
              </td>
              <td className="tnum py-2.5 text-right font-semibold text-ink">
                {formatMoney(bucket.cost.total)}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
