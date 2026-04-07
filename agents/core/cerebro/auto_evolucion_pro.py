"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Agente de evolución pro que investiga y mejora la infraestructura de código
TECNOLOGÍA: Python, IA, Selenium, Celery, Redis
"""
import time
import os
import json
from datetime import datetime
from agencia.agents.cerebro.root_assistant import RootAssistant
from agencia.agents.cerebro.patcher_pro import aplicar_mejora, model_gemini

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def log_sistema(accion, detalle):
    ruta = "runs/state.json"
    with open(ruta, 'r', encoding='utf-8') as f:
        data = json.load(f)
    data['recent'].append({
        "role": "AUTONOMOUS_EVOLUTION",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "content": f"🚀 {accion}: {detalle}"
    })
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def bucle_infinito():
    ra = RootAssistant()
    print("🔥 AGENTE DE EVOLUCIÓN PRO ACTIVO - USANDO INTERNET Y AUTOPROGRAMACIÓN")
    
    temas_negocio = [
        "automatización de auditorías financieras con IA 2026",
        "agentes de IA que usan selenium para navegar",
        "seguridad en bases de datos sqlite para python", 
        "optimizacion de colas de tareas con celery y redis"
    ]

    while True:
        try:
            tema = random.choice(temas_negocio)
            print(f"\n🔎 Investigando en internet: {tema}")
            ra.investigar_tecnologia(tema)
            log_sistema("INVESTIGACIÓN", f"Se obtuvo conocimiento sobre {tema}")
            time.sleep(2)

            print("🛠️ Sintetizando conocimiento y mejorando infraestructura...")
            
            prompt_mejora = """
            Eres un Ingeniero de Confiabilidad de Sistemas (SRE) y Arquitecto Senior.
            Tu misión es optimizar la robustez de los archivos .py.

            REGLAS CRÍTICAS:
            1. ENFOQUE TÉCNICO: Céntrate en mejorar lógica, manejo de errores y velocidad.
            2. PROHIBICIÓN ESTÉTICA: No modifiques NADA dentro de la carpeta 'templates/' ni archivos .html. Ignora el diseño visual.
            3. PROTECCIÓN DE REDUNDANCIA: Bajo ninguna circunstancia borres la lista 'self.api_keys' ni la función 'rotar_api_key' en root_assistant.py. Es vital para la continuidad del negocio.
            4. MEJORA ESTRUCTURAL: Si encuentras código repetido o ineficiente en database.py o root_assistant.py, simplifícalo.

            Responde SOLO con la instrucción técnica para el patcher.
            """
            
            mision = model_gemini.generate_content(prompt_mejora).text.strip()
            
            if "dashboard" in mision.lower() and "lógica" not in mision.lower():
                archivo_destino = "database.py" 
            else:
                archivo_destino = "root_assistant.py"
            
            print(f"🛠️ Aplicando mejora estructural en: {archivo_destino}")
            aplicar_mejora(archivo_destino, mision)
            log_sistema("AUTOPROGRAMACIÓN", f"Se aplicó mejora en {archivo_destino}: {mision[:100]}...")

            print("✅ Ciclo exitoso. Esperando evolución...")
            time.sleep(30) 
            
        except Exception as e:
            print(f"⚠️ Error detectado: {e}. Reintentando en 60s...")
            time.sleep(60)
if __name__ == "__main__":
    import random
    bucle_infinito()