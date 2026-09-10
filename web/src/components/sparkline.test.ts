import { describe, expect, it } from 'vitest'
import { geometry } from './sparkline'

describe('geometry', () => {
  it('scales a series that peaks below 1 to the real max instead of flattening it', () => {
    const { y } = geometry([0, 0.35], 100, 26)
    expect(y(0.35) - y(0)).toBeCloseTo(-(26 - 4), 5)
  })

  it('keeps every y coordinate inside the viewBox height for a series with negative dips', () => {
    const values = [-3.2, 0.5, 4, -1]
    const { y } = geometry(values, 100, 26)
    for (const value of values) {
      expect(y(value)).toBeGreaterThanOrEqual(0)
      expect(y(value)).toBeLessThanOrEqual(26)
    }
  })

  it('falls back to a flat line without dividing by zero when every value is identical', () => {
    const { y } = geometry([2, 2, 2], 100, 26)
    expect(Number.isFinite(y(2))).toBe(true)
  })

  it('draws the highest value nearest the top of the box', () => {
    const { y } = geometry([1, 5, 3], 100, 26)
    expect(y(5)).toBeLessThan(y(1))
    expect(y(5)).toBeLessThan(y(3))
  })
})
