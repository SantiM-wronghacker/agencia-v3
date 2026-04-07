"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Agente de auto-evolución que investiga y mejora código
TECNOLOGÍA: Python, json, RootAssistant, patcher_pro
"""
import time
import os
import json
import sys
from datetime import datetime
from agencia.agents.cerebro.root_assistant import RootAssistant
from agencia.agents.cerebro.patcher_pro import aplicar_mejora, model

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def actualizar_historial(accion, detalle):
    ruta = "runs/state.json"
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {"recent": []}

    nuevo_evento = {
        "role": "system_auto",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "content": f" AUTO-MEJORA: {accion}. Detalle: {detalle}"
    }
    data['recent'].append(nuevo_evento)

    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def iniciar_evolucion_real(tema="nuevas librerias de automatizacion financiera 2026", mision="Optimiza el manejo de errores en app_dashboard.py para que sea más robusto.", intervalo=300):
    ra = RootAssistant()
    print("Iniciando evolución con reporte en state.json...")
    print(f"Tema de investigación: {tema}")
    print(f"Misión principal: {mision}")
    print(f"Intervalo entre ciclos: {intervalo} segundos")

    while True:
        try:
            print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Iniciando ciclo de evolución...")
            ra.investigar_tecnologia(tema)
            time.sleep(2)
            actualizar_historial("Investigación", f"Se buscó información sobre {tema}")

            aplicar_mejora("app_dashboard.py", mision)
            time.sleep(2)
            actualizar_historial("Parche aplicado", f"Se mejoró app_dashboard.py con la misión: {mision}")

            print("Ciclo completado. Reporte guardado en state.json.")
            print(f"Próximo ciclo en {intervalo} segundos...")
            time.sleep(intervalo)

        except Exception as e:
            error_msg = f"Error crítico: {str(e)}"
            print(error_msg)
            actualizar_historial("Error", error_msg)
            time.sleep(60)

def mostrar_resumen():
    try:
        with open("runs/state.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
        print("\n=== RESUMEN EJECUTIVO ===")
        print(f"Eventos recientes: {len(data['recent'])}")
        print("Últimos eventos:")
        for evento in data['recent'][-3:]:
            print(f"- {evento['timestamp']}: {evento['content']}")
    except Exception as e:
        print(f"\n=== RESUMEN EJECUTIVO ===")
        print("No se pudo cargar el historial de eventos.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        tema = sys.argv[1]
    if len(sys.argv) > 2:
        mision = sys.argv[2]
    if len(sys.argv) > 3:
        try:
            intervalo = int(sys.argv[3])
        except ValueError:
            intervalo = 300
    else:
        intervalo = 300

    iniciar_evolucion_real(tema, mision, intervalo)
    mostrar_resumen()