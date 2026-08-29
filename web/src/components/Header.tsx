import type { Meta } from '../api'
import { formatDateRange } from '../format'
import type { ThemeMode } from '../theme'
import { Button } from './Controls'

interface HeaderProps {
  meta: Meta | null
  ratesAsOf: string
  mode: ThemeMode
  onToggleTheme: () => void
  onRefresh: () => void
  refreshing: boolean
}

export function Header({
  meta,
  ratesAsOf,
  mode,
  onToggleTheme,
  onRefresh,
  refreshing,
}: HeaderProps) {
  return (
    <header className="sticky top-0 z-40 border-b border-border bg-page/85 backdrop-blur-md">
      <div className="mx-auto flex max-w-[1440px] flex-wrap items-center gap-x-4 gap-y-2 px-5 py-3 lg:px-8">
        <div className="flex min-w-0 items-center gap-2.5">
          <Logo />
          <h1 className="text-[15px] font-semibold whitespace-nowrap text-ink">AI Usage Cost</h1>
        </div>

        <p className="min-w-0 flex-1 text-[12.5px] text-ink-2">
          {meta ? (
            <>
              <span className="whitespace-nowrap">
                {formatDateRange(meta.first_day, meta.last_day)}
              </span>
              <Dot />
              <span className="whitespace-nowrap text-muted">
                {meta.files_scanned.toLocaleString()} log files
              </span>
              {ratesAsOf ? (
                <>
                  <Dot />
                  <span className="whitespace-nowrap text-muted">rates as of {ratesAsOf}</span>
                </>
              ) : null}
            </>
          ) : (
            <span className="text-muted">loading…</span>
          )}
        </p>

        <div className="flex items-center gap-2">
          <Button onClick={onRefresh} disabled={refreshing} title="Re-read the local log files">
            <svg
              width="13"
              height="13"
              viewBox="0 0 16 16"
              aria-hidden
              className={refreshing ? 'animate-spin' : ''}
            >
              <path
                d="M14 8a6 6 0 1 1-1.76-4.24M14 2v4h-4"
                fill="none"
                stroke="currentColor"
                strokeWidth="1.6"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
            {refreshing ? 'Refreshing…' : 'Refresh'}
          </Button>
          <Button
            onClick={onToggleTheme}
            aria-label={`Switch to ${mode === 'dark' ? 'light' : 'dark'} theme`}
            title={`Switch to ${mode === 'dark' ? 'light' : 'dark'} theme`}
            className="px-2"
          >
            {mode === 'dark' ? <SunIcon /> : <MoonIcon />}
          </Button>
        </div>
      </div>
    </header>
  )
}

function Dot() {
  return (
    <span aria-hidden className="mx-2 text-axis">
      ·
    </span>
  )
}

function Logo() {
  return (
    <span
      aria-hidden
      className="flex h-7 w-7 items-center justify-center rounded-lg bg-accent-soft text-accent"
    >
      <svg width="15" height="15" viewBox="0 0 16 16">
        <path
          d="M2 13V9.5M6 13V5M10 13V7.5M14 13V3"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
        />
      </svg>
    </span>
  )
}

function SunIcon() {
  return (
    <svg width="15" height="15" viewBox="0 0 16 16" aria-hidden>
      <circle cx="8" cy="8" r="3.1" fill="none" stroke="currentColor" strokeWidth="1.5" />
      <path
        d="M8 .8v1.8M8 13.4v1.8M15.2 8h-1.8M2.6 8H.8M13.1 13.1l-1.3-1.3M4.2 4.2 2.9 2.9M13.1 2.9l-1.3 1.3M4.2 11.8l-1.3 1.3"
        stroke="currentColor"
        strokeWidth="1.5"
        strokeLinecap="round"
      />
    </svg>
  )
}

function MoonIcon() {
  return (
    <svg width="15" height="15" viewBox="0 0 16 16" aria-hidden>
      <path
        d="M13.5 9.6A5.8 5.8 0 0 1 6.4 2.5 5.9 5.9 0 1 0 13.5 9.6Z"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.5"
        strokeLinejoin="round"
      />
    </svg>
  )
}
