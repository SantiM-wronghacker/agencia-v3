# Demos de Agencia v3

Demos ejecutables para mostrar los 4 servicios vendibles del sistema.
Cada demo corre un pipeline completo de IA con Ollama local — sin APIs externas.

---

## Requisitos

1. **Python 3.12+** con dependencias instaladas:
   ```bash
   pip install -r requirements.txt
   ```

2. **Ollama corriendo**:
   ```bash
   ollama serve
   ```

3. **Modelo instalado** (recomendado: llama3:8b, ~4 GB):
   ```bash
   ollama pull llama3:8b
   ```
   Los demos detectan automáticamente el modelo disponible.
   También funcionan con `gpt-oss:20b` o `mistral:7b`.

---

## Ejecutar demos

### Todos los demos en secuencia
```bash
python demos/run_all_demos.py
```

### Demo individual
```bash
python demos/run_all_demos.py content    # Content Pipeline
python demos/run_all_demos.py business   # Business Analysis
python demos/run_all_demos.py legal      # Legal Review
python demos/run_all_demos.py ops        # Ops Automation
```

### Directamente
```bash
python demos/demo_content_pipeline.py
python demos/demo_business_analysis.py
python demos/demo_legal_review.py
python demos/demo_ops_automation.py
```

---

## Qué muestra cada demo

### 1. Content Pipeline — `demo_content_pipeline.py`
**Servicio**: Generación de contenido SEO completo a partir de un tema.

**Pipeline**:
- **Researcher** — Investiga el tema y extrae puntos clave
- **Writer** — Redacta el artículo completo
- **SEO Optimizer** — Optimiza keywords y estructura
- **Reviewer** — Revisa y pule la versión final

**Casos de uso reales**:
- Agencias de marketing que producen 10-50 artículos/semana
- E-commerce con catálogos de productos
- Blogs corporativos con equipo editorial reducido

---

### 2. Business Analysis — `demo_business_analysis.py`
**Servicio**: Análisis empresarial completo con estrategia y proyecciones.

**Pipeline**:
- **Data Analyst** — Analiza los datos y métricas del negocio
- **Strategy Director** — Propone estrategia de recuperación/crecimiento
- **Finance Director** — Calcula proyecciones financieras y ROI
- **Reporter** — Consolida todo en reporte ejecutivo

**Casos de uso reales**:
- Diagnóstico de empresas antes de invertir o escalar
- Análisis mensual de KPIs para directivos
- Consultoría estratégica para PyMEs

---

### 3. Legal Review — `demo_legal_review.py`
**Servicio**: Revisión jurídica de contratos con análisis de riesgos.

**Pipeline**:
- **Legal Analyst** — Identifica cláusulas problemáticas
- **Compliance Checker** — Verifica cumplimiento normativo
- **Risk Assessor** — Evalúa riesgos financieros y legales
- **Summarizer** — Produce dictamen ejecutivo

**Casos de uso reales**:
- Despachos legales que revisan contratos en volumen
- Startups y empresas sin área legal interna
- Due diligence antes de firmar acuerdos importantes

---

### 4. Ops Automation — `demo_ops_automation.py`
**Servicio**: Diagnóstico y optimización de procesos con plan de implementación.

**Pipeline**:
- **Process Mapper** — Documenta y analiza el proceso actual
- **Optimizer** — Identifica cuellos de botella y propone mejoras
- **Implementation Planner** — Crea plan de implementación paso a paso

**Casos de uso reales**:
- Empresas con procesos manuales que quieren automatizar
- Onboarding de clientes, gestión de pedidos, facturación
- Cualquier proceso con más de 5 pasos y varios equipos involucrados

---

## Para mostrar a un cliente

### Guión de presentación

**Antes de correr el demo:**
> "Voy a mostrarte cómo el sistema analiza [el caso de tu industria].
> Estás viendo IA corriendo localmente en tu computadora — tus datos nunca
> salen de tu red."

**Mientras corre el pipeline:**
> "Cada paso es un agente especializado. El Researcher hace lo que haría
> un analista junior en 2 horas. El Writer produce el borrador en segundos.
> El SEO Optimizer y el Reviewer lo dejan listo para publicar."

**Al terminar:**
> "Esto que acabas de ver tomó [X] segundos. Un equipo humano tardaría
> 2-4 horas. El sistema corre en tu servidor — sin costos de API, sin
> límites de uso, sin datos en la nube."

### Puntos de valor a enfatizar
1. **100% local** — los datos del cliente nunca salen de su infraestructura
2. **Sin costo por uso** — una vez instalado, es tuyo
3. **Personalizable** — los templates se ajustan a tu industria y tono
4. **Escalable** — el mismo sistema sirve para 10 o 10,000 tareas/día
5. **Auditable** — cada step queda registrado en la base de datos local

---

## Resolución de problemas

**Ollama no responde:**
```bash
# Verificar que está corriendo
curl http://localhost:11434/api/tags

# Si no está corriendo
ollama serve
```

**Modelo no disponible:**
```bash
# Ver modelos instalados
ollama list

# Instalar modelo recomendado
ollama pull llama3:8b
```

**El demo es lento:**
- Normal en primera ejecución (modelo se carga en RAM)
- Segunda ejecución es más rápida (~30-50% menos tiempo)
- Con GPU: 5-10x más rápido (instala la versión GPU de Ollama)

**Error de Python:**
```bash
# Asegúrate de estar en la raíz del proyecto
cd /ruta/a/agencia-v3
python demos/run_all_demos.py
```
