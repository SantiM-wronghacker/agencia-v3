export default function Suspended() {
  const openSupport = () => {
    const mailto = 'mailto:soporte@nomi.mx?subject=Reactivar mi servicio nomi'
    if (window.electron) {
      window.electron.openExternal(mailto)
    } else {
      window.open(mailto)
    }
  }

  return (
    <div className="min-h-screen bg-nomi-bg flex items-center justify-center px-6">
      <div className="text-center max-w-sm">
        {/* Logo */}
        <div className="flex justify-center mb-12">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 106 32" style={{ height: 40, width: 'auto' }}>
            <rect width="32" height="32" rx="7" fill="#6aaad9"/>
            <text x="16" y="16" textAnchor="middle" dominantBaseline="central"
              fontFamily="'Helvetica Neue',Helvetica,Arial,sans-serif"
              fontSize="22" fontWeight="700" fill="white">n</text>
            <text x="44" y="16" dominantBaseline="central"
              fontFamily="'Helvetica Neue',Helvetica,Arial,sans-serif"
              fontSize="21" fontWeight="600" fill="#1a1f2e">nomi</text>
          </svg>
        </div>

        {/* Icono */}
        <div className="text-5xl mb-6">🔒</div>

        <h2 className="text-2xl font-semibold text-nomi-text mb-3">
          Tu servicio está suspendido.
        </h2>

        <p className="text-nomi-secondary mb-8">
          Contacta a tu asesor para reactivar tu acceso.
        </p>

        <button
          onClick={openSupport}
          className="px-8 py-2.5 bg-nomi-accent text-white rounded-lg font-medium text-sm hover:brightness-90"
        >
          Contactar soporte
        </button>
      </div>
    </div>
  )
}
