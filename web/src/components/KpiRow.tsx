import type { Report } from '../api'
import { formatCount, formatExact, formatMoney, formatPercent, formatTokens } from '../format'
import type { ThemeMode } from '../theme'
import { seriesColor } from '../theme'
import { Card } from './Card'
import { Swatch } from './Controls'

interface KpiRowProps {
  report: Report
  clientOrder: string[]
  mode: ThemeMode
}

export function KpiRow({ report, clientOrder, mode }: KpiRowProps) {
  const { totals } = report
  const clients = report.by_client
  const clientTotal = clients.reduce((sum, bucket) => sum + bucket.cost.total, 0)

  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-12">
      <Card className="flex flex-col justify-between lg:col-span-6">
        <div>
          <p className="text-[13px] font-medium text-ink-2">Total API-equivalent cost</p>
          <p className="mt-1 text-[46px] leading-[1.05] font-semibold tracking-tight text-ink">
            {formatMoney(totals.cost.total)}
          </p>
          <p className="mt-1 text-[12.5px] text-muted">
            What these {formatCount(totals.events)} requests would cost at published API list
            prices.
          </p>
        </div>

        <div className="mt-5">
          <div className="mb-2 flex items-baseline justify-between">
            <span className="text-[11px] font-medium tracking-wide text-muted uppercase">
              By client
            </span>
          </div>
          {clients.length === 0 ? (
            <p className="text-[13px] text-muted">No priced requests in this slice.</p>
          ) : (
            <>
              <div
                className="flex h-2.5 w-full gap-0.5 overflow-hidden rounded-full bg-surface-2"
                role="img"
                aria-label="Share of cost by client"
              >
                {clients.map((bucket) => (
                  <span
                    key={bucket.key}
                    className="h-full"
                    style={{
                      width: `${clientTotal > 0 ? (bucket.cost.total / clientTotal) * 100 : 0}%`,
                      background: seriesColor(clientOrder.indexOf(bucket.key), mode),
                    }}
                  />
                ))}
              </div>
              <dl className="mt-3 flex flex-wrap gap-x-7 gap-y-2">
                {clients.map((bucket) => (
                  <div key={bucket.key} className="min-w-0">
                    <dt className="flex items-center gap-1.5 text-[12px] text-ink-2">
                      <Swatch color={seriesColor(clientOrder.indexOf(bucket.key), mode)} />
                      <span className="truncate">{bucket.label}</span>
                    </dt>
                    <dd className="tnum mt-0.5 text-[17px] font-semibold text-ink">
                      {formatMoney(bucket.cost.total)}
                      <span className="ml-1.5 text-[12px] font-normal text-muted">
                        {clientTotal > 0 ? formatPercent(bucket.cost.total / clientTotal) : '0%'}
                      </span>
                    </dd>
                  </div>
                ))}
              </dl>
            </>
          )}
        </div>
      </Card>

      <StatTile
        className="lg:col-span-2"
        label="Tokens"
        value={formatTokens(totals.tokens.total)}
        title={formatExact(totals.tokens.total)}
        foot={`${formatTokens(totals.tokens.cache_read)} of it cache reads`}
      />
      <StatTile
        className="lg:col-span-2"
        label="Requests"
        value={formatCount(totals.events)}
        foot={`across ${formatCount(report.files_scanned)} log files`}
      />
      <StatTile
        className="lg:col-span-2"
        label="Sessions"
        value={formatCount(totals.sessions)}
        foot={
          totals.sessions > 0
            ? `${formatMoney(totals.cost.total / totals.sessions)} avg per session`
            : '—'
        }
      />
    </div>
  )
}

interface StatTileProps {
  label: string
  value: string
  foot: string
  title?: string
  className?: string
}

function StatTile({ label, value, foot, title, className = '' }: StatTileProps) {
  return (
    <Card className={`flex flex-col justify-between ${className}`}>
      <p className="text-[13px] font-medium text-ink-2">{label}</p>
      <p className="mt-3 text-[30px] leading-none font-semibold tracking-tight text-ink" title={title}>
        {value}
      </p>
      <p className="mt-2 text-[12px] leading-snug text-muted">{foot}</p>
    </Card>
  )
}
