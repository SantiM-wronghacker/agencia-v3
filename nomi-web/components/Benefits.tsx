'use client'

export default function Benefits() {
  const benefits = [
    {
      title: 'Listo desde el primer día',
      description: 'No necesitas esperar a que alguien configure nada. Tu agencia funciona desde la primera hora.',
      icon: '⚡',
    },
    {
      title: 'Sin conocimientos técnicos',
      description: 'Nomi habla tu idioma. Configura y controla todo desde una interfaz intuitiva.',
      icon: '🎯',
    },
    {
      title: 'Funciona en tu equipo',
      description: 'Se integra con tus herramientas actuales. No necesitas cambiar tu forma de trabajar.',
      icon: '🤝',
    },
  ]

  return (
    <section id="que-es" className="section-padding max-w-6xl mx-auto">
      <div className="text-center mb-16">
        <h2 className="text-3xl md:text-5xl font-600 mb-4">Qué es nomi</h2>
        <p className="text-lg text-nomi-secondary max-w-2xl mx-auto">
          Una plataforma de agentes de IA diseñada para equipos que quieren automatizar sin complicaciones.
        </p>
      </div>

      <div className="grid md:grid-cols-3 gap-8">
        {benefits.map((benefit, i) => (
          <div key={i} className="glass p-8 rounded-2xl">
            <div className="text-4xl mb-4">{benefit.icon}</div>
            <h3 className="text-xl font-600 mb-3">{benefit.title}</h3>
            <p className="text-nomi-secondary text-sm leading-relaxed">
              {benefit.description}
            </p>
          </div>
        ))}
      </div>
    </section>
  )
}
