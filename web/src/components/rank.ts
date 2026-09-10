import type { CostState, Provenance } from '@/api'

export const STATE_RANK: Record<CostState, number> = { priced: 0, free: 1, unpriced: 2, unavailable: 3 }

export const PROVENANCE_RANK: Record<Provenance, number> = {
  measured: 0,
  derived: 1,
  estimated: 2,
  inferred: 3,
  unavailable: 4,
}

export function worstState(states: CostState[]): CostState {
  return [...states].sort((a, b) => STATE_RANK[b] - STATE_RANK[a])[0] ?? 'unavailable'
}

export function worstProvenance(values: Provenance[]): Provenance {
  return [...values].sort((a, b) => PROVENANCE_RANK[b] - PROVENANCE_RANK[a])[0] ?? 'unavailable'
}
