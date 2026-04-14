'use client'

import { useState } from 'react'
import ContactForm from './ContactForm'

type Plan = 'lite' | 'core' | 'prime'
type Giro = 'restaurante' | 'salud' | 'bienes-raices' | 'legal' | 'contabilidad' | 'marketing' | 'logistica' | 'educacion' | 'seguros' | 'comercio' | 'otro'

const GIROS = [
  'Restaurante', 'Salud', 'Bienes raíces', 'Legal', 'Contabilidad',
  'Marketing', 'Logística', 'Educación', 'Seguros', 'Comercio', 'Otro'
]

const PLANS = {
  lite: { name: 'Lite', price: 95, setup: 0 },
  core: { name: 'Core', price: 227, setup: 742 },
  prime: { name: 'Prime', price: 475, setup: 1755 },
}

const AGENT_PRICES = {
  lite: 9.5,
  core: 22.7,
  prime: 47.5,
}

const AGENTS_BY_TIER_AND_GIRO: Record<string, Record<string, string[]>> = {
  lite: {
    universal: ['Ops Daily', 'Lead Nurturing', 'Quotation Generator'],
    restaurante: ['Restaurant Manager'],
    salud: [],
    'bienes-raices': ['Real Estate Agent'],
    legal: [],
    contabilidad: [],
    marketing: [],
    logistica: [],
    educacion: [],
    seguros: ['Insurance Advisor'],
    comercio: [],
    otro: [],
  },
  core: {
    universal: ['Email Campaign', 'HR Onboarding', 'Sales Pipeline', 'Social Media Manager', 'Ops Automation'],
    restaurante: ['Content Repurposer'],
    salud: [],
    'bienes-raices': [],
    legal: [],
    contabilidad: [],
    marketing: ['Blog Publisher', 'Content Repurposer'],
    logistica: ['Logistics Coordinator'],
    educacion: ['Education Manager', 'Blog Publisher'],
    seguros: [],
    comercio: [],
    otro: [],
  },
  prime: {
    universal: ['Daily Report'],
    restaurante: ['Content Pipeline'],
    salud: ['Business Analysis', 'Legal Review'],
    'bienes-raices': ['Market Intelligence', 'Financial Advisor'],
    legal: ['Legal Review', 'Business Analysis', 'Market Intelligence'],
    contabilidad: ['Accounting Report', 'Financial Advisor', 'Business Analysis'],
    marketing: ['Content Pipeline', 'Social Autopilot', 'Market Intelligence'],
    logistica: ['Business Analysis', 'Travel Planner'],
    educacion: ['Content Pipeline'],
    seguros: ['Financial Advisor', 'Business Analysis'],
    comercio: ['Market Intelligence', 'Financial Advisor', 'Content Pipeline'],
    otro: [],
  },
}

export default function Quoter() {
  const [step, setStep] = useState(1)
  const [selectedGiro, setSelectedGiro] = useState<Giro | null>(null)
  const [selectedPlan, setSelectedPlan] = useState<Plan | null>(null)
  const [selectedAgents, setSelectedAgents] = useState<string[]>([])

  const getAvailableAgents = () => {
    if (!selectedGiro || !selectedPlan) return []

    const universal = AGENTS_BY_TIER_AND_GIRO[selectedPlan]?.universal || []
    const specialized = AGENTS_BY_TIER_AND_GIRO[selectedPlan]?.[selectedGiro.replace(' ', '-')] || []

    return [...universal, ...specialized]
  }

  const getIncludedCount = () => {
    const tier = selectedPlan
    if (!tier) return 0
    return Math.min(5, getAvailableAgents().length)
  }

  const calculatePrice = (): { monthly: number; setup: number; total: number } => {
    if (!selectedPlan) return { monthly: 0, setup: 0, total: 0 }

    const plan = PLANS[selectedPlan]
    let agentPrice = 0

    // Primeros 5 agentes del plan actual incluidos
    const included = getIncludedCount()
    const additional = Math.max(0, selectedAgents.length - included)

    if (additional > 0) {
      agentPrice = additional * AGENT_PRICES[selectedPlan]
    }

    const monthlyPrice = plan.price + agentPrice
    const setupPrice = plan.setup
    const totalFirstMonth = monthlyPrice + setupPrice

    return { monthly: monthlyPrice, setup: setupPrice, total: totalFirstMonth }
  }

  const handleAgentToggle = (agent: string) => {
    setSelectedAgents(prev =>
      prev.includes(agent) ? prev.filter(a => a !== agent) : [...prev, agent]
    )
  }

  const handleNextStep = () => {
    if (step < 3) setStep(step + 1)
  }

  const handlePrevStep = () => {
    if (step > 1) setStep(step - 1)
  }

  const pricing = calculatePrice()
  const included = getIncludedCount()

  return (
    <section id="precios" className="section-padding max-w-6xl mx-auto">
      <div className="text-center mb-16">
        <h2 className="text-3xl md:text-5xl font-600 mb-4">Cotizador</h2>
        <p className="text-lg text-nomi-secondary max-w-2xl mx-auto">
          Elige tu plan y agentes. Te diremos exactamente cuánto cuesta.
        </p>
      </div>

      <div className="glass rounded-2xl p-8 md:p-12">
        {/* PASO 1 — Giro */}
        {step === 1 && (
          <div>
            <h3 className="text-2xl font-600 mb-6">Paso 1: ¿Cuál es tu giro?</h3>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-8">
              {GIROS.map((giro, i) => (
                <button
                  key={i}
                  onClick={() => setSelectedGiro(giro.toLowerCase().replace(' ', '-') as Giro)}
                  className={`p-4 rounded-lg font-500 transition ${
                    selectedGiro === giro.toLowerCase().replace(' ', '-')
                      ? 'bg-nomi-accent text-white'
                      : 'bg-white/40 hover:bg-white/60'
                  }`}
                >
                  {giro}
                </button>
              ))}
            </div>
            <div className="flex justify-end">
              <button
                onClick={handleNextStep}
                disabled={!selectedGiro}
                className={`px-8 py-2 rounded-lg font-500 ${
                  selectedGiro
                    ? 'bg-nomi-accent text-white hover:brightness-90'
                    : 'bg-nomi-border text-nomi-secondary cursor-not-allowed'
                }`}
              >
                Siguiente
              </button>
            </div>
          </div>
        )}

        {/* PASO 2 — Plan + Agentes */}
        {step === 2 && (
          <div>
            <h3 className="text-2xl font-600 mb-6">Paso 2: Elige tu plan</h3>

            <div className="grid md:grid-cols-3 gap-6 mb-12">
              {(Object.entries(PLANS) as [Plan, typeof PLANS['lite']][]).map(([key, plan]) => (
                <button
                  key={key}
                  onClick={() => setSelectedPlan(key)}
                  className={`p-6 rounded-xl border-2 transition ${
                    selectedPlan === key
                      ? 'border-nomi-accent bg-nomi-accent/10'
                      : 'border-nomi-border hover:border-nomi-accent/50'
                  }`}
                >
                  <div className="text-lg font-600 mb-2">{plan.name}</div>
                  <div className="text-3xl font-600 text-nomi-accent">${plan.price}</div>
                  <div className="text-sm text-nomi-secondary">por mes</div>
                  {plan.setup > 0 && (
                    <div className="text-sm text-nomi-secondary mt-2">
                      ${plan.setup} implementación
                    </div>
                  )}
                </button>
              ))}
            </div>

            {selectedPlan && (
              <>
                <h3 className="text-xl font-600 mb-4">Agentes disponibles</h3>
                <div className="mb-8">
                  <div className="text-sm text-nomi-secondary mb-4">
                    Primeros {included} agentes incluidos. Adicionales: ${AGENT_PRICES[selectedPlan]}/mes cada uno.
                  </div>
                  <div className="grid md:grid-cols-2 gap-3">
                    {getAvailableAgents().map((agent, i) => (
                      <button
                        key={i}
                        onClick={() => handleAgentToggle(agent)}
                        className={`p-3 rounded-lg text-left transition ${
                          selectedAgents.includes(agent)
                            ? 'bg-nomi-accent/20 border border-nomi-accent'
                            : 'bg-white/40 border border-nomi-border hover:bg-white/60'
                        }`}
                      >
                        <div className="font-500">{agent}</div>
                        {i < included && <div className="text-xs text-nomi-secondary">Incluido</div>}
                      </button>
                    ))}
                  </div>
                </div>
              </>
            )}

            <div className="flex gap-4 justify-between">
              <button
                onClick={handlePrevStep}
                className="px-8 py-2 border border-nomi-border rounded-lg font-500 hover:bg-white/30"
              >
                Atrás
              </button>
              <button
                onClick={handleNextStep}
                disabled={!selectedPlan || selectedAgents.length === 0}
                className={`px-8 py-2 rounded-lg font-500 ${
                  selectedPlan && selectedAgents.length > 0
                    ? 'bg-nomi-accent text-white hover:brightness-90'
                    : 'bg-nomi-border text-nomi-secondary cursor-not-allowed'
                }`}
              >
                Siguiente
              </button>
            </div>
          </div>
        )}

        {/* PASO 3 — Resumen + Formulario */}
        {step === 3 && (
          <div>
            <h3 className="text-2xl font-600 mb-6">Paso 3: Tu cotización</h3>

            {/* Resumen */}
            <div className="bg-white/60 p-6 rounded-xl mb-8">
              <div className="grid md:grid-cols-2 gap-6 mb-6">
                <div>
                  <div className="text-sm text-nomi-secondary mb-1">Plan</div>
                  <div className="text-lg font-600">{selectedPlan && PLANS[selectedPlan].name}</div>
                </div>
                <div>
                  <div className="text-sm text-nomi-secondary mb-1">Agentes</div>
                  <div className="text-lg font-600">{selectedAgents.length}</div>
                </div>
              </div>

              <div className="border-t border-nomi-border pt-4">
                <div className="flex justify-between mb-2">
                  <span className="text-nomi-secondary">Cuota mensual</span>
                  <span className="font-600">${pricing.monthly.toFixed(2)}</span>
                </div>
                {pricing.setup > 0 && (
                  <div className="flex justify-between mb-4">
                    <span className="text-nomi-secondary">Implementación</span>
                    <span className="font-600">${pricing.setup}</span>
                  </div>
                )}
                <div className="flex justify-between text-lg font-600 border-t border-nomi-border pt-4">
                  <span>Total (primer mes)</span>
                  <span className="text-nomi-accent">${pricing.total.toFixed(2)}</span>
                </div>
              </div>
            </div>

            {/* Formulario de contacto */}
            <ContactForm
              giro={selectedGiro || ''}
              plan={selectedPlan || 'lite'}
              agents={selectedAgents}
              needsDetails={selectedAgents.length <= 2}
              precioEstimado={pricing.total}
            />

            <div className="flex gap-4 justify-between mt-8">
              <button
                onClick={handlePrevStep}
                className="px-8 py-2 border border-nomi-border rounded-lg font-500 hover:bg-white/30"
              >
                Atrás
              </button>
            </div>
          </div>
        )}

        {/* Indicador de progreso */}
        <div className="flex justify-center gap-2 mt-8">
          {[1, 2, 3].map(i => (
            <div
              key={i}
              className={`h-2 w-8 rounded-full transition ${
                i === step ? 'bg-nomi-accent' : i < step ? 'bg-nomi-accent/50' : 'bg-nomi-border'
              }`}
            />
          ))}
        </div>
      </div>
    </section>
  )
}
