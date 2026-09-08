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
