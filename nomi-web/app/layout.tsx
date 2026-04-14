import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'nomi — Automatización para tu negocio',
  description: 'Agentes de IA listos desde el primer día. Sin conocimientos técnicos. Funciona en tu equipo.',
  viewport: 'width=device-width, initial-scale=1',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="es">
      <body className="bg-nomi-bg text-nomi-text">
        {children}
      </body>
    </html>
  )
}
