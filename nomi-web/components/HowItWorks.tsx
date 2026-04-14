'use client'

export default function HowItWorks() {
  const steps = [
    {
      number: '01',
      title: 'Elige tu plan',
      description: 'Lite, Core o Prime. Cada uno viene con los agentes que necesitas.',
    },
    {
      number: '02',
      title: 'Personaliza',
      description: 'Selecciona los agentes especializados para tu negocio.',
    },
    {
      number: '03',
      title: 'Disfruta',
      description: 'Tu agencia funciona. Tú te enfocas en lo que importa.',
    },
  ]

  return (
    <section id="como-funciona" className="section-padding max-w-6xl mx-auto">
      <div className="text-center mb-16">
        <h2 className="text-3xl md:text-5xl font-600 mb-4">Cómo funciona</h2>
        <p className="text-lg text-nomi-secondary max-w-2xl mx-auto">
          Tres pasos simples para tener tu agencia de IA corriendo.
        </p>
      </div>

      <div className="grid md:grid-cols-3 gap-8">
        {steps.map((step, i) => (
          <div key={i} className="relative">
            <div className="flex items-start gap-6">
              <div className="text-5xl font-600 text-nomi-accent opacity-20 flex-shrink-0">
                {step.number}
              </div>
              <div>
                <h3 className="text-xl font-600 mb-2">{step.title}</h3>
                <p className="text-nomi-secondary text-sm">
                  {step.description}
                </p>
              </div>
            </div>
            {i < steps.length - 1 && (
              <div className="hidden md:block absolute top-8 -right-4 w-8 h-0.5 bg-nomi-border" />
            )}
          </div>
        ))}
      </div>
    </section>
  )
}
