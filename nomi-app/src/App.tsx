import { useState, useEffect } from 'react'
import Login from './screens/Login'
import Dashboard from './screens/Dashboard'
import Suspended from './screens/Suspended'
import { loadSession, clearSession, Session } from './lib/store'
import { startHeartbeat, stopHeartbeat } from './lib/heartbeat'
import { validateLicense } from './lib/api'

type AppScreen = 'loading' | 'login' | 'dashboard' | 'suspended'

export default function App() {
  const [screen, setScreen] = useState<AppScreen>('loading')
  const [session, setSession] = useState<Session | null>(null)
  const [connected, setConnected] = useState(true)

  useEffect(() => {
    const stored = loadSession()
    if (!stored) {
      setScreen('login')
      return
    }

    // Valida la licencia guardada al arrancar
    validateLicense(stored.licenseKey)
      .then((res) => {
        if (res.status === 'blocked' || !res.valid) {
          clearSession()
          setScreen('suspended')
          return
        }
        // Actualiza agentes/plan en caso de que hayan cambiado
        const updatedSession = {
          ...stored,
          plan: res.plan || stored.plan,
          agentes: res.agentes || stored.agentes,
          clientName: res.client_name || stored.clientName,
        }
        setSession(updatedSession)
        setScreen('dashboard')
        setConnected(true)
        startHeartbeat(() => setScreen('suspended'))
      })
      .catch(() => {
        // Sin conexión — carga desde cache
        setSession(stored)
        setScreen('dashboard')
        setConnected(false)
        startHeartbeat(() => setScreen('suspended'))
      })
  }, [])

  const handleLoginSuccess = () => {
    const stored = loadSession()
    if (!stored) return
    setSession(stored)
    setScreen('dashboard')
    setConnected(true)
    startHeartbeat(() => {
      stopHeartbeat()
      setScreen('suspended')
    })
  }

  const handleSuspended = () => {
    stopHeartbeat()
    clearSession()
    setScreen('suspended')
  }

  if (screen === 'loading') {
    return (
      <div className="min-h-screen bg-nomi-bg flex items-center justify-center">
        <div className="text-nomi-secondary text-sm">Iniciando...</div>
      </div>
    )
  }

  if (screen === 'login') {
    return <Login onSuccess={handleLoginSuccess} onSuspended={handleSuspended} />
  }

  if (screen === 'suspended') {
    return <Suspended />
  }

  if (screen === 'dashboard' && session) {
    return (
      <Dashboard
        session={session}
        connected={connected}
        onSuspended={handleSuspended}
      />
    )
  }

  return <Login onSuccess={handleLoginSuccess} onSuspended={handleSuspended} />
}
