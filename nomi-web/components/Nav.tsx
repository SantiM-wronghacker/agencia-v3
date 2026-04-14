'use client'

import Link from 'next/link'
import { useState } from 'react'

export default function Nav() {
  const [mobileOpen, setMobileOpen] = useState(false)

  const scroll = (id: string) => {
    setMobileOpen(false)
    const el = document.getElementById(id)
    el?.scrollIntoView({ behavior: 'smooth' })
  }

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 backdrop-blur-md bg-nomi-bg/80 border-b border-nomi-border">
      <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
        {/* Logo */}
        <div>
          <img src="/logo/nomi-logo-horizontal-light.svg" alt="nomi" height={32} style={{ height: 32, width: 'auto' }} />
        </div>

        {/* Desktop Menu */}
        <div className="hidden md:flex items-center gap-8">
          <button
            onClick={() => scroll('que-es')}
            className="text-nomi-secondary hover:text-nomi-text text-sm"
          >
            Qué es
          </button>
          <button
            onClick={() => scroll('como-funciona')}
            className="text-nomi-secondary hover:text-nomi-text text-sm"
          >
            Cómo funciona
          </button>
          <button
            onClick={() => scroll('precios')}
            className="text-nomi-secondary hover:text-nomi-text text-sm"
          >
            Precios
          </button>
        </div>

        {/* CTA Button */}
        <div className="hidden md:block">
          <button
            onClick={() => scroll('precios')}
            className="px-6 py-2 bg-nomi-accent text-white rounded-lg text-sm font-500 hover:brightness-90"
          >
            Cotizar ahora
          </button>
        </div>

        {/* Mobile Menu Toggle */}
        <button
          onClick={() => setMobileOpen(!mobileOpen)}
          className="md:hidden p-2"
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <line x1="3" y1="6" x2="21" y2="6" />
            <line x1="3" y1="12" x2="21" y2="12" />
            <line x1="3" y1="18" x2="21" y2="18" />
          </svg>
        </button>

        {/* Mobile Menu */}
        {mobileOpen && (
          <div className="absolute top-full left-0 right-0 bg-nomi-bg border-b border-nomi-border md:hidden">
            <div className="flex flex-col gap-4 p-6">
              <button
                onClick={() => scroll('que-es')}
                className="text-left text-nomi-secondary hover:text-nomi-text"
              >
                Qué es
              </button>
              <button
                onClick={() => scroll('como-funciona')}
                className="text-left text-nomi-secondary hover:text-nomi-text"
              >
                Cómo funciona
              </button>
              <button
                onClick={() => scroll('precios')}
                className="text-left text-nomi-secondary hover:text-nomi-text"
              >
                Precios
              </button>
              <button
                onClick={() => scroll('precios')}
                className="w-full px-6 py-2 bg-nomi-accent text-white rounded-lg text-sm font-500 hover:brightness-90"
              >
                Cotizar ahora
              </button>
            </div>
          </div>
        )}
      </div>
    </nav>
  )
}
