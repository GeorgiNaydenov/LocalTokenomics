import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App'
import { TooltipProvider } from '@/components/ui/tooltip'
import '@/design-system/theme.css'

createRoot(document.getElementById('root') as HTMLElement).render(
  <StrictMode>
    <TooltipProvider delayDuration={200}>
      <App />
    </TooltipProvider>
  </StrictMode>,
)
