# PROYECTO AGENCIA-V3 — DOCUMENTO MAESTRO

## Descripción
Sistema multi-agente para agencias de marketing y negocios en México.
Permite crear, configurar y desplegar agentes de IA especializados por vertical de negocio,
con licenciamiento por cliente, exportación de paquetes y automatización completa.

---

## ARQUITECTURA GENERAL

```
agencia-v3/
├── api/            — FastAPI: endpoints REST + WebSocket
├── core/           — BaseAgent, AgentGroup, LLM routing
├── groups/         — 25 grupos de agentes por caso de uso
├── tools/          — 65+ tools organizadas por dominio
├── config/         — Settings, habilidades
├── license-server/ — Servidor de licencias (FastAPI independiente)
├── export/         — Exportador de paquetes cliente
├── demos/          — 4 demos funcionales con Ollama
├── tests/          — 703 tests (unit, integration, e2e, performance)
├── scripts/        — Gates de calidad y utilitarios
└── dashboard/      — Frontend React (opcional)
```

### Stack
- **LLM**: Ollama local (mistral:7b) + Groq/Gemini/Mistral cloud (auto-routing)
- **API**: FastAPI + SQLite + WebSocket
- **Testing**: pytest, 85% cobertura mínima
- **Distribución**: paquetes ZIP exportables por cliente

---

## HISTORIAL DE FASES COMPLETADAS

✅ Fase 1  — Estructura base: core, config, API skeleton
✅ Fase 2  — LLM routing: Ollama + Groq + Gemini + Mistral
✅ Fase 3  — Tools sociales: Instagram, Facebook, LinkedIn, TikTok, Twitter
✅ Fase 4  — Tools email/CRM: SMTP, HubSpot, WhatsApp, Google Sheets, Calendar
✅ Fase 5  — Tools documentos: PDF, Word
✅ Fase 6  — Tools productividad: Notion, Slack, Trello
✅ Fase 7  — Tools contabilidad: SAT México, Excel, CSV
✅ Fase 8  — Grupos base: content_pipeline, business_analysis, legal_review, ops_automation
✅ Fase 9  — License server + exportador de paquetes cliente
✅ Fase 10 — Grupos ventas: sales_pipeline, quotation_generator, hr_onboarding
✅ Fase 11 — Grupos operaciones: accounting_report, ops_daily
✅ Fase 12 — Grupos contenido: blog_publisher, content_repurposer
✅ Fase 13 — Grupos marketing: social_media_manager, email_campaign
✅ Fase 14 — Dashboard React + WebSocket live
✅ Fase 15 — Demos funcionales con Ollama (4 demos)
✅ Fase 16.1 — Fixtures globales + cobertura crítica (276 tests, 80% cobertura)
✅ Fase 16.2 — Suite E2E con Ollama real (16 tests e2e, auto-skip si no disponible)
✅ Fase 16.3 — Tests de rendimiento + gates de calidad (459 tests, 91% cobertura)
✅ Fase 17  — Tools web y medios: WordPress, Webflow, Ghost, SD local, resize (458 tests)
✅ Fase 18  — Tools verticales: restaurantes, salud, real estate, logística, seguros, turismo (573 tests)
✅ Fase 19  — Tools inteligencia: web search, scraper, finanzas, BANXICO, educación, GitHub (641 tests)
✅ Fase 20  — Automatización: scheduler, webhooks, Zapier/Make/n8n, Drive, Dropbox (703 tests)

---

## GRUPOS DISPONIBLES (25)

| Grupo | Descripción |
|-------|-------------|
| content_pipeline | Generación y publicación de contenido |
| business_analysis | Análisis de negocio y reportes |
| legal_review | Revisión de documentos legales |
| ops_automation | Automatización de operaciones |
| social_media_manager | Gestión de redes sociales |
| email_campaign | Campañas de email marketing |
| sales_pipeline | Pipeline de ventas CRM |
| quotation_generator | Generador de cotizaciones |
| hr_onboarding | Onboarding de recursos humanos |
| accounting_report | Reportes contables y SAT |
| ops_daily | Operaciones diarias |
| blog_publisher | Publicación en blogs (WP/Ghost/Webflow) |
| content_repurposer | Reutilización de contenido multimedia |
| restaurant_manager | Gestión de restaurantes |
| health_assistant | Asistente de salud y citas |
| real_estate_agent | Agente inmobiliario |
| logistics_coordinator | Coordinación logística y envíos |
| insurance_advisor | Asesor de seguros |
| travel_planner | Planificador de viajes |
| market_intelligence | Inteligencia de mercado |
| financial_advisor | Asesor financiero |
| education_manager | Gestión educativa y cursos |
| daily_report | Reporte diario automatizado |
| social_autopilot | Piloto automático de redes |
| lead_nurturing | Nutrición de leads |

---

## TOOLS DISPONIBLES (65+)

### Social (5)
Instagram, Facebook, LinkedIn, TikTok, Twitter

### Email (2)
SMTP, Mailchimp

### CRM (4)
HubSpot, WhatsApp, Google Sheets, Google Calendar

### Documentos (2)
PDF Generator, Word Generator

### Productividad (3)
Notion, Slack, Trello

### Contabilidad (3)
SAT México, Excel Reports, CSV Processor

### Web (3)
WordPress, Webflow, Ghost

### Media (3)
Image Gen Local (SD), Image Gen API, Image Resize

### Verticales (10)
Reservations, Menu Manager, Appointment Scheduler, Patient Forms,
Property Listings, Portals, Shipping, Inventory, Policy Manager, Itinerary

### Inteligencia (9)
Web Search, Web Scraper, Market Data, Financial Calculator,
BANXICO, Quiz Generator, Learning Tracker, GitHub, System Monitor

### Automatización (6)
Scheduler, Trigger, Webhook Receiver, Zapier Webhook, Make Webhook, N8N Webhook

### Storage (2)
Google Drive, Dropbox

---

## ESTADO ACTUAL DEL SISTEMA

```
Estado final: 703 tests | 85% cobertura | 0 fallos | 65+ tools | 25 grupos | 19 dominios
```

### Comandos clave
```bash
# Arrancar API
python api/main.py

# Arrancar license server
cd license-server && python main.py

# Correr gates de calidad
./scripts/run_gates.sh

# Correr demos
python demos/run_all_demos.py

# Correr E2E
./scripts/run_e2e.sh

# Exportar paquete cliente
curl -X POST http://localhost:8001/export/{client_id} -H "Content-Type: application/json" -d '{...}'
```

---

## CONFIGURACIÓN INICIAL (cliente nuevo)

1. Copiar `.env.example` → `.env` y configurar claves
2. Arrancar `python api/main.py` (puerto 8001)
3. Arrancar `cd license-server && python main.py` (puerto 8080)
4. Exportar paquete: `POST /export/{client_id}`
5. Entregar ZIP al cliente con instrucciones

---

## PRÓXIMAS FASES OPCIONALES

- Fase 21 — Panel de administración web para gestión de clientes
- Fase 22 — Integración con Stripe para cobros automáticos
- Fase 23 — App móvil React Native
- Fase 24 — Marketplace de grupos/tools adicionales
