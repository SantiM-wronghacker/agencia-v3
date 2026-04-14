import { useState } from 'react'
import { validateLicense } from '../lib/api'
import { saveSession } from '../lib/store'

interface LoginProps {
  onSuccess: () => void
  onSuspended: () => void
}

export default function Login({ onSuccess, onSuspended }: LoginProps) {
  const [email, setEmail] = useState('')
  const [licenseKey, setLicenseKey] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!email || !licenseKey) return
    setError('')
    setLoading(true)

    try {
      const res = await validateLicense(licenseKey.trim())

      if (res.status === 'blocked') {
        onSuspended()
        return
      }

      if (!res.valid) {
        setError(res.message || 'Licencia inválida. Verifica tu clave e intenta de nuevo.')
        setLoading(false)
        return
      }

      saveSession({
        licenseKey: licenseKey.trim(),
        clientId: licenseKey.trim(), // El validate no regresa client_id, usamos key como ID temporal
        clientName: res.client_name || email,
        plan: res.plan || 'lite',
        agentes: res.agentes || [],
      })

      onSuccess()
    } catch {
      setError('No se pudo conectar con el servidor. Verifica tu conexión a internet.')
    } finally {
      setLoading(false)
    }
  }

  const openSupport = () => {
    const mailto = 'mailto:soporte@nomi.mx?subject=Problema con mi licencia'
    if (window.electron) {
      window.electron.openExternal(mailto)
    } else {
      window.open(mailto)
    }
  }

  return (
    <div className="min-h-screen bg-nomi-bg flex items-center justify-center px-6">
      <div
        className="w-full max-w-sm rounded-2xl p-10 border border-nomi-border"
        style={{ background: 'rgba(255,255,255,0.5)', backdropFilter: 'blur(8px)' }}
      >
        {/* Logo */}
        <div className="text-center mb-10">
          <h1 className="text-4xl font-semibold text-nomi-text">nomi</h1>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1.5">Correo electrónico</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full px-4 py-2.5 rounded-lg border border-nomi-border bg-white/60 focus:outline-none focus:border-nomi-accent text-sm"
              placeholder="tu@empresa.com"
              autoComplete="email"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1.5">Clave de licencia</label>
            <input
              type="text"
              value={licenseKey}
              onChange={(e) => setLicenseKey(e.target.value)}
              required
              className="w-full px-4 py-2.5 rounded-lg border border-nomi-border bg-white/60 focus:outline-none focus:border-nomi-accent text-sm font-mono"
              placeholder="XXXX-XXXX-XXXX"
              autoComplete="off"
              spellCheck={false}
            />
          </div>

          {error && (
            <div className="text-sm text-red-600 bg-red-50 px-3 py-2 rounded-lg">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full py-2.5 bg-nomi-accent text-white rounded-lg font-medium text-sm hover:brightness-90 disabled:opacity-60 disabled:cursor-not-allowed mt-2"
          >
            {loading ? 'Verificando...' : 'Entrar'}
          </button>
        </form>

        <div className="text-center mt-6">
          <button
            onClick={openSupport}
            className="text-xs text-nomi-secondary hover:text-nomi-accent"
          >
            ¿Problemas? Contacta soporte
          </button>
        </div>
      </div>
    </div>
  )
}
