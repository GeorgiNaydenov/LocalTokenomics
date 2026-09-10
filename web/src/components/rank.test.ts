import { describe, expect, it } from 'vitest'
import { worstProvenance, worstState } from './rank'

describe('worstState', () => {
  it('picks unavailable over unpriced, free and priced', () => {
    expect(worstState(['priced', 'free', 'unpriced', 'unavailable'])).toBe('unavailable')
  })

  it('picks unpriced over free and priced', () => {
    expect(worstState(['priced', 'free', 'unpriced'])).toBe('unpriced')
  })

  it('returns unavailable for an empty list', () => {
    expect(worstState([])).toBe('unavailable')
  })

  it('is order-independent', () => {
    expect(worstState(['unpriced', 'free'])).toBe('unpriced')
    expect(worstState(['free', 'unpriced'])).toBe('unpriced')
  })
})

describe('worstProvenance', () => {
  it('picks unavailable as the worst', () => {
    expect(worstProvenance(['measured', 'derived', 'unavailable'])).toBe('unavailable')
  })

  it('picks measured as the best when nothing worse is present', () => {
    expect(worstProvenance(['measured', 'derived'])).toBe('derived')
  })

  it('returns unavailable for an empty list', () => {
    expect(worstProvenance([])).toBe('unavailable')
  })
})
