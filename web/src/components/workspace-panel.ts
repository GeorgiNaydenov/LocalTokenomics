import { useState } from 'react'

const WIDTH_KEY = 'auc.workspace.width'
const FULLSCREEN_KEY = 'auc.workspace.fullscreen'

export const MIN_WIDTH = 360
export const DEFAULT_WIDTH = 480
export const MAX_WIDTH = 900

export function clampWidth(width: number): number {
  const bound = typeof window === 'undefined' ? MAX_WIDTH : Math.min(MAX_WIDTH, window.innerWidth * 0.9)
  return Math.min(bound, Math.max(MIN_WIDTH, width))
}

function readWidth(): number {
  try {
    const raw = localStorage.getItem(WIDTH_KEY)
    const parsed = raw ? Number(raw) : NaN
    return Number.isFinite(parsed) ? clampWidth(parsed) : DEFAULT_WIDTH
  } catch {
    return DEFAULT_WIDTH
  }
}

function persistWidth(width: number) {
  try {
    localStorage.setItem(WIDTH_KEY, String(Math.round(width)))
  } catch {
    return
  }
}

function readFullscreen(): boolean {
  try {
    return localStorage.getItem(FULLSCREEN_KEY) === '1'
  } catch {
    return false
  }
}

function persistFullscreen(fullscreen: boolean) {
  try {
    localStorage.setItem(FULLSCREEN_KEY, fullscreen ? '1' : '0')
  } catch {
    return
  }
}

export function useWorkspacePanel(): {
  width: number
  setWidth: (width: number) => void
  fullscreen: boolean
  toggleFullscreen: () => void
} {
  const [width, setWidthState] = useState(readWidth)
  const [fullscreen, setFullscreen] = useState(readFullscreen)

  const setWidth = (next: number) => {
    const clamped = clampWidth(next)
    setWidthState(clamped)
    persistWidth(clamped)
  }

  const toggleFullscreen = () => {
    setFullscreen((current) => {
      const next = !current
      persistFullscreen(next)
      return next
    })
  }

  return { width, setWidth, fullscreen, toggleFullscreen }
}
