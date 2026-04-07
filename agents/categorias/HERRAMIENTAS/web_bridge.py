"""
AREA: HERRAMIENTAS
DESCRIPCION: Puente de Internet v1.0. Modulo que cualquier agente puede importar
             para tener acceso a internet en tiempo real. Usa solo stdlib (urllib,
             http.client). Funciones: buscar(), fetch(), extraer_precios(),
             buscar_vuelos(), buscar_hoteles().
TECNOLOGIA: urllib, http.client (stdlib)
"""

import urllib.request
import urllib.parse
import urllib.error
import http.client
import ssl
import re
import json
import sys
import io as _io
from datetime import datetime

# Fix Unicode para Windows (cp1252)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
elif hasattr(sys.stdout, "buffer"):
    sys.stdout = open(sys.stdout.fileno(), mode="w", encoding="utf-8", errors="replace", closefd=False)
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
elif hasattr(sys.stderr, "buffer"):
    sys.stderr = open(sys.stderr.fileno(), mode="w", encoding="utf-8", errors="replace", closefd=False)

# ─────────────────────────────────────────────
#  CONFIGURACION
# ─────────────────────────────────────────────

TIMEOUT = 10  # segundos

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "es-MX,es;q=0.9,en;q=0.8",
}

# Variable global para saber si hay internet
WEB = False

def _test_conexion():
    """Prueba si hay conexion a internet."""
    global WEB
    try:
        req = urllib.request.Request("https://www.google.com", method="HEAD")
        req.add_header("User-Agent", HEADERS["User-Agent"])
        urllib.request.urlopen(req, timeout=5)
        WEB = True
    except Exception:
        WEB = False
    return WEB

# Probar conexion al importar
_test_conexion()


# ─────────────────────────────────────────────
#  FETCH — obtener contenido de cualquier URL
# ─────────────────────────────────────────────

def fetch(url, timeout=TIMEOUT):
    """
    Obtiene el contenido HTML/texto de cualquier URL.

    Args:
        url: URL completa (con https://)
        timeout: segundos de timeout (default 10)

    Returns:
        dict con keys: ok, contenido, status, error
    """
    try:
        req = urllib.request.Request(url)
        for k, v in HEADERS.items():
            req.add_header(k, v)

        # Crear contexto SSL que no falle con certificados
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        resp = urllib.request.urlopen(req, timeout=timeout, context=ctx)
        status = resp.getcode()
        encoding = resp.headers.get_content_charset() or "utf-8"

        contenido = resp.read()
        try:
            texto = contenido.decode(encoding, errors="replace")
        except Exception:
            texto = contenido.decode("utf-8", errors="replace")

        return {"ok": True, "contenido": texto, "status": status, "error": None}

    except urllib.error.HTTPError as e:
        return {"ok": False, "contenido": "", "status": e.code, "error": f"HTTP {e.code}: {e.reason}"}
    except urllib.error.URLError as e:
        return {"ok": False, "contenido": "", "status": 0, "error": f"URL Error: {e.reason}"}
    except Exception as e:
        return {"ok": False, "contenido": "", "status": 0, "error": str(e)}


def _limpiar_html(html):
    """Quita tags HTML y devuelve solo texto limpio."""
    # Quitar scripts y styles
    html = re.sub(r'<script[^>]*>[\s\S]*?</script>', ' ', html, flags=re.IGNORECASE)
    html = re.sub(r'<style[^>]*>[\s\S]*?</style>', ' ', html, flags=re.IGNORECASE)
    # Quitar tags
    html = re.sub(r'<[^>]+>', ' ', html)
    # Decodificar entidades comunes
    html = html.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    html = html.replace('&quot;', '"').replace('&#39;', "'").replace('&nbsp;', ' ')
    # Limpiar espacios
    html = re.sub(r'\s+', ' ', html).strip()
    return html


def fetch_texto(url, timeout=TIMEOUT):
    """
    Igual que fetch() pero devuelve solo texto limpio (sin HTML).
    """
    resultado = fetch(url, timeout)
    if resultado["ok"]:
        resultado["contenido"] = _limpiar_html(resultado["contenido"])
    return resultado


# ─────────────────────────────────────────────
#  BUSCAR — busqueda web via DuckDuckGo HTML
# ─────────────────────────────────────────────

def buscar(query, max_resultados=5):
    """
    Busca en DuckDuckGo y retorna lista de resultados.

    Args:
        query: texto a buscar
        max_resultados: maximo de resultados (default 5)

    Returns:
        lista de dicts con keys: titulo, url, snippet
    """
    if not query:
        return []

    try:
        # DuckDuckGo HTML lite
        params = urllib.parse.urlencode({"q": query})
        url = f"https://html.duckduckgo.com/html/?{params}"

        req = urllib.request.Request(url)
        for k, v in HEADERS.items():
            req.add_header(k, v)

        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        resp = urllib.request.urlopen(req, timeout=TIMEOUT, context=ctx)
        html = resp.read().decode("utf-8", errors="replace")

        resultados = []

        # Parsear resultados de DuckDuckGo HTML
        # Cada resultado esta en un <div class="result">
        bloques = re.findall(r'<div[^>]*class="[^"]*result[^"]*"[^>]*>([\s\S]*?)</div>\s*(?=<div[^>]*class="[^"]*result|$)', html)

        if not bloques:
            # Fallback: buscar links directamente
            links = re.findall(r'<a[^>]*class="result__a"[^>]*href="([^"]*)"[^>]*>([\s\S]*?)</a>', html)
            snippets = re.findall(r'<a[^>]*class="result__snippet"[^>]*>([\s\S]*?)</a>', html)

            for i, (href, titulo) in enumerate(links[:max_resultados]):
                # DuckDuckGo usa redirect URLs, extraer la real
                url_real = href
                match_url = re.search(r'uddg=([^&]+)', href)
                if match_url:
                    url_real = urllib.parse.unquote(match_url.group(1))

                snippet = _limpiar_html(snippets[i]) if i < len(snippets) else ""
                resultados.append({
                    "titulo": _limpiar_html(titulo),
                    "url": url_real,
                    "snippet": snippet[:200]
                })
        else:
            for bloque in bloques[:max_resultados]:
                # Extraer titulo y URL
                match_link = re.search(r'<a[^>]*class="result__a"[^>]*href="([^"]*)"[^>]*>([\s\S]*?)</a>', bloque)
                match_snippet = re.search(r'class="result__snippet"[^>]*>([\s\S]*?)</(?:a|div|span)>', bloque)

                if match_link:
                    href = match_link.group(1)
                    titulo = _limpiar_html(match_link.group(2))

                    url_real = href
                    match_url = re.search(r'uddg=([^&]+)', href)
                    if match_url:
                        url_real = urllib.parse.unquote(match_url.group(1))

                    snippet = _limpiar_html(match_snippet.group(1))[:200] if match_snippet else ""

                    resultados.append({
                        "titulo": titulo,
                        "url": url_real,
                        "snippet": snippet
                    })

        return resultados[:max_resultados]

    except Exception as e:
        return [{"titulo": "Error", "url": "", "snippet": str(e)}]


# ─────────────────────────────────────────────
#  EXTRAER PRECIOS — numeros con $ de un texto
# ─────────────────────────────────────────────

def extraer_precios(texto):
    """
    Extrae numeros con simbolo $ de un texto scrapeado.

    Args:
        texto: string con contenido de una pagina web

    Returns:
        lista de dicts con keys: precio_texto, precio_numero, moneda
    """
    if not texto:
        return []

    precios = []

    # Patron: $1,234.56 | $1234 | USD 1,234 | MXN 1234.56
    patrones = [
        # $1,234.56 o $1234
        r'(\$\s*[\d,]+(?:\.\d{1,2})?)',
        # USD/MXN 1,234.56
        r'((?:USD|MXN|EUR)\s*[\d,]+(?:\.\d{1,2})?)',
        # 1,234 USD/MXN
        r'([\d,]+(?:\.\d{1,2})?\s*(?:USD|MXN|EUR|dolares|pesos))',
    ]

    encontrados = set()

    for patron in patrones:
        matches = re.findall(patron, texto, re.IGNORECASE)
        for match in matches:
            if match not in encontrados:
                encontrados.add(match)
                # Extraer numero limpio
                numeros = re.findall(r'[\d,]+(?:\.\d{1,2})?', match)
                if numeros:
                    num_str = numeros[0].replace(",", "")
                    try:
                        num = float(num_str)
                        # Detectar moneda
                        moneda = "MXN"
                        if "USD" in match.upper() or "dolar" in match.lower():
                            moneda = "USD"
                        elif "EUR" in match.upper():
                            moneda = "EUR"

                        precios.append({
                            "precio_texto": match.strip(),
                            "precio_numero": num,
                            "moneda": moneda
                        })
                    except ValueError:
                        pass

    # Ordenar por precio
    precios.sort(key=lambda x: x["precio_numero"])
    return precios


# ─────────────────────────────────────────────
#  BUSCAR VUELOS — scraping Google Flights
# ─────────────────────────────────────────────

def buscar_vuelos(origen, destino, fecha):
    """
    Busca vuelos usando busqueda web (Google Flights no permite scraping directo,
    asi que busca en DuckDuckGo por resultados de vuelos).

    Args:
        origen: ciudad o codigo IATA de origen (ej: "CDMX", "MEX")
        destino: ciudad o codigo IATA de destino (ej: "Tokio", "NRT")
        fecha: fecha del vuelo (ej: "2025-03-15", "marzo 2025")

    Returns:
        dict con keys: ok, vuelos (lista), fuente, error
    """
    try:
        query = f"vuelos {origen} a {destino} {fecha} precio"
        resultados_web = buscar(query, max_resultados=5)

        vuelos = []
        for r in resultados_web:
            # Intentar extraer precios del snippet
            precios = extraer_precios(r.get("snippet", ""))
            vuelos.append({
                "fuente": r.get("titulo", ""),
                "url": r.get("url", ""),
                "info": r.get("snippet", ""),
                "precios_encontrados": precios
            })

        # Tambien buscar en Kayak/Skyscanner
        query2 = f"flights {origen} to {destino} {fecha} cheap"
        resultados2 = buscar(query2, max_resultados=3)
        for r in resultados2:
            precios = extraer_precios(r.get("snippet", ""))
            vuelos.append({
                "fuente": r.get("titulo", ""),
                "url": r.get("url", ""),
                "info": r.get("snippet", ""),
                "precios_encontrados": precios
            })

        return {
            "ok": len(vuelos) > 0,
            "origen": origen,
            "destino": destino,
            "fecha": fecha,
            "vuelos": vuelos,
            "total_resultados": len(vuelos),
            "error": None
        }

    except Exception as e:
        return {
            "ok": False, "origen": origen, "destino": destino,
            "fecha": fecha, "vuelos": [], "total_resultados": 0,
            "error": str(e)
        }


# ─────────────────────────────────────────────
#  BUSCAR HOTELES — scraping Booking/Hotels
# ─────────────────────────────────────────────

def buscar_hoteles(destino, fechas, personas=2):
    """
    Busca hoteles usando busqueda web (Booking no permite scraping directo,
    asi que busca resultados de hoteles via DuckDuckGo).

    Args:
        destino: ciudad destino (ej: "Cancun", "CDMX")
        fechas: rango de fechas (ej: "15-20 marzo 2025")
        personas: numero de personas (default 2)

    Returns:
        dict con keys: ok, hoteles (lista), fuente, error
    """
    try:
        query = f"hoteles {destino} {fechas} {personas} personas precio por noche"
        resultados_web = buscar(query, max_resultados=5)

        hoteles = []
        for r in resultados_web:
            precios = extraer_precios(r.get("snippet", ""))
            hoteles.append({
                "fuente": r.get("titulo", ""),
                "url": r.get("url", ""),
                "info": r.get("snippet", ""),
                "precios_encontrados": precios
            })

        # Busqueda adicional en ingles
        query2 = f"hotels {destino} {fechas} {personas} guests price"
        resultados2 = buscar(query2, max_resultados=3)
        for r in resultados2:
            precios = extraer_precios(r.get("snippet", ""))
            hoteles.append({
                "fuente": r.get("titulo", ""),
                "url": r.get("url", ""),
                "info": r.get("snippet", ""),
                "precios_encontrados": precios
            })

        return {
            "ok": len(hoteles) > 0,
            "destino": destino,
            "fechas": fechas,
            "personas": personas,
            "hoteles": hoteles,
            "total_resultados": len(hoteles),
            "error": None
        }

    except Exception as e:
        return {
            "ok": False, "destino": destino, "fechas": fechas,
            "personas": personas, "hoteles": [], "total_resultados": 0,
            "error": str(e)
        }


# ─────────────────────────────────────────────
#  TEST RAPIDO
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 55)
    print("WEB BRIDGE v1.0 — Puente de Internet")
    print("=" * 55)

    print(f"\nConexion a internet: {'SI' if WEB else 'NO'}")

    if not WEB:
        print("Sin conexion. El modulo funciona pero retornara errores.")
        sys.exit(0)

    # Test buscar
    print("\n--- Test buscar('tipo de cambio dolar mexico hoy') ---")
    resultados = buscar("tipo de cambio dolar mexico hoy", max_resultados=3)
    for r in resultados:
        print(f"  {r['titulo'][:60]}")
        print(f"  {r['url'][:80]}")
        print(f"  {r['snippet'][:100]}")
        print()

    # Test extraer_precios
    print("--- Test extraer_precios ---")
    texto_prueba = "El dolar esta a $17.50 MXN. Vuelo desde $3,499 MXN. Hotel USD 120 por noche."
    precios = extraer_precios(texto_prueba)
    for p in precios:
        print(f"  {p['precio_texto']} -> {p['precio_numero']} {p['moneda']}")

    # Test fetch
    print("\n--- Test fetch ---")
    r = fetch_texto("https://www.google.com")
    print(f"  Status: {r['status']}")
    print(f"  Contenido: {r['contenido'][:100]}...")

    print("\n" + "=" * 55)
    print("Todos los tests completados.")
