import { useEffect, useState } from 'react'
import { MoonIcon, SunIcon } from 'lucide-react'
import type { Meta, View } from './api'
import type { ThemeMode } from './theme'
import { StatLabel } from '@/components/stat'
import { Button } from '@/components/ui/button'
import { cn } from '@/design-system/cn'

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
  return <img src="./logo-mark.png" alt="" width={20} height={20} className="size-5" />
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
    <header className="sticky top-0 z-40 flex min-h-13 flex-wrap items-center gap-5 border-b bg-card px-4">
      <div className="flex flex-none items-center gap-2.5">
        <div className="grid size-7 flex-none place-items-center rounded-md border">
          <Logo />
        </div>
        <div>
          <div className="text-[13.5px] font-bold leading-tight">LocalTokenomics</div>
          <StatLabel className="mt-0.5 text-[9px]">Token Insights at your fingertips</StatLabel>
        </div>
      </div>

      <nav
        role="tablist"
        className="scroll-thin order-3 flex w-full min-w-0 basis-full self-stretch overflow-x-auto border-t sm:order-none sm:w-auto sm:flex-initial sm:basis-auto sm:border-t-0"
      >
        {TABS.map((tab) => (
          <button
            key={tab.id}
            type="button"
            role="tab"
            aria-selected={view === tab.id}
            onClick={() => onSelectView(tab.id)}
            className={cn(
              'h-13 whitespace-nowrap border-b-2 px-4 text-xs tracking-[0.04em] transition-colors',
              view === tab.id
                ? 'border-b-primary font-medium text-foreground'
                : 'border-b-transparent text-muted-foreground hover:text-foreground',
            )}
          >
            {tab.label}
          </button>
        ))}
      </nav>

      <div className="ml-auto flex min-w-0 flex-none items-center justify-end gap-2.5">
        <Button variant="ghost" size="sm" onClick={onOpenRail} className="lg:hidden">
          Filters
        </Button>
        <span className="tabular hidden whitespace-nowrap text-[10.5px] text-muted-foreground xl:inline">
          rates as of {ratesAsOf}, {filesScanned} log files
        </span>
        {readout && (
          <span
            className={cn(
              'tabular whitespace-nowrap text-[10.5px] text-muted-foreground',
              rescanning && 'opacity-50',
            )}
          >
            {readout}
          </span>
        )}
        <Button variant="ghost" size="sm" onClick={onRescan} className="whitespace-nowrap">
          {rescanning ? 'Scanning…' : 'Rescan logs'}
        </Button>
        <Button variant="ghost" size="icon-sm" onClick={onToggleTheme} aria-label="Switch theme">
          {mode === 'dark' ? <MoonIcon /> : <SunIcon />}
        </Button>
      </div>
    </header>
  )
}
