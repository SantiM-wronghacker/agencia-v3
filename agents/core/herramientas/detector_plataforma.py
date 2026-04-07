"""
AREA: CEREBRO
DESCRIPCION: Detecta en que plataforma esta hospedado un sitio web y que servicios
             utiliza (hosting, CMS, analytics, redes sociales, pagos). Analiza headers
             HTTP, DNS y contenido HTML para determinar la stack tecnologica.
TECNOLOGIA: Python stdlib (urllib, socket, re, json)
"""

import os
import sys
import re
import json
import socket
from urllib.request import urlopen, Request
from urllib.error import URLError
from pathlib import Path

BASE_DIR = Path(__file__).parent


def _fetch(url: str, timeout: int = 10) -> tuple:
    """Fetch URL, retorna (status, headers_dict, body_text)."""
    try:
        if not url.startswith("http"):
            url = "https://" + url
        req = Request(url, headers={"User-Agent": "Mozilla/5.0 (AgenciaSanti Bot)"})
        resp = urlopen(req, timeout=timeout)
        headers = {k.lower(): v for k, v in resp.getheaders()}
        body = resp.read(50000).decode("utf-8", errors="replace")
        return resp.status, headers, body
    except URLError as e:
        return 0, {}, str(e)
    except Exception as e:
        return 0, {}, str(e)


def _resolver_dns(dominio: str) -> dict:
    """Resuelve DNS basico del dominio."""
    resultado = {"ips": [], "cname": None}
    try:
        # Limpiar dominio
        dominio = dominio.replace("https://", "").replace("http://", "").split("/")[0]
        ips = socket.getaddrinfo(dominio, None)
        resultado["ips"] = list(set(ip[4][0] for ip in ips))
    except Exception:
        pass
    return resultado


def detectar_hosting(url: str) -> dict:
    """
    Detecta la plataforma de hosting de un sitio web.
    Retorna: {hosting, cms, servicios[], credenciales_necesarias[]}
    """
    resultado = {
        "url": url,
        "hosting": None,
        "hosting_id": None,
        "cms": None,
        "cms_id": None,
        "cdn": None,
        "servicios_detectados": [],
        "plataformas_necesarias": [],
        "confianza": "baja",
    }

    status, headers, body = _fetch(url)
    if status == 0:
        resultado["error"] = f"No se pudo acceder a {url}"
        return resultado

    headers_str = json.dumps(headers).lower()
    body_lower = body.lower()

    # ── HOSTING ──
    hosting_checks = [
        # (id, nombre, [indicadores en headers/body])
        ("github_pages", "GitHub Pages", ["github.io", "server: github.com", "fastly"]),
        ("vercel", "Vercel", ["x-vercel", "vercel", ".vercel.app"]),
        ("netlify", "Netlify", ["x-nf-", "netlify", ".netlify.app"]),
        ("firebase", "Firebase Hosting", ["x-firebase", "firebaseapp.com", "firebase"]),
        ("aws_s3", "AWS S3 / CloudFront", ["x-amz-", "cloudfront", "amazonaws.com"]),
        ("cloudflare", "Cloudflare", ["cf-ray", "cloudflare", "cf-cache"]),
        ("shopify", "Shopify", ["x-shopify", "shopify", "myshopify.com", "cdn.shopify"]),
        ("wordpress", "WordPress.com", ["wp-content", "wordpress", "wp-json"]),
        ("wix", "Wix", ["x-wix", "wix.com", "wixsite"]),
        ("squarespace", "Squarespace", ["squarespace", "sqsp"]),
        ("cpanel_ftp", "cPanel / Hosting tradicional", ["cpanel", "whm", "x-powered-by: plesk"]),
    ]

    for hid, nombre, indicadores in hosting_checks:
        for ind in indicadores:
            if ind in headers_str or ind in body_lower or ind in url.lower():
                resultado["hosting"] = nombre
                resultado["hosting_id"] = hid
                resultado["confianza"] = "alta"
                break
        if resultado["hosting"]:
            break

    # Si no detecta hosting pero responde, es hosting generico
    if not resultado["hosting"] and status == 200:
        resultado["hosting"] = "Hosting Desconocido (probablemente cPanel/VPS)"
        resultado["hosting_id"] = "cpanel_ftp"
        resultado["confianza"] = "media"

    # ── CMS ──
    cms_checks = [
        ("wordpress", "WordPress", ["wp-content", "wp-includes", "wp-json", "/xmlrpc.php"]),
        ("shopify", "Shopify", ["cdn.shopify", "shopify.com", "myshopify"]),
        ("woocommerce", "WooCommerce", ["woocommerce", "wc-ajax"]),
        ("joomla", "Joomla", ["/media/jui/", "joomla"]),
        ("drupal", "Drupal", ["drupal", "/sites/default/"]),
        ("webflow", "Webflow", ["webflow", ".webflow.io"]),
    ]

    for cid, nombre, indicadores in cms_checks:
        for ind in indicadores:
            if ind in body_lower or ind in headers_str:
                resultado["cms"] = nombre
                resultado["cms_id"] = cid
                break
        if resultado["cms"]:
            break

    # ── CDN ──
    if "cloudflare" in headers_str:
        resultado["cdn"] = "Cloudflare"
    elif "cloudfront" in headers_str:
        resultado["cdn"] = "CloudFront (AWS)"
    elif "fastly" in headers_str:
        resultado["cdn"] = "Fastly"
    elif "akamai" in headers_str:
        resultado["cdn"] = "Akamai"

    # ── SERVICIOS DETECTADOS EN EL HTML ──
    servicios_checks = [
        ("google_analytics", "Google Analytics", ["gtag", "google-analytics", "ga.js", "googletagmanager"]),
        ("meta_pixel", "Meta Pixel", ["fbq(", "facebook.com/tr", "fbevents"]),
        ("hotjar", "Hotjar", ["hotjar", "hj("]),
        ("mailchimp", "Mailchimp", ["mailchimp", "mc.js", "list-manage.com"]),
        ("stripe", "Stripe", ["stripe.com/v3", "stripe.js"]),
        ("paypal", "PayPal", ["paypal.com/sdk", "paypalobjects"]),
        ("whatsapp_widget", "WhatsApp Widget", ["wa.me", "whatsapp", "api.whatsapp"]),
        ("facebook_messenger", "Facebook Chat Plugin", ["customerchat", "facebook.com/customer_chat"]),
        ("intercom", "Intercom", ["intercom", "intercomcdn"]),
        ("crisp", "Crisp Chat", ["crisp.chat", "client.crisp"]),
        ("hubspot", "HubSpot", ["hubspot", "hs-scripts", "hbspt"]),
        ("google_maps", "Google Maps", ["maps.googleapis", "google.com/maps"]),
        ("recaptcha", "reCAPTCHA", ["recaptcha", "grecaptcha"]),
        ("tiktok_pixel", "TikTok Pixel", ["analytics.tiktok", "tiktok.com/i18n"]),
    ]

    for sid, nombre, indicadores in servicios_checks:
        for ind in indicadores:
            if ind in body_lower:
                resultado["servicios_detectados"].append({
                    "id": sid,
                    "nombre": nombre,
                })
                break

    # ── REDES SOCIALES ENCONTRADAS EN EL SITIO ──
    redes_patterns = {
        "facebook_pages": r'facebook\.com/[\w.-]+',
        "instagram": r'instagram\.com/[\w.-]+',
        "twitter_x": r'(?:twitter|x)\.com/[\w.-]+',
        "tiktok": r'tiktok\.com/@[\w.-]+',
        "linkedin": r'linkedin\.com/(?:in|company)/[\w.-]+',
        "youtube": r'youtube\.com/(?:@|channel/|c/)[\w.-]+',
    }

    for red_id, pattern in redes_patterns.items():
        match = re.search(pattern, body)
        if match:
            resultado["servicios_detectados"].append({
                "id": red_id,
                "nombre": red_id.replace("_", " ").title(),
                "url_encontrada": match.group(0),
            })

    # ── PLATAFORMAS QUE NECESITAN CREDENCIALES ──
    necesarias = set()
    if resultado["hosting_id"]:
        necesarias.add(resultado["hosting_id"])
    if resultado["cms_id"]:
        necesarias.add(resultado["cms_id"])
    for srv in resultado["servicios_detectados"]:
        sid = srv["id"]
        # Mapear servicios a plataformas del gestor_credenciales
        mapa = {
            "google_analytics": "google_analytics",
            "meta_pixel": "meta_ads",
            "stripe": "stripe",
            "paypal": "paypal",
            "mailchimp": "mailchimp",
            "hubspot": "hubspot",
            "whatsapp_widget": "whatsapp_business",
            "facebook_messenger": "messenger",
            "facebook_pages": "facebook_pages",
            "instagram": "instagram",
            "twitter_x": "twitter_x",
            "tiktok": "tiktok",
            "linkedin": "linkedin",
            "tiktok_pixel": "tiktok",
        }
        if sid in mapa:
            necesarias.add(mapa[sid])

    resultado["plataformas_necesarias"] = sorted(necesarias)

    return resultado


def analisis_completo(url: str, proyecto: str = None) -> dict:
    """
    Analisis completo: detecta hosting + verifica credenciales guardadas.
    """
    deteccion = detectar_hosting(url)

    # Si hay proyecto, verificar que credenciales ya tenemos
    if proyecto:
        try:
            from agencia.agents.herramientas.gestor_credenciales import tiene_credencial, PLATAFORMAS
            configuradas = []
            faltantes = []
            for plat_id in deteccion["plataformas_necesarias"]:
                if plat_id in PLATAFORMAS:
                    info = PLATAFORMAS[plat_id]
                    entry = {
                        "plataforma": plat_id,
                        "nombre": info["nombre"],
                        "campos": info["campos"],
                        "instrucciones": info["instrucciones"],
                    }
                    if tiene_credencial(proyecto, plat_id):
                        configuradas.append(entry)
                    else:
                        faltantes.append(entry)

            deteccion["credenciales_configuradas"] = configuradas
            deteccion["credenciales_faltantes"] = faltantes
        except ImportError:
            deteccion["credenciales_configuradas"] = []
            deteccion["credenciales_faltantes"] = []

    return deteccion


# ─────────────────────────────────────────────────────────────────────────────
#  CLI
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    args = sys.argv[1:]

    if not args or args[0] == "--help":
        print("Detector de Plataforma — Agencia Santi")
        print()
        print("Uso:")
        print("  python detector_plataforma.py <url>")
        print("  python detector_plataforma.py <url> --proyecto <nombre>")
        sys.exit(0)

    url = args[0]
    proyecto = None
    if "--proyecto" in args:
        idx = args.index("--proyecto")
        if idx + 1 < len(args):
            proyecto = args[idx + 1]

    print(f"Analizando: {url}")
    print("-" * 50)

    resultado = analisis_completo(url, proyecto)

    print(f"Hosting:    {resultado['hosting'] or 'No detectado'} (confianza: {resultado['confianza']})")
    print(f"CMS:        {resultado['cms'] or 'No detectado'}")
    print(f"CDN:        {resultado['cdn'] or 'No detectado'}")

    if resultado["servicios_detectados"]:
        print(f"\nServicios detectados ({len(resultado['servicios_detectados'])}):")
        for srv in resultado["servicios_detectados"]:
            extra = f" — {srv['url_encontrada']}" if "url_encontrada" in srv else ""
            print(f"  - {srv['nombre']}{extra}")

    if resultado["plataformas_necesarias"]:
        print(f"\nPlataformas que necesitan credenciales ({len(resultado['plataformas_necesarias'])}):")
        for p in resultado["plataformas_necesarias"]:
            print(f"  - {p}")

    if proyecto and "credenciales_faltantes" in resultado:
        falt = resultado["credenciales_faltantes"]
        conf = resultado["credenciales_configuradas"]
        print(f"\nCredenciales para proyecto '{proyecto}':")
        for c in conf:
            print(f"  [OK] {c['nombre']}")
        for c in falt:
            print(f"  [FALTA] {c['nombre']}")
            print(f"          Campos: {', '.join(c['campos'])}")
            print(f"          {c['instrucciones']}")
