'use client'

import { useState } from 'react'
import { submitLead } from '@/lib/api'

interface ContactFormProps {
  giro: string
  plan: string
  agents: string[]
  needsDetails: boolean
  precioEstimado?: number
}

export default function ContactForm({ giro, plan, agents, needsDetails, precioEstimado }: ContactFormProps) {
  const [formData, setFormData] = useState({
    nombre: '',
    correo: '',
    necesidades: '',
  })
  const [submitted, setSubmitted] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      await submitLead({
        nombre: formData.nombre,
        email: formData.correo,
        mensaje: formData.necesidades,
        plan,
        agentes: agents,
        precio_estimado: precioEstimado,
      })
      setSubmitted(true)
      setTimeout(() => {
        setSubmitted(false)
        setFormData({ nombre: '', correo: '', necesidades: '' })
      }, 5000)
    } catch (err) {
      console.error(err)
      setError('Hubo un problema al enviar. Intenta de nuevo.')
    } finally {
      setLoading(false)
    }
  }

  if (submitted) {
    return (
      <div className="bg-nomi-accent/10 border border-nomi-accent rounded-lg p-6 text-center">
        <div className="text-lg font-600 text-nomi-accent mb-2">✓ Cotización enviada</div>
        <p className="text-nomi-secondary">
          En las próximas horas recibirás tu cotización en {formData.correo}
        </p>
      </div>
    )
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block text-sm font-500 mb-2">Tu nombre</label>
        <input
          type="text"
          name="nombre"
          value={formData.nombre}
          onChange={handleChange}
          required
          className="w-full px-4 py-2 bg-white/60 border border-nomi-border rounded-lg focus:outline-none focus:border-nomi-accent"
          placeholder="Juan Pérez"
        />
      </div>

      <div>
        <label className="block text-sm font-500 mb-2">Correo electrónico</label>
        <input
          type="email"
          name="correo"
          value={formData.correo}
          onChange={handleChange}
          required
          className="w-full px-4 py-2 bg-white/60 border border-nomi-border rounded-lg focus:outline-none focus:border-nomi-accent"
          placeholder="tu@email.com"
        />
      </div>

      {needsDetails && (
        <div>
          <label className="block text-sm font-500 mb-2">
            ¿Qué necesitas automatizar?
          </label>
          <textarea
            name="necesidades"
            value={formData.necesidades}
            onChange={handleChange}
            className="w-full px-4 py-2 bg-white/60 border border-nomi-border rounded-lg focus:outline-none focus:border-nomi-accent resize-none"
            rows={3}
            placeholder="Cuéntanos qué procesos quieres automatizar..."
          />
        </div>
      )}

      {error && (
        <div className="text-sm text-red-600">{error}</div>
      )}

      <button
        type="submit"
        disabled={loading}
        className="w-full px-6 py-3 bg-nomi-accent text-white rounded-lg font-500 hover:brightness-90 disabled:opacity-60"
      >
        {loading ? 'Enviando...' : 'Solicitar cotización'}
      </button>
    </form>
  )
}
