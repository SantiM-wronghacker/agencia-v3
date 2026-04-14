import type { Metadata, Viewport } from 'next'
import './globals.css'

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
}

export const metadata: Metadata = {
  title: 'Nomi — Automatización IA para tu negocio',
  description: 'El trabajo no para. Aunque tú sí. Nomi automatiza las tareas más repetitivas de tu operación.',
  openGraph: {
    title: 'Nomi — Automatización IA para tu negocio',
    description: 'El trabajo no para. Aunque tú sí. Nomi automatiza las tareas más repetitivas de tu operación.',
    type: 'website',
    url: 'https://nomi-mx.com',
    siteName: 'Nomi',
  },
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
