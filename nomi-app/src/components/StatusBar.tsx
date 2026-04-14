import { loadLastHeartbeat } from '../lib/store'

interface StatusBarProps {
  plan: string
  connected: boolean
}

export default function StatusBar({ plan, connected }: StatusBarProps) {
  const lastHb = loadLastHeartbeat()
  const lastHbDisplay = lastHb
    ? new Date(lastHb).toLocaleString('es-MX', { dateStyle: 'short', timeStyle: 'short' })
    : 'Nunca'

  return (
    <div
      className="h-7 px-4 flex items-center gap-6 text-xs border-t border-nomi-border"
      style={{ background: 'rgba(255,255,255,0.3)' }}
    >
      <div className="flex items-center gap-1.5">
        <span
          className={`w-2 h-2 rounded-full ${connected ? 'bg-green-500' : 'bg-nomi-secondary'}`}
        />
        <span className="text-nomi-secondary">
          {connected ? 'Conectado' : 'Sin conexión'}
        </span>
      </div>
      <div className="text-nomi-secondary">
        Plan: <span className="font-medium text-nomi-text capitalize">{plan}</span>
      </div>
      <div className="text-nomi-secondary">
        Último heartbeat: <span className="font-medium text-nomi-text">{lastHbDisplay}</span>
      </div>
    </div>
  )
}
