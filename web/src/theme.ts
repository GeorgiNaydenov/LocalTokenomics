import { useCallback, useEffect, useSyncExternalStore } from 'react'
import type { CostState, Provenance, SpanKind } from './api'

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
  } catch {}
  return systemMode()
}

let current: ThemeMode = typeof window === 'undefined' ? 'light' : read()

function apply(mode: ThemeMode) {
  document.documentElement.dataset.theme = mode
  document.documentElement.style.colorScheme = mode
}

export function setTheme(mode: ThemeMode) {
  current = mode
  apply(mode)
  try {
    localStorage.setItem(STORAGE_KEY, mode)
  } catch {}
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

export const SERIES: string[] = [
  'var(--accent)',
  'var(--bubble-c-1)',
  'var(--bubble-c-6)',
  'var(--bubble-c-3)',
  'var(--bubble-c-4)',
  'var(--bubble-c-9)',
  'var(--bubble-c-8)',
  'var(--bubble-c-5)',
]

export const STATE_COLOR: Record<CostState, string> = {
  priced: 'var(--accent)',
  free: 'var(--success)',
  unpriced: 'var(--bubble-c-3)',
  unavailable: 'var(--border-strong)',
}

export const STATE_BADGE: Record<CostState, string> = {
  priced: 'badge badge--accent',
  free: 'badge badge--free',
  unpriced: 'badge',
  unavailable: 'badge',
}

export const PROVENANCE_COLOR: Record<Provenance, string> = {
  measured: 'var(--accent)',
  derived: 'var(--bubble-c-1)',
  estimated: 'var(--bubble-c-3)',
  inferred: 'var(--bubble-c-4)',
  unavailable: 'var(--border-strong)',
}

export const PROVENANCE_BADGE: Record<Provenance, string> = {
  measured: 'badge badge--accent',
  derived: 'badge badge--new',
  estimated: 'badge',
  inferred: 'badge',
  unavailable: 'badge',
}

export const SPAN_KIND_GLYPH: Record<SpanKind, string> = {
  turn: '¶',
  user: '»',
  assistant: '«',
  reasoning: '~',
  model_call: '◆',
  tool_call: '▶',
  tool_result: '◀',
  retrieval: '◎',
  compaction: '⇥',
  error: '✕',
  subagent: '↳',
}

export interface TokenBucket {
  key: 'uncached_input' | 'cache_read' | 'cache_write' | 'output'
  label: string
  color: string
  mult: string
}

export const BUCKETS: TokenBucket[] = [
  { key: 'uncached_input', label: 'Uncached input', color: 'var(--bubble-c-6)', mult: '1x' },
  { key: 'cache_read', label: 'Cache read', color: 'var(--bubble-c-1)', mult: '0.1x' },
  { key: 'cache_write', label: 'Cache write', color: 'var(--bubble-c-3)', mult: '1.25x' },
  { key: 'output', label: 'Output', color: 'var(--accent)', mult: 'output rate' },
]
