'use client'

export default function Footer() {
  const year = new Date().getFullYear()

  return (
    <footer className="border-t border-nomi-border mt-20">
      <div className="max-w-6xl mx-auto px-6 py-12">
        <div className="flex flex-col md:flex-row items-center justify-between gap-8">
          <div>
            <div className="mb-2">
              <img src="/logo/nomi-logo-horizontal-light.svg" alt="nomi" height={24} style={{ height: 24, width: 'auto' }} />
            </div>
            <p className="text-sm text-nomi-secondary">
              Automatización para tu negocio.
            </p>
          </div>

          <div className="text-sm text-nomi-secondary text-center md:text-right">
            <p>© {year} nomi. Todos los derechos reservados.</p>
            <p className="mt-2">
              Hecho con ❤️ para equipos que quieren crecer más rápido.
            </p>
          </div>
        </div>
      </div>
    </footer>
  )
}
