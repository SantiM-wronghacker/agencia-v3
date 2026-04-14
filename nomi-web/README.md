# nomi — Website & Admin Panel

Website de ventas + panel administrativo para gestión de clientes de nomi.

## Stack

- **Framework**: Next.js 14 (App Router)
- **Estilos**: Tailwind CSS + CSS custom properties
- **Tipografía**: Outfit (Google Fonts)
- **Backend**: License Server (FastAPI en puerto 8080)

## Colores

- **Fondo**: #f2ede4 (crema cálido)
- **Texto principal**: #1a1f2e
- **Texto secundario**: #9aa0b0
- **Acento**: #6aaad9 (azul acero)
- **Bordes**: #ddd8ce

## Estructura

```
nomi-web/
├── app/
│   ├── layout.tsx          — Layout principal
│   ├── page.tsx            — Home / Landing page
│   ├── globals.css         — Estilos globales
│   └── admin/
│       └── page.tsx        — Panel administrativo
├── components/
│   ├── Nav.tsx             — Navegación
│   ├── Hero.tsx            — Sección hero
│   ├── Benefits.tsx        — Beneficios
│   ├── HowItWorks.tsx      — Cómo funciona
│   ├── Quoter.tsx          — Cotizador (3 pasos)
│   ├── ContactForm.tsx     — Formulario de contacto
│   └── Footer.tsx          — Pie de página
├── lib/
│   └── api.ts              — Funciones helper para API
├── package.json
├── tsconfig.json
├── tailwind.config.js
├── next.config.js
└── .gitignore
```

## Secciones Principales

### 1. Navegación
- Logo "nomi"
- Links (Qué es, Cómo funciona, Precios)
- Botón "Cotizar ahora"
- Responsive con menú mobile

### 2. Hero
- Tagline: "Automatización para tu negocio"
- Headline: "El trabajo no para. Aunque tú sí."
- Subtitle descriptivo
- 2 CTA buttons

### 3. Beneficios
- 3 tarjetas: Listo desde el primer día / Sin conocimientos técnicos / Funciona en tu equipo

### 4. Cómo Funciona
- 3 pasos numerados y visuales

### 5. Cotizador (3 pasos interactivos)

**Paso 1**: Giro de empresa (grid de chips)
- 11 opciones: Restaurante, Salud, Bienes raíces, Legal, Contabilidad, Marketing, Logística, Educación, Seguros, Comercio, Otro

**Paso 2**: Plan + Agentes
- 3 planes: Lite ($95/mes), Core ($227/mes + $742 setup), Prime ($475/mes + $1,755 setup)
- Agentes por tier (Lite/Core/Prime)
- Primeros 5 agentes del plan incluidos
- Agentes adicionales: +$9.50 (lite) / +$22.70 (core) / +$47.50 (prime) c/u

**Paso 3**: Resumen + Formulario
- Resumen de plan y agentes
- Nombre + Email
- Campo "¿Qué necesitas?" solo si ≤ 2 agentes
- Mensaje de confirmación

### 6. Footer
- Logo + copyright

## Panel Admin (`/admin`)

### Autenticación
- Password simple (hardcoded: `nomi2026`)
- Guarda sesión en localStorage

### Funcionalidades
- **Listar clientes**: nombre, plan, estado (badge), últimas acciones
- **Nuevo cliente**: form con nombre, email, plan, fecha vigencia
- **Gestión**:
  - Ver detalle
  - Bloquear / Desbloquear
  - Enviar link de descarga + licencia

### Conexión con License Server
- Endpoints: `GET /clients`, `POST /clients`, `POST /clients/{id}/block`, etc.
- Header: `X-Admin-Token: nomi2026`

## Desarrollo

### Instalar dependencias
```bash
npm install
```

### Correr en desarrollo
```bash
npm run dev
```
Abre [http://localhost:3000](http://localhost:3000)

### Build para producción
```bash
npm run build
npm start
```

## Variables de Entorno

Crear `.env.local` si es necesario:
```
NEXT_PUBLIC_LICENSE_SERVER_URL=http://localhost:8080
```

## Notas Técnicas

- **Sin animaciones complejas**: transiciones suaves de 0.15s en hover
- **Responsive**: mobile-first
- **Paleta**: CSS custom properties para facilitar cambios
- **TypeScript**: strict mode activado
- **Formulario de contacto**: por ahora hace console.log (después POST a backend)

## Próximos Pasos

- [ ] Conectar formulario de cotización a API backend
- [ ] Integración con pagos (Stripe)
- [ ] Email notifications
- [ ] Analytics y tracking
- [ ] Autenticación segura en admin
