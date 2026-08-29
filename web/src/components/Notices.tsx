import type { Report } from '../api'
import { formatCount, formatTokens } from '../format'

interface NoticesProps {
  report: Report
  onDismiss: () => void
}

/** Unpriced models never reach the totals, so say so where the totals are. */
export function Notices({ report, onDismiss }: NoticesProps) {
  const { unknown_models: unknown, warnings } = report
  if (unknown.length === 0 && warnings.length === 0) return null

  return (
    <div className="rounded-xl border border-border bg-warn-soft p-4">
      <div className="flex items-start gap-3">
        <span aria-hidden className="mt-0.5 shrink-0 text-warn">
          <svg width="16" height="16" viewBox="0 0 16 16">
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
        </span>
        <div className="min-w-0 flex-1 text-[13px] leading-relaxed text-ink">
          {unknown.length > 0 ? (
            <p>
              <strong className="font-semibold">
                {unknown.length} model{unknown.length === 1 ? '' : 's'} had no price entry
              </strong>{' '}
              and {unknown.length === 1 ? 'is' : 'are'} excluded from every total, chart and table
              on this page:{' '}
              {unknown.map((item, index) => (
                <span key={item.model}>
                  {index > 0 ? ', ' : ''}
                  <code className="rounded bg-surface px-1 py-0.5 text-[12px]">{item.model}</code>{' '}
                  <span className="tnum text-ink-2" title={`${item.tokens.toLocaleString()} tokens`}>
                    ({formatTokens(item.tokens)} tok · {formatCount(item.events)} req)
                  </span>
                </span>
              ))}
              . Add them to <code className="text-[12px]">rates.json</code> to price them.
            </p>
          ) : null}
          {warnings.length > 0 ? (
            <ul className={`${unknown.length > 0 ? 'mt-2' : ''} list-disc space-y-1 pl-4`}>
              {warnings.slice(0, 6).map((warning) => (
                <li key={warning}>{warning}</li>
              ))}
              {warnings.length > 6 ? (
                <li className="text-ink-2">…and {warnings.length - 6} more.</li>
              ) : null}
            </ul>
          ) : null}
        </div>
        <button
          type="button"
          onClick={onDismiss}
          aria-label="Dismiss notice"
          className="shrink-0 rounded-md p-1 text-ink-2 hover:bg-surface hover:text-ink"
        >
          <svg width="12" height="12" viewBox="0 0 12 12" aria-hidden>
            <path
              d="M1 1l10 10M11 1L1 11"
              stroke="currentColor"
              strokeWidth="1.6"
              strokeLinecap="round"
            />
          </svg>
        </button>
      </div>
    </div>
  )
}
