"""
ÁREA: CEREBRO
DESCRIPCIÓN: Integrador masivo del llm_router. Reemplaza todas las llamadas directas
a Groq en todos los agentes por el sistema de rotación automática de proveedores.
TECNOLOGÍA: AST, Python
"""

import os
import re
import shutil
from datetime import datetime

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

LOG = "registro_noche.txt"

# Agentes que NO se tocan (ya usan el router o son del sistema)
EXCLUIR = {
    "llm_router.py", "bus_mensajes.py", "noche_total.py",
    "reparador_masivo.py", "integrador_router.py",
    "orquestador_clawbot.py", "maestro_ceo.py"
}

# Patrones de imports de Groq a reemplazar
PATRON_IMPORT_GROQ = re.compile(
    r'from groq import Groq.*?\n|import groq.*?\n',
    re.IGNORECASE
)

# Patrones de inicialización del cliente Groq
PATRON_CLIENTE = re.compile(
    r'client\s*=\s*Groq\s*\(.*?\)\s*\n|'
    r'API_KEY\s*=\s*["\']gsk_[^"\']+["\']\s*\n|'
    r'MODELO\s*=\s*["\']llama[^"\']+["\']\s*\n',
    re.IGNORECASE
)

# Patrones de llamadas directas a Groq
PATRON_LLAMADA = re.compile(
    r'client\.chat\.completions\.create\s*\(',
    re.IGNORECASE
)


def log(msg):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    linea = f"[{ts}] [INTEGRADOR] {msg}"
    print(linea)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(linea + "\n")


def necesita_integracion(codigo):
    """Detecta si un agente usa Groq directamente."""
    tiene_groq = bool(re.search(r'from groq import|import groq|Groq\(', codigo, re.IGNORECASE))
    ya_usa_router = 'from llm_router import' in codigo or 'llm_router' in codigo
    return tiene_groq and not ya_usa_router


def integrar_agente(archivo):
    """
    Integra el llm_router en un agente que usa Groq directo.
    Estrategia: agrega el import del router al inicio y reemplaza
    las llamadas directas por completar() del router.
    """
    with open(archivo, 'r', encoding='utf-8', errors='replace') as f:
        codigo = f.read()

    if not necesita_integracion(codigo):
        return "YA_INTEGRADO"

    # Backup
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = archivo.replace('.py', f'.bak.{ts}')
    shutil.copy2(archivo, backup)

    nuevo_codigo = codigo

    # 1. Eliminar imports de Groq
    nuevo_codigo = re.sub(
        r'from groq import Groq\s*\n',
        '',
        nuevo_codigo
    )
    nuevo_codigo = re.sub(
        r'import groq\s*\n',
        '',
        nuevo_codigo
    )

    # 2. Eliminar API_KEY hardcodeada de Groq
    nuevo_codigo = re.sub(
        r'API_KEY\s*=\s*["\']gsk_[^"\']+["\']\s*\n',
        '',
        nuevo_codigo
    )

    # 3. Eliminar inicialización del cliente Groq
    nuevo_codigo = re.sub(
        r'client\s*=\s*Groq\s*\([^)]*\)\s*\n',
        '',
        nuevo_codigo
    )

    # 4. Eliminar definición del MODELO si era solo para Groq
    nuevo_codigo = re.sub(
        r'MODELO\s*=\s*["\']llama-3\.3-70b-versatile["\']\s*\n',
        '',
        nuevo_codigo
    )

    # 5. Reemplazar llamadas a client.chat.completions.create por completar()
    # Detecta si el agente hace llamadas simples y las convierte
    nuevo_codigo = re.sub(
        r'client\.chat\.completions\.create\s*\(',
        '_groq_compat_create(',
        nuevo_codigo
    )

    # 6. Agregar import del router y función de compatibilidad al inicio
    # (después del docstring si existe)
    import_router = '''from llm_router import completar

def _groq_compat_create(**kwargs):
    """Compatibilidad con llamadas antiguas a client.chat.completions.create"""
    messages = kwargs.get('messages', [])
    temperatura = kwargs.get('temperature', 0.5)
    max_tokens = kwargs.get('max_tokens', 1000)

    class _Resp:
        class _Choice:
            class _Msg:
                content = ""
            message = _Msg()
        choices = [_Choice()]

    resultado = completar(messages, temperatura=temperatura, max_tokens=max_tokens)
    resp = _Resp()
    resp.choices[0].message.content = resultado or ""
    return resp

'''

    # Insertar después del docstring del módulo o al inicio
    if nuevo_codigo.startswith('"""') or nuevo_codigo.startswith("'''"):
        # Buscar fin del docstring
        for delim in ['"""', "'''"]:
            if nuevo_codigo.startswith(delim):
                fin = nuevo_codigo.find(delim, 3)
                if fin != -1:
                    pos = fin + 3
                    # Saltar saltos de línea
                    while pos < len(nuevo_codigo) and nuevo_codigo[pos] == '\n':
                        pos += 1
                    nuevo_codigo = nuevo_codigo[:pos] + '\n' + import_router + nuevo_codigo[pos:]
                    break
    else:
        nuevo_codigo = import_router + nuevo_codigo

    # 7. Escribir resultado
    with open(archivo, 'w', encoding='utf-8') as f:
        f.write(nuevo_codigo)

    log(f"  ✓ {archivo} integrado. Backup: {backup}")
    return "INTEGRADO"


def ejecutar():
    log("=" * 60)
    log("INTEGRADOR MASIVO LLM_ROUTER INICIADO")
    log("=" * 60)

    archivos = [
        f for f in sorted(os.listdir('.'))
        if f.endswith('.py') and f not in EXCLUIR
    ]

    resultados = {"INTEGRADO": [], "YA_INTEGRADO": [], "ERROR": [], "SIN_GROQ": []}

    for archivo in archivos:
        try:
            with open(archivo, 'r', encoding='utf-8', errors='replace') as f:
                codigo = f.read()

            if 'from groq import' not in codigo and 'import groq' not in codigo and 'Groq(' not in codigo:
                resultados["SIN_GROQ"].append(archivo)
                continue

            resultado = integrar_agente(archivo)
            resultados[resultado].append(archivo)

        except Exception as e:
            log(f"  ERROR en {archivo}: {e}")
            resultados["ERROR"].append(archivo)

    log("\n" + "=" * 60)
    log("INTEGRACIÓN COMPLETADA")
    log(f"  Integrados:     {len(resultados['INTEGRADO'])}")
    log(f"  Ya integrados:  {len(resultados['YA_INTEGRADO'])}")
    log(f"  Sin Groq:       {len(resultados['SIN_GROQ'])}")
    log(f"  Errores:        {len(resultados['ERROR'])}")
    log("=" * 60)

    if resultados['INTEGRADO']:
        log(f"\nAgentes integrados:")
        for a in resultados['INTEGRADO']:
            log(f"  ✓ {a}")

    if resultados['ERROR']:
        log(f"\nErrores:")
        for a in resultados['ERROR']:
            log(f"  ✗ {a}")


if __name__ == "__main__":
    ejecutar()