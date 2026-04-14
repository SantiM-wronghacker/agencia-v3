import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './styles.css'

// Declaración del API expuesta por Electron preload
declare global {
  interface Window {
    electron?: {
      openExternal: (url: string) => void
      getVersion: () => Promise<string>
    }
  }
}

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
