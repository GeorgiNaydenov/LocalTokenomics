import { useEffect, useState } from 'react'
import type { Meta, View } from './api'
import type { ThemeMode } from './theme'

interface HeaderProps {
  view: View
  onSelectView: (view: View) => void
  meta: Meta | null
  ratesAsOf: string
  filesScanned: number
  onRescan: () => void
  rescanning: boolean
  lastScanAt: number | null
  mode: ThemeMode
  onToggleTheme: () => void
  onOpenRail?: () => void
}

const TABS: { id: View; label: string }[] = [
  { id: 'overview', label: 'Overview' },
  { id: 'sessions', label: 'Sessions' },
  { id: 'sources', label: 'Sources' },
  { id: 'pricing', label: 'Models and pricing' },
]

function Logo() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
      <path d="M5 6 A13 13 0 0 1 18 19" stroke="var(--accent)" strokeWidth={1.8} strokeLinecap="round" />
      <line x1="5" y1="19" x2="12.6" y2="11.4" stroke="var(--fg-strong)" strokeWidth={1.4} strokeLinecap="round" />
      <circle cx="5" cy="19" r="1.3" fill="var(--fg-strong)" />
    </svg>
  )
}

function scanReadout(lastScanAt: number | null): string | null {
  if (lastScanAt === null) return null
  const minutes = Math.floor((Date.now() - lastScanAt) / 60_000)
  return minutes < 1 ? 'scanned just now' : `scanned ${minutes} min ago`
}

export default function Header({
  view,
  onSelectView,
  ratesAsOf,
  filesScanned,
  onRescan,
  rescanning,
  lastScanAt,
  mode,
  onToggleTheme,
  onOpenRail,
}: HeaderProps) {
  const [, setTick] = useState(0)
  useEffect(() => {
    const interval = setInterval(() => setTick((n) => n + 1), 30_000)
    return () => clearInterval(interval)
  }, [])
  const readout = scanReadout(lastScanAt)

  return (
    <header className="app-header">
      <div style={{ display: 'flex', alignItems: 'center', gap: 10, flex: 'none' }}>
        <div className="app-logo">
          <Logo />
        </div>
        <div>
          <div
            style={{
              fontFamily: 'var(--font-display)',
              fontWeight: 700,
              fontSize: 13.5,
              lineHeight: 1.1,
              color: 'var(--fg-strong)',
            }}
          >
            ai-usage-cost
          </div>
          <div className="lbl" style={{ fontSize: 9, marginTop: 2 }}>
            local · read only
          </div>
        </div>
      </div>

      <nav
        className="hdr-nav"
        role="tablist"
        style={{ display: 'flex', alignSelf: 'stretch', gap: 0, flex: '0 1 auto', minWidth: 0, overflowX: 'auto' }}
      >
        {TABS.map((tab) => (
          <button
            key={tab.id}
            type="button"
            role="tab"
            aria-selected={view === tab.id}
            className={'tab-btn' + (view === tab.id ? ' is-active' : '')}
            onClick={() => onSelectView(tab.id)}
            style={{ minHeight: 0, height: 52, padding: '0 16px', fontSize: 12, letterSpacing: '0.04em' }}
          >
            {tab.label}
          </button>
        ))}
      </nav>

      <div
        style={{
          marginLeft: 'auto',
          display: 'flex',
          alignItems: 'center',
          gap: 10,
          flex: '0 1 auto',
          minWidth: 0,
          justifyContent: 'flex-end',
        }}
      >
        <button
          type="button"
          className="btn-ghost"
          data-rail-toggle
          onClick={onOpenRail}
          aria-label="Open filters"
          style={{ flex: 'none', height: 32, minHeight: 32, padding: '0 10px', fontSize: 11.5 }}
        >
          Filters
        </button>
        <span
          className="num hdr-meta"
          style={{ fontSize: 10.5, color: 'var(--fg-faint)', whiteSpace: 'nowrap', flex: 'none' }}
        >
          rates {ratesAsOf} · {filesScanned} log files
        </span>
        {readout && (
          <span
            className="num"
            style={{
              fontSize: 10.5,
              color: 'var(--fg-faint)',
              whiteSpace: 'nowrap',
              flex: 'none',
              opacity: rescanning ? 0.5 : 1,
            }}
          >
            {readout}
          </span>
        )}
        <button
          type="button"
          className="btn-ghost"
          onClick={onRescan}
          style={{ flex: 'none', height: 32, minHeight: 32, padding: '0 12px', fontSize: 11.5, whiteSpace: 'nowrap' }}
        >
          {rescanning ? 'Scanning…' : 'Rescan logs'}
        </button>
        <button
          type="button"
          className={'theme-toggle' + (mode === 'dark' ? ' is-dark' : '')}
          onClick={onToggleTheme}
          aria-label="Switch theme"
          style={{ flex: 'none' }}
        >
          <span className="theme-toggle__icon theme-toggle__icon--sun">☀</span>
          <span className="theme-toggle__icon theme-toggle__icon--moon">☾</span>
          <span className="theme-toggle__knob" />
        </button>
      </div>
    </header>
  )
}
