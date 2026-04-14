import { sendHeartbeat } from './api'
import { loadSession, clearSession, saveLastHeartbeat } from './store'

const INTERVAL_MS = 24 * 60 * 60 * 1000 // 24 horas

let _timer: ReturnType<typeof setInterval> | null = null
let _onSuspended: (() => void) | null = null

export function startHeartbeat(onSuspended: () => void): void {
  _onSuspended = onSuspended

  // Heartbeat inmediato al arrancar
  doHeartbeat()

  // Luego cada 24h
  if (_timer) clearInterval(_timer)
  _timer = setInterval(doHeartbeat, INTERVAL_MS)
}

export function stopHeartbeat(): void {
  if (_timer) {
    clearInterval(_timer)
    _timer = null
  }
}

async function doHeartbeat(): Promise<void> {
  const session = loadSession()
  if (!session) return

  try {
    const res = await sendHeartbeat(session.clientId, session.licenseKey, session.plan)

    if (!res.active || res.status === 'blocked') {
      clearSession()
      stopHeartbeat()
      _onSuspended?.()
      return
    }

    saveLastHeartbeat(new Date().toISOString())
  } catch {
    // Sin conexión — no suspender inmediatamente; el grace period lo maneja el servidor
    console.warn('[heartbeat] Sin conexión al license server')
  }
}
