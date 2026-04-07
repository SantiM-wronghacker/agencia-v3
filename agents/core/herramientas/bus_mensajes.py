"""
ÁREA: CEREBRO
DESCRIPCIÓN: Bus de mensajes central. Sistema nervioso de la agencia — permite que los agentes se comuniquen entre sí depositando y recogiendo resultados sin dependencias directas.
TECNOLOGÍA: JSON (nativo)
"""

import json
import os
import time
import uuid
from datetime import datetime

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

BUS_ARCHIVO = "bus_mensajes.json"

# ─────────────────────────────────────────────
#  ESTRUCTURA DE UN MENSAJE EN EL BUS
# ─────────────────────────────────────────────
# {
#   "id": "uuid",
#   "timestamp": "2026-02-19 22:00:00",
#   "de": "maestro_ceo",
#   "para": "agente_finanzas",         # o "BROADCAST" para todos
#   "tipo": "orden | resultado | error",
#   "contenido": "...",
#   "contexto": {},                    # datos extra que el agente necesita
#   "estado": "pendiente | procesado | error",
#   "respuesta_a": "uuid_del_mensaje_original"  # para encadenar respuestas
# }

def _cargar_bus():
    """Carga el bus de mensajes desde disco."""
    if not os.path.exists(BUS_ARCHIVO):
        return []
    try:
        with open(BUS_ARCHIVO, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []

def _guardar_bus(mensajes):
    """Guarda el bus de mensajes en disco."""
    with open(BUS_ARCHIVO, 'w', encoding='utf-8') as f:
        json.dump(mensajes, f, indent=2, ensure_ascii=False)

def depositar(de, para, tipo, contenido, contexto=None, respuesta_a=None):
    """
    Deposita un mensaje en el bus.
    Retorna el ID del mensaje creado.
    """
    mensajes = _cargar_bus()
    
    mensaje = {
        "id": str(uuid.uuid4())[:8],
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "de": de,
        "para": para,
        "tipo": tipo,
        "contenido": contenido,
        "contexto": contexto or {},
        "estado": "pendiente",
        "respuesta_a": respuesta_a
    }
    
    mensajes.append(mensaje)
    _guardar_bus(mensajes)
    
    _registrar_log(f"[BUS] {de} → {para} | {tipo} | id:{mensaje['id']}")
    return mensaje["id"]

def recoger(para, tipo=None, solo_pendientes=True):
    """
    Recoge mensajes dirigidos a un agente.
    Retorna lista de mensajes y los marca como procesados.
    """
    mensajes = _cargar_bus()
    encontrados = []
    
    for m in mensajes:
        destinatario_ok = (m["para"] == para or m["para"] == "BROADCAST")
        tipo_ok = (tipo is None or m["tipo"] == tipo)
        estado_ok = (not solo_pendientes or m["estado"] == "pendiente")
        
        if destinatario_ok and tipo_ok and estado_ok:
            encontrados.append(m)
            m["estado"] = "procesado"
    
    if encontrados:
        _guardar_bus(mensajes)
    
    return encontrados

def recoger_respuesta(id_mensaje_original, timeout=30):
    """
    Espera y recoge la respuesta a un mensaje específico.
    Útil para comunicación síncrona entre agentes.
    """
    inicio = time.time()
    while time.time() - inicio < timeout:
        mensajes = _cargar_bus()
        for m in mensajes:
            if m.get("respuesta_a") == id_mensaje_original and m["estado"] == "pendiente":
                m["estado"] = "procesado"
                _guardar_bus(mensajes)
                return m
        time.sleep(0.5)
    return None

def ver_estado():
    """Muestra el estado actual del bus para diagnóstico."""
    mensajes = _cargar_bus()
    pendientes = [m for m in mensajes if m["estado"] == "pendiente"]
    procesados = [m for m in mensajes if m["estado"] == "procesado"]
    
    print(f"\n📡 BUS DE MENSAJES — Estado actual")
    print(f"   Total:     {len(mensajes)}")
    print(f"   Pendientes: {len(pendientes)}")
    print(f"   Procesados: {len(procesados)}")
    
    if pendientes:
        print("\n   Pendientes:")
        for m in pendientes[-5:]:
            print(f"   [{m['id']}] {m['de']} → {m['para']} | {m['tipo']}")
    
    return {"total": len(mensajes), "pendientes": len(pendientes), "procesados": len(procesados)}

def limpiar_procesados(mantener_ultimos=50):
    """Limpia mensajes ya procesados para no inflar el archivo."""
    mensajes = _cargar_bus()
    pendientes = [m for m in mensajes if m["estado"] == "pendiente"]
    procesados = [m for m in mensajes if m["estado"] == "procesado"]
    
    # Mantiene solo los últimos N procesados como historial
    procesados_recientes = procesados[-mantener_ultimos:]
    mensajes_limpios = procesados_recientes + pendientes
    
    _guardar_bus(mensajes_limpios)
    eliminados = len(mensajes) - len(mensajes_limpios)
    _registrar_log(f"[BUS] Limpieza: {eliminados} mensajes eliminados.")
    return eliminados

def _registrar_log(mensaje):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    with open("registro_noche.txt", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {mensaje}\n")

# ─────────────────────────────────────────────
#  USO DIRECTO: diagnóstico del bus
# ─────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "limpiar":
        n = limpiar_procesados()
        print(f"✅ Limpieza completa. {n} mensajes eliminados.")
    else:
        ver_estado()