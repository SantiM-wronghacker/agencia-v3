"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Gestor de configuración para la fábrica de agentes.
             Lee preferencias del usuario (modo, prioridades).
TECNOLOGÍA: Python estándar (json, os)
"""

import os
import json
from datetime import datetime

CONFIG_FILE = ".fabricamode"
MODO_DEFAULT = "NOCHE"

def leer_modo_usuario():
    """Lee el modo preferido del usuario desde el archivo .fabricamode"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                modo = f.read().strip().upper()
                if modo in ["CREAR", "MEJORAR", "BALANCEADO", "EXPANSION", "NOCHE"]:
                    return modo
        except Exception as e:
            print(f"  [WARN] Error leyendo {CONFIG_FILE}: {e}")
    return MODO_DEFAULT

def guardar_modo_usuario(modo):
    """Guarda el modo preferido del usuario"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            f.write(modo.upper())
        return True
    except Exception as e:
        print(f"  [WARN] Error guardando {CONFIG_FILE}: {e}")
        return False

def limpiar_modo_usuario():
    """Limpia la preferencia guardada (vuelve al default)"""
    if os.path.exists(CONFIG_FILE):
        try:
            os.remove(CONFIG_FILE)
            return True
        except Exception as e:
            print(f"  [WARN] Error limpiando {CONFIG_FILE}: {e}")
            return False
    return True

def traducir_modo(modo):
    """Traduce el modo interno a descripción legible"""
    descripciones = {
        "CREAR": "Generar nuevos agentes (CREAR)",
        "MEJORAR": "Optimizar existentes (MEJORAR)",
        "BALANCEADO": "Crear Y mejorar simultáneamente (BALANCEADO)",
        "EXPANSION": "Solo micros del plan (EXPANSION)",
        "NOCHE": "Todas las tareas: noche + factory + misiones (NOCHE)"
    }
    return descripciones.get(modo, f"Desconocido ({modo})")

def obtener_config_fabrica(modo):
    """Retorna la configuración de fábrica según el modo"""
    configs = {
        "CREAR": {
            "tamaño_lote": 15,
            "modo_fabrica": "crear",  # Crear nuevos hasta 500
            "umbral_modo_mejora": 500,
            "descripcion": "Creando nuevos agentes"
        },
        "MEJORAR": {
            "tamaño_lote": 20,
            "modo_fabrica": "mejorar",  # Mejorar los existentes
            "umbral_modo_mejora": 9999,  # Nunca cambiar a crear
            "descripcion": "Mejorando agentes existentes"
        },
        "BALANCEADO": {
            "tamaño_lote": 10,
            "modo_fabrica": "balanceado",  # 60% crear, 40% mejorar
            "umbral_modo_mejora": 500,
            "descripcion": "Creando Y mejorando"
        },
        "EXPANSION": {
            "tamaño_lote": 8,
            "modo_fabrica": "expansion",  # Solo micros del plan
            "umbral_modo_mejora": 9999,
            "descripcion": "Generando 206 micros planificados"
        },
        "NOCHE": {
            "tamaño_lote": 15,
            "modo_fabrica": "crear",  # Default
            "umbral_modo_mejora": 500,
            "descripcion": "Modo noche completo: factory + noche + misiones"
        }
    }
    return configs.get(modo.upper(), configs["NOCHE"])

# ─────────────────────────────────────────────
#  LOG DE PREFERENCIAS
# ─────────────────────────────────────────────

def registrar_preferencia(modo):
    """Registra en logs que modo está siendo usado"""
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    msg = f"[{ts}] [FABRICA_CONFIG] Modo seleccionado: {modo} ({traducir_modo(modo)})\n"
    try:
        with open("registro_noche.txt", "a", encoding="utf-8") as f:
            f.write(msg)
    except:
        pass

# ─────────────────────────────────────────────
#  EJEMPLO DE USO
# ─────────────────────────────────────────────

if __name__ == "__main__":
    modo = leer_modo_usuario()
    print(f"\nModo actual: {modo}")
    print(f"Descripcion: {traducir_modo(modo)}")
    config = obtener_config_fabrica(modo)
    print(f"Config: {config}")
