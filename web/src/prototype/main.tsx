import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'

import '@/design-system/theme.css'
import Prototype from './Prototype'

createRoot(document.getElementById('root') as HTMLElement).render(
  <StrictMode>
    <Prototype />
  </StrictMode>,
)
