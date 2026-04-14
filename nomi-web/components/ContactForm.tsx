'use client'

import { useState } from 'react'

interface ContactFormProps {
  giro: string
  plan: string
  agents: string[]
  needsDetails: boolean
}

export default function ContactForm({ giro, plan, agents, needsDetails }: ContactFormProps) {
  const [formData, setFormData] = useState({
    nombre: '',
    correo: '',
    necesidades: '',
  })
  const [submitted, setSubmitted] = useState(false)

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    })
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()

    const payload = {
      ...formData,
      giro,
      plan,
      agents,
      timestamp: new Date().toISOString(),
    }

    console.log('Cotización enviada:', payload)

    // Por ahora: guardar en localStorage o enviar a API
    // Después: POST a /api/cotizaciones o license-server

    setSubmitted(true)
    setTimeout(() => {
      setSubmitted(false)
      setFormData({ nombre: '', correo: '', necesidades: '' })
    }, 5000)
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

      <button
        type="submit"
        className="w-full px-6 py-3 bg-nomi-accent text-white rounded-lg font-500 hover:brightness-90"
      >
        Solicitar cotización
      </button>
    </form>
  )
}
