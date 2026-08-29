import { useCallback, useEffect, useSyncExternalStore } from 'react'

export type ThemeMode = 'light' | 'dark'

const STORAGE_KEY = 'auc.theme'
const listeners = new Set<() => void>()

function systemMode(): ThemeMode {
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
}

function read(): ThemeMode {
  try {
    const stored = localStorage.getItem(STORAGE_KEY)
    if (stored === 'light' || stored === 'dark') return stored
  } catch {
    /* private mode: fall through to the system preference */
  }
  return systemMode()
}

let current: ThemeMode = typeof window === 'undefined' ? 'light' : read()

function apply(mode: ThemeMode) {
  document.documentElement.classList.toggle('dark', mode === 'dark')
  document.documentElement.style.colorScheme = mode
}

export function setTheme(mode: ThemeMode) {
  current = mode
  apply(mode)
  try {
    localStorage.setItem(STORAGE_KEY, mode)
  } catch {
    /* persistence is a convenience, not a requirement */
  }
  listeners.forEach((listener) => listener())
}

function subscribe(listener: () => void) {
  listeners.add(listener)
  return () => {
    listeners.delete(listener)
  }
}

export function useTheme(): [ThemeMode, () => void] {
  const mode = useSyncExternalStore(
    subscribe,
    () => current,
    () => 'light' as ThemeMode,
  )
  useEffect(() => {
    apply(mode)
  }, [mode])
  const toggle = useCallback(() => {
    setTheme(current === 'dark' ? 'light' : 'dark')
  }, [])
  return [mode, toggle]
}

/* ------------------------------------------------------------------ *
 * Chart palette.                                                      *
 * A validated eight-slot categorical order, stepped per theme.        *
 * Slots are handed out by a *stable* identity index (position in the  *
 * full model/tool list from /api/meta) so filtering never repaints a   *
 * surviving series.                                                    *
 * ------------------------------------------------------------------ */
const SERIES_LIGHT = [
  '#2a78d6',
  '#eb6834',
  '#1baf7a',
  '#eda100',
  '#e87ba4',
  '#008300',
  '#4a3aa7',
  '#e34948',
]

const SERIES_DARK = [
  '#3987e5',
  '#d95926',
  '#199e70',
  '#c98500',
  '#d55181',
  '#008300',
  '#9085e9',
  '#e66767',
]

const OTHER = '#898781'

export function seriesColor(index: number, mode: ThemeMode): string {
  const slots = mode === 'dark' ? SERIES_DARK : SERIES_LIGHT
  return index >= 0 && index < slots.length ? slots[index] : OTHER
}

export interface ChartInk {
  surface: string
  grid: string
  axis: string
  muted: string
  ink: string
  ink2: string
  meterFill: string
  meterTrack: string
}

export function chartInk(mode: ThemeMode): ChartInk {
  return mode === 'dark'
    ? {
        surface: '#1a1a19',
        grid: '#2c2c2a',
        axis: '#383835',
        muted: '#929189',
        ink: '#ffffff',
        ink2: '#c3c2b7',
        meterFill: '#3987e5',
        meterTrack: '#184f95',
      }
    : {
        surface: '#fcfcfb',
        grid: '#e1e0d9',
        axis: '#c3c2b7',
        muted: '#7b7a74',
        ink: '#0b0b0b',
        ink2: '#52514e',
        meterFill: '#2a78d6',
        meterTrack: '#b7d3f6',
      }
}

/** Token-mix components get the first four slots, in stack order. */
export const TOKEN_PARTS = [
  { key: 'uncached_input', label: 'Uncached input', slot: 0 },
  { key: 'cache_read', label: 'Cache read', slot: 1 },
  { key: 'cache_write', label: 'Cache write', slot: 2 },
  { key: 'output', label: 'Output', slot: 3 },
] as const

export type TokenPartKey = (typeof TOKEN_PARTS)[number]['key']
