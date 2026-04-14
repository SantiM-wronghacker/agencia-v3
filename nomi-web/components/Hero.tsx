'use client'

export default function Hero() {
  const scroll = (id: string) => {
    const el = document.getElementById(id)
    el?.scrollIntoView({ behavior: 'smooth' })
  }

  return (
    <section className="pt-32 pb-20 px-6">
      <div className="max-w-3xl mx-auto text-center">
        {/* Tag */}
        <div className="inline-block mb-6 px-4 py-2 bg-white/40 border border-nomi-border rounded-full">
          <p className="text-sm text-nomi-secondary">Automatización para tu negocio</p>
        </div>

        {/* Headline */}
        <h1 className="text-4xl md:text-6xl font-600 mb-6 leading-tight">
          El trabajo no para. <span className="gradient-text">Aunque tú sí.</span>
        </h1>

        {/* Subtitle */}
        <p className="text-lg md:text-xl text-nomi-secondary mb-12 max-w-2xl mx-auto">
          Nomi le pone nombre a las cosas que antes no tenías tiempo de hacer.
        </p>

        {/* CTA Buttons */}
        <div className="flex flex-col md:flex-row gap-4 justify-center">
          <button
            onClick={() => scroll('precios')}
            className="px-8 py-3 bg-nomi-accent text-white rounded-lg font-500 hover:brightness-90"
          >
            Empezar ahora
          </button>
          <button
            onClick={() => scroll('que-es')}
            className="px-8 py-3 border border-nomi-border rounded-lg font-500 hover:bg-white/30"
          >
            Conocer más
          </button>
        </div>
      </div>
    </section>
  )
}
