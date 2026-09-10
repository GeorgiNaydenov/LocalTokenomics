import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { describe, expect, it } from 'vitest'

import { MetricInfo } from './metric-info'

describe('MetricInfo', () => {
  it('opens on click and shows the simple content', () => {
    render(
      <MetricInfo content={{ kind: 'simple', text: 'A plain explanation.' }} ariaLabel="Explain X">
        <span>trigger</span>
      </MetricInfo>,
    )
    fireEvent.click(screen.getByRole('button', { name: 'Explain X' }))
    expect(screen.getByText('A plain explanation.')).toBeInTheDocument()
  })

  it('closes on a second click and does not return focus to the trigger', async () => {
    // Regression test for a real bug: Radix returns focus to the trigger by default when
    // popover content closes, and this trigger's onFocus reopens the popover for keyboard
    // users -- without onCloseAutoFocus prevented, every close immediately re-focuses the
    // trigger, which immediately reopens it, forever. This is the literal "close, refocus,
    // reopen" cycle a user would see as flicker.
    render(
      <MetricInfo content={{ kind: 'simple', text: 'A plain explanation.' }} ariaLabel="Explain X">
        <span>trigger</span>
      </MetricInfo>,
    )
    const trigger = screen.getByRole('button', { name: 'Explain X' })
    fireEvent.click(trigger)
    expect(screen.getByText('A plain explanation.')).toBeInTheDocument()

    fireEvent.click(trigger)
    await waitFor(() => {
      expect(screen.queryByText('A plain explanation.')).not.toBeInTheDocument()
    })
    // If onCloseAutoFocus were not prevented, Radix would move focus to the trigger here,
    // and this component's own onFocus handler would reopen it -- the content would still
    // be in the document a tick later.
    await new Promise((resolve) => setTimeout(resolve, 50))
    expect(screen.queryByText('A plain explanation.')).not.toBeInTheDocument()
  })

  it('renders the rich metric content with meaning, formula and computed value', () => {
    render(
      <MetricInfo
        content={{
          kind: 'metric',
          meaning: 'What this number means.',
          formula: 'a + b = c',
          computed: '1 + 2 = 3',
          caveats: 'A caveat.',
        }}
        ariaLabel="Explain Y"
      >
        <span>trigger</span>
      </MetricInfo>,
    )
    fireEvent.click(screen.getByRole('button', { name: 'Explain Y' }))
    expect(screen.getByText('What this number means.')).toBeInTheDocument()
    expect(screen.getByText('a + b = c')).toBeInTheDocument()
    expect(screen.getByText('1 + 2 = 3')).toBeInTheDocument()
    expect(screen.getByText('A caveat.')).toBeInTheDocument()
  })
})
