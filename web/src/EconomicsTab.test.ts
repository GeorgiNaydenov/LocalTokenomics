import { describe, expect, it } from 'vitest'
import type { Capabilities } from './api'
import { rateUnavailableHint } from './EconomicsTab'

function capabilities(overrides: Partial<Capabilities> = {}): Capabilities {
  return {
    trace: 'measured',
    tokens: 'measured',
    cost: 'measured',
    context: 'measured',
    latency: 'measured',
    ...overrides,
  }
}

describe('rateUnavailableHint', () => {
  it('names the missing timing capability instead of claiming no source anywhere logs it', () => {
    expect(rateUnavailableHint(capabilities({ latency: 'unavailable' }))).toContain('no timing')
  })

  it('names the missing token capability when latency is fine but tokens are not', () => {
    expect(rateUnavailableHint(capabilities({ tokens: 'unavailable' }))).toContain('no token counts')
  })

  it('falls back to a generic reason when both capabilities are present but this row lacks one', () => {
    expect(rateUnavailableHint(capabilities())).toContain('this row does not have')
  })

  it('falls back to a generic reason when capability data was not supplied', () => {
    expect(rateUnavailableHint(null)).not.toContain('No source')
  })
})
