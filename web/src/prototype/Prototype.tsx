import { useState } from 'react'
import { ActivityIcon, MoonIcon, RefreshCwIcon, SlidersHorizontalIcon, SunIcon } from 'lucide-react'

import { Button } from '@/components/ui/button'
import { Separator } from '@/components/ui/separator'
import { Toaster } from '@/components/ui/sonner'
import { TooltipProvider } from '@/components/ui/tooltip'
import { cn } from '@/design-system/cn'
import { useTheme } from '@/theme'
import { Gallery } from './Gallery'
import { SCREEN_LABELS, Screens, type ScreenId } from './Screens'
import { TOTALS } from './data'

type Tab = ScreenId | 'gallery'

const TABS: Tab[] = ['overview', 'sessions', 'sources', 'pricing', 'gallery']

const TAB_LABELS: Record<Tab, string> = { ...SCREEN_LABELS, gallery: 'Design system' }

export default function Prototype() {
  const [mode, toggleTheme] = useTheme()
  const [tab, setTab] = useState<Tab>('overview')
  const [railOpen, setRailOpen] = useState(false)
  const [scanning, setScanning] = useState(false)

  const rescan = () => {
    setScanning(true)
    setTimeout(() => setScanning(false), 900)
  }

  return (
    <TooltipProvider delayDuration={200}>
      <div className="flex min-h-svh flex-col bg-background text-foreground">
        <header className="sticky top-0 z-40 flex flex-wrap items-center gap-4 border-b bg-card px-4 py-2.5">
          <div className="flex items-center gap-2.5">
            <span className="grid size-7 place-items-center rounded-md bg-primary text-primary-foreground">
              <ActivityIcon className="size-4" />
            </span>
            <div className="leading-tight">
              <p className="text-sm font-semibold tracking-[-0.01em]">ai-usage-cost</p>
              <p className="text-[11px] uppercase tracking-[0.08em] text-muted-foreground">
                local · read only
              </p>
            </div>
          </div>

          <Separator orientation="vertical" className="h-6" />

          <nav className="flex flex-wrap items-center gap-0.5" aria-label="Sections">
            {TABS.map((item) => (
              <button
                key={item}
                type="button"
                onClick={() => setTab(item)}
                aria-current={tab === item ? 'page' : undefined}
                className={cn(
                  'rounded-md px-3 py-1.5 text-sm font-medium transition-colors',
                  tab === item
                    ? 'bg-primary-subtle text-primary'
                    : 'text-muted-foreground hover:bg-accent hover:text-foreground',
                  item === 'gallery' && 'ml-2',
                )}
              >
                {TAB_LABELS[item]}
              </button>
            ))}
          </nav>

          <div className="ml-auto flex items-center gap-2">
            {tab !== 'gallery' ? (
              <Button
                variant="outline"
                size="sm"
                className="lg:hidden"
                onClick={() => setRailOpen(true)}
              >
                <SlidersHorizontalIcon /> Filters
              </Button>
            ) : null}
            <span className="tabular hidden text-[11px] text-muted-foreground xl:inline">
              rates {TOTALS.ratesAsOf} · {TOTALS.files} log files · scanned 2 min ago
            </span>
            <Button variant="outline" size="sm" onClick={rescan} disabled={scanning}>
              <RefreshCwIcon className={scanning ? 'animate-spin' : undefined} />
              {scanning ? 'Scanning…' : 'Rescan logs'}
            </Button>
            <Button
              variant="ghost"
              size="icon"
              onClick={toggleTheme}
              aria-label={mode === 'dark' ? 'Switch to light theme' : 'Switch to dark theme'}
            >
              {mode === 'dark' ? <SunIcon /> : <MoonIcon />}
            </Button>
          </div>
        </header>

        {tab === 'gallery' ? (
          <Gallery />
        ) : (
          <Screens
            screen={tab}
            onSelectScreen={setTab}
            railOpen={railOpen}
            onRailOpenChange={setRailOpen}
          />
        )}
      </div>
      <Toaster position="bottom-right" />
    </TooltipProvider>
  )
}
