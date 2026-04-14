'use client'

import { useState, useEffect } from 'react'

interface Client {
  id: string
  name: string
  email: string
  package_type: string
  status: string
  last_heartbeat?: string
  active: number
}

const ADMIN_PASSWORD = 'nomi2026'
const LICENSE_SERVER_URL = 'http://localhost:8080'

export default function AdminPage() {
  const [authenticated, setAuthenticated] = useState(false)
  const [password, setPassword] = useState('')
  const [clients, setClients] = useState<Client[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [showNewClientForm, setShowNewClientForm] = useState(false)
  const [newClient, setNewClient] = useState({
    name: '',
    email: '',
    package_type: 'lite',
    paid_until: '',
  })

  useEffect(() => {
    const stored = localStorage.getItem('nomi_admin_auth')
    if (stored === 'true') {
      setAuthenticated(true)
      loadClients()
    }
  }, [])

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault()
    if (password === ADMIN_PASSWORD) {
      setAuthenticated(true)
      localStorage.setItem('nomi_admin_auth', 'true')
      setPassword('')
      loadClients()
    } else {
      setError('Contraseña incorrecta')
    }
  }

  const loadClients = async () => {
    setLoading(true)
    try {
      const res = await fetch(`${LICENSE_SERVER_URL}/clients`, {
        headers: { 'X-Admin-Token': ADMIN_PASSWORD },
      })
      if (res.ok) {
        setClients(await res.json())
      }
    } catch (err) {
      setError('Error cargando clientes')
      console.error(err)
    }
    setLoading(false)
  }

  const handleCreateClient = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const res = await fetch(`${LICENSE_SERVER_URL}/clients`, {
        method: 'POST',
        headers: {
          'X-Admin-Token': ADMIN_PASSWORD,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newClient),
      })
      if (res.ok) {
        setNewClient({ name: '', email: '', package_type: 'lite', paid_until: '' })
        setShowNewClientForm(false)
        await loadClients()
      }
    } catch (err) {
      setError('Error creando cliente')
      console.error(err)
    }
  }

  const handleBlockClient = async (clientId: string) => {
    try {
      const res = await fetch(`${LICENSE_SERVER_URL}/clients/${clientId}/block`, {
        method: 'POST',
        headers: { 'X-Admin-Token': ADMIN_PASSWORD },
      })
      if (res.ok) {
        await loadClients()
      }
    } catch (err) {
      console.error(err)
    }
  }

  const handleUnblockClient = async (clientId: string) => {
    try {
      const res = await fetch(`${LICENSE_SERVER_URL}/clients/${clientId}/unblock`, {
        method: 'POST',
        headers: { 'X-Admin-Token': ADMIN_PASSWORD },
      })
      if (res.ok) {
        await loadClients()
      }
    } catch (err) {
      console.error(err)
    }
  }

  const handleSendLink = async (clientId: string) => {
    try {
      const res = await fetch(`${LICENSE_SERVER_URL}/clients/${clientId}/send-link`, {
        method: 'POST',
        headers: { 'X-Admin-Token': ADMIN_PASSWORD },
      })
      if (res.ok) {
        alert('Email enviado exitosamente')
      }
    } catch (err) {
      console.error(err)
      alert('Error enviando email')
    }
  }

  const handleLogout = () => {
    setAuthenticated(false)
    localStorage.removeItem('nomi_admin_auth')
    setClients([])
  }

  if (!authenticated) {
    return (
      <div className="min-h-screen bg-nomi-bg flex items-center justify-center px-6">
        <div className="glass rounded-2xl p-8 max-w-md w-full">
          <div className="flex justify-center mb-6">
            <img src="/logo/nomi-logo-horizontal-light.svg" alt="nomi" height={32} style={{ height: 32, width: 'auto' }} />
          </div>
          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <label className="block text-sm font-500 mb-2">Contraseña</label>
              <input
                type="password"
                value={password}
                onChange={e => setPassword(e.target.value)}
                className="w-full px-4 py-2 bg-white/60 border border-nomi-border rounded-lg focus:outline-none focus:border-nomi-accent"
                placeholder="Ingresa la contraseña"
              />
            </div>
            {error && <div className="text-sm text-red-600">{error}</div>}
            <button
              type="submit"
              className="w-full px-6 py-2 bg-nomi-accent text-white rounded-lg font-500 hover:brightness-90"
            >
              Acceder
            </button>
          </form>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-nomi-bg">
      <nav className="border-b border-nomi-border sticky top-0 bg-nomi-bg/80 backdrop-blur">
        <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
          <img src="/logo/nomi-logo-horizontal-light.svg" alt="nomi" height={32} style={{ height: 32, width: 'auto' }} />
          <button
            onClick={handleLogout}
            className="px-4 py-2 text-sm font-500 text-nomi-secondary hover:text-nomi-text"
          >
            Salir
          </button>
        </div>
      </nav>

      <div className="max-w-6xl mx-auto px-6 py-12">
        <div className="flex items-center justify-between mb-8">
          <h2 className="text-3xl font-600">Clientes</h2>
          <button
            onClick={() => setShowNewClientForm(!showNewClientForm)}
            className="px-6 py-2 bg-nomi-accent text-white rounded-lg font-500 hover:brightness-90"
          >
            + Nuevo cliente
          </button>
        </div>

        {error && (
          <div className="bg-red-100 border border-red-300 text-red-700 px-4 py-3 rounded-lg mb-6">
            {error}
          </div>
        )}

        {showNewClientForm && (
          <div className="glass rounded-2xl p-8 mb-8">
            <h3 className="text-2xl font-600 mb-6">Nuevo cliente</h3>
            <form onSubmit={handleCreateClient} className="space-y-4">
              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-500 mb-2">Nombre</label>
                  <input
                    type="text"
                    value={newClient.name}
                    onChange={e => setNewClient({ ...newClient, name: e.target.value })}
                    required
                    className="w-full px-4 py-2 bg-white/60 border border-nomi-border rounded-lg focus:outline-none focus:border-nomi-accent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-500 mb-2">Email</label>
                  <input
                    type="email"
                    value={newClient.email}
                    onChange={e => setNewClient({ ...newClient, email: e.target.value })}
                    required
                    className="w-full px-4 py-2 bg-white/60 border border-nomi-border rounded-lg focus:outline-none focus:border-nomi-accent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-500 mb-2">Plan</label>
                  <select
                    value={newClient.package_type}
                    onChange={e => setNewClient({ ...newClient, package_type: e.target.value })}
                    className="w-full px-4 py-2 bg-white/60 border border-nomi-border rounded-lg focus:outline-none focus:border-nomi-accent"
                  >
                    <option value="lite">Lite</option>
                    <option value="core">Core</option>
                    <option value="prime">Prime</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-500 mb-2">Vigencia (YYYY-MM-DD)</label>
                  <input
                    type="date"
                    value={newClient.paid_until}
                    onChange={e => setNewClient({ ...newClient, paid_until: e.target.value })}
                    required
                    className="w-full px-4 py-2 bg-white/60 border border-nomi-border rounded-lg focus:outline-none focus:border-nomi-accent"
                  />
                </div>
              </div>
              <div className="flex gap-4">
                <button
                  type="submit"
                  className="px-6 py-2 bg-nomi-accent text-white rounded-lg font-500 hover:brightness-90"
                >
                  Crear cliente
                </button>
                <button
                  type="button"
                  onClick={() => setShowNewClientForm(false)}
                  className="px-6 py-2 border border-nomi-border rounded-lg font-500 hover:bg-white/30"
                >
                  Cancelar
                </button>
              </div>
            </form>
          </div>
        )}

        {loading ? (
          <p className="text-center text-nomi-secondary">Cargando...</p>
        ) : (
          <div className="grid gap-4">
            {clients.map(client => (
              <div key={client.id} className="glass rounded-xl p-6">
                <div className="grid md:grid-cols-4 gap-4 items-center">
                  <div>
                    <div className="font-600">{client.name}</div>
                    <div className="text-sm text-nomi-secondary">{client.email}</div>
                  </div>
                  <div className="text-sm">
                    <span className="text-nomi-secondary">Plan:</span>{' '}
                    <span className="font-500">{client.package_type}</span>
                  </div>
                  <div className="text-sm">
                    <span
                      className={`px-3 py-1 rounded-full text-xs font-500 ${
                        client.status === 'active'
                          ? 'bg-green-100 text-green-700'
                          : 'bg-red-100 text-red-700'
                      }`}
                    >
                      {client.status}
                    </span>
                  </div>
                  <div className="flex gap-2">
                    <button
                      onClick={() =>
                        client.status === 'active'
                          ? handleBlockClient(client.id)
                          : handleUnblockClient(client.id)
                      }
                      className="px-3 py-1 text-sm rounded-lg border border-nomi-border hover:bg-white/30"
                    >
                      {client.status === 'active' ? 'Bloquear' : 'Desbloquear'}
                    </button>
                    <button
                      onClick={() => handleSendLink(client.id)}
                      className="px-3 py-1 text-sm rounded-lg bg-nomi-accent/20 text-nomi-accent hover:bg-nomi-accent/30"
                    >
                      Enviar link
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
