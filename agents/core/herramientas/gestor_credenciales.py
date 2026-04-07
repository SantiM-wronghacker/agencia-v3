"""
AREA: CEREBRO
DESCRIPCION: Vault seguro de credenciales por proyecto/cliente. Almacena API keys,
             tokens OAuth, credenciales FTP/SSH y mas, cifrados con Fernet (AES-128).
             Soporta todas las plataformas: hosting, redes sociales, email, CRM, ecommerce.
TECNOLOGIA: Python stdlib + cryptography (Fernet)
"""

import os
import sys
import json
import base64
import hashlib
from pathlib import Path
from datetime import datetime

# Intentar importar Fernet para cifrado real
try:
    from cryptography.fernet import Fernet
    CRYPTO_OK = True
except ImportError:
    CRYPTO_OK = False

BASE_DIR = Path(__file__).parent
VAULT_DIR = BASE_DIR / ".vault"
VAULT_FILE = VAULT_DIR / "credenciales.enc"
KEY_FILE = VAULT_DIR / ".vault_key"

# ─────────────────────────────────────────────────────────────────────────────
#  CATALOGO DE PLATAFORMAS: qué credenciales necesita cada una
# ─────────────────────────────────────────────────────────────────────────────

PLATAFORMAS = {
    # ── HOSTING WEB ──
    "github_pages": {
        "nombre": "GitHub Pages",
        "categoria": "hosting",
        "campos": ["token", "repo", "usuario"],
        "auth_tipo": "token",
        "acciones": ["push codigo", "deploy sitio", "crear PR", "editar archivos"],
        "instrucciones": "Genera un Personal Access Token en github.com/settings/tokens con permisos 'repo'",
    },
    "vercel": {
        "nombre": "Vercel",
        "categoria": "hosting",
        "campos": ["api_key", "team_id"],
        "auth_tipo": "api_key",
        "acciones": ["deploy", "ver logs", "configurar dominio"],
        "instrucciones": "Ve a vercel.com/account/tokens para generar un token",
    },
    "netlify": {
        "nombre": "Netlify",
        "categoria": "hosting",
        "campos": ["api_key", "site_id"],
        "auth_tipo": "api_key",
        "acciones": ["deploy", "configurar dominio", "ver analytics"],
        "instrucciones": "Ve a app.netlify.com/user/applications para crear un Personal access token",
    },
    "cpanel_ftp": {
        "nombre": "cPanel / FTP",
        "categoria": "hosting",
        "campos": ["host", "usuario", "password", "puerto"],
        "auth_tipo": "password",
        "acciones": ["subir archivos", "editar sitio", "gestionar BD"],
        "instrucciones": "Usa las credenciales FTP de tu hosting (Hostinger, GoDaddy, Namecheap, etc.)",
    },
    "firebase": {
        "nombre": "Firebase Hosting",
        "categoria": "hosting",
        "campos": ["project_id", "service_account_json"],
        "auth_tipo": "service_account",
        "acciones": ["deploy", "gestionar BD", "auth usuarios"],
        "instrucciones": "Descarga el JSON de Service Account desde console.firebase.google.com",
    },
    "aws_s3": {
        "nombre": "AWS S3",
        "categoria": "hosting",
        "campos": ["access_key", "secret_key", "bucket", "region"],
        "auth_tipo": "api_key",
        "acciones": ["subir archivos", "deploy sitio estatico", "gestionar bucket"],
        "instrucciones": "Crea un usuario IAM con permisos S3 en console.aws.amazon.com",
    },
    "wordpress": {
        "nombre": "WordPress",
        "categoria": "hosting",
        "campos": ["url_sitio", "usuario", "password_app"],
        "auth_tipo": "password",
        "acciones": ["crear posts", "editar paginas", "subir media", "gestionar plugins"],
        "instrucciones": "En WordPress ve a Usuarios > Tu perfil > Contrasenas de aplicacion para generar una",
    },
    "shopify": {
        "nombre": "Shopify",
        "categoria": "hosting",
        "campos": ["tienda_url", "api_key", "api_secret", "access_token"],
        "auth_tipo": "oauth",
        "acciones": ["gestionar productos", "editar tema", "ver pedidos", "gestionar inventario"],
        "instrucciones": "Crea una app privada en tu panel de Shopify > Configuracion > Apps",
    },

    # ── REDES SOCIALES ──
    "facebook_pages": {
        "nombre": "Facebook Pages",
        "categoria": "redes_sociales",
        "campos": ["page_id", "page_access_token", "app_id", "app_secret"],
        "auth_tipo": "oauth",
        "acciones": ["publicar posts", "responder mensajes", "responder comentarios", "ver estadisticas"],
        "instrucciones": "Crea una app en developers.facebook.com y genera un Page Access Token con permisos pages_manage_posts, pages_messaging",
    },
    "instagram": {
        "nombre": "Instagram Business",
        "categoria": "redes_sociales",
        "campos": ["instagram_account_id", "access_token", "app_id"],
        "auth_tipo": "oauth",
        "acciones": ["publicar fotos", "responder DMs", "responder comentarios", "ver insights"],
        "instrucciones": "Conecta tu cuenta de Instagram Business a Facebook y usa la Graph API. Necesitas permisos instagram_basic, instagram_manage_messages",
    },
    "twitter_x": {
        "nombre": "Twitter / X",
        "categoria": "redes_sociales",
        "campos": ["api_key", "api_secret", "access_token", "access_token_secret", "bearer_token"],
        "auth_tipo": "oauth",
        "acciones": ["publicar tweets", "responder", "dar like", "ver menciones"],
        "instrucciones": "Crea un proyecto en developer.twitter.com y genera las 4 claves de API",
    },
    "tiktok": {
        "nombre": "TikTok Business",
        "categoria": "redes_sociales",
        "campos": ["app_id", "app_secret", "access_token"],
        "auth_tipo": "oauth",
        "acciones": ["publicar videos", "ver estadisticas", "gestionar comentarios"],
        "instrucciones": "Registra tu app en developers.tiktok.com",
    },
    "linkedin": {
        "nombre": "LinkedIn",
        "categoria": "redes_sociales",
        "campos": ["client_id", "client_secret", "access_token"],
        "auth_tipo": "oauth",
        "acciones": ["publicar posts", "gestionar pagina empresa"],
        "instrucciones": "Crea una app en linkedin.com/developers",
    },

    # ── MENSAJERIA / CHAT ──
    "whatsapp_business": {
        "nombre": "WhatsApp Business API",
        "categoria": "mensajeria",
        "campos": ["phone_number_id", "access_token", "business_id", "webhook_verify_token"],
        "auth_tipo": "api_key",
        "acciones": ["enviar mensajes", "responder automatico", "enviar plantillas", "chatbot"],
        "instrucciones": "Configura WhatsApp Business API en business.facebook.com > WhatsApp. Necesitas verificar tu negocio.",
    },
    "telegram_bot": {
        "nombre": "Telegram Bot",
        "categoria": "mensajeria",
        "campos": ["bot_token", "chat_id"],
        "auth_tipo": "token",
        "acciones": ["enviar mensajes", "responder automatico", "chatbot", "enviar archivos"],
        "instrucciones": "Habla con @BotFather en Telegram para crear tu bot y obtener el token",
    },
    "messenger": {
        "nombre": "Facebook Messenger",
        "categoria": "mensajeria",
        "campos": ["page_id", "page_access_token", "app_id", "webhook_verify_token"],
        "auth_tipo": "oauth",
        "acciones": ["responder mensajes", "chatbot automatico", "enviar plantillas"],
        "instrucciones": "Usa el mismo token de Facebook Pages con permiso pages_messaging",
    },

    # ── EMAIL ──
    "gmail": {
        "nombre": "Gmail / Google Workspace",
        "categoria": "email",
        "campos": ["credentials_json", "token_json"],
        "auth_tipo": "oauth",
        "acciones": ["leer emails", "enviar emails", "responder automatico", "etiquetar"],
        "instrucciones": "Crea credenciales OAuth en console.cloud.google.com > APIs > Gmail API",
    },
    "outlook": {
        "nombre": "Outlook / Microsoft 365",
        "categoria": "email",
        "campos": ["client_id", "client_secret", "tenant_id", "refresh_token"],
        "auth_tipo": "oauth",
        "acciones": ["leer emails", "enviar emails", "responder automatico", "calendario"],
        "instrucciones": "Registra una app en portal.azure.com > Azure AD > App registrations",
    },
    "smtp_generico": {
        "nombre": "SMTP Generico",
        "categoria": "email",
        "campos": ["host", "puerto", "usuario", "password", "usar_tls"],
        "auth_tipo": "password",
        "acciones": ["enviar emails"],
        "instrucciones": "Usa los datos SMTP de tu proveedor de email",
    },
    "sendgrid": {
        "nombre": "SendGrid",
        "categoria": "email",
        "campos": ["api_key", "from_email"],
        "auth_tipo": "api_key",
        "acciones": ["enviar emails masivos", "campanas", "templates"],
        "instrucciones": "Genera una API key en app.sendgrid.com > Settings > API Keys",
    },
    "mailchimp": {
        "nombre": "Mailchimp",
        "categoria": "email",
        "campos": ["api_key", "server_prefix", "list_id"],
        "auth_tipo": "api_key",
        "acciones": ["campanas email", "gestionar listas", "automatizaciones"],
        "instrucciones": "Ve a mailchimp.com > Account > Extras > API Keys",
    },

    # ── CRM Y VENTAS ──
    "hubspot": {
        "nombre": "HubSpot",
        "categoria": "crm",
        "campos": ["api_key", "access_token"],
        "auth_tipo": "api_key",
        "acciones": ["gestionar contactos", "pipeline ventas", "automatizaciones", "email marketing"],
        "instrucciones": "Ve a Settings > Integrations > API key en tu cuenta HubSpot",
    },
    "pipedrive": {
        "nombre": "Pipedrive",
        "categoria": "crm",
        "campos": ["api_token", "company_domain"],
        "auth_tipo": "api_key",
        "acciones": ["gestionar deals", "contactos", "pipeline", "actividades"],
        "instrucciones": "Ve a Settings > Personal preferences > API en Pipedrive",
    },

    # ── ECOMMERCE ──
    "mercadolibre": {
        "nombre": "MercadoLibre",
        "categoria": "ecommerce",
        "campos": ["app_id", "client_secret", "access_token", "refresh_token"],
        "auth_tipo": "oauth",
        "acciones": ["publicar productos", "gestionar ventas", "responder preguntas", "ver metricas"],
        "instrucciones": "Crea una app en developers.mercadolibre.com.mx",
    },
    "stripe": {
        "nombre": "Stripe",
        "categoria": "ecommerce",
        "campos": ["secret_key", "publishable_key", "webhook_secret"],
        "auth_tipo": "api_key",
        "acciones": ["crear pagos", "suscripciones", "ver transacciones", "reembolsos"],
        "instrucciones": "Ve a dashboard.stripe.com/apikeys para obtener tus claves",
    },
    "paypal": {
        "nombre": "PayPal",
        "categoria": "ecommerce",
        "campos": ["client_id", "client_secret", "modo"],
        "auth_tipo": "oauth",
        "acciones": ["crear pagos", "ver transacciones", "suscripciones"],
        "instrucciones": "Crea una app en developer.paypal.com",
    },
    "woocommerce": {
        "nombre": "WooCommerce",
        "categoria": "ecommerce",
        "campos": ["url_tienda", "consumer_key", "consumer_secret"],
        "auth_tipo": "api_key",
        "acciones": ["gestionar productos", "pedidos", "cupones", "inventario"],
        "instrucciones": "En WordPress > WooCommerce > Ajustes > Avanzado > REST API para crear claves",
    },

    # ── PUBLICIDAD ──
    "google_ads": {
        "nombre": "Google Ads",
        "categoria": "publicidad",
        "campos": ["developer_token", "client_id", "client_secret", "refresh_token", "customer_id"],
        "auth_tipo": "oauth",
        "acciones": ["crear campanas", "gestionar anuncios", "ver metricas", "ajustar presupuesto"],
        "instrucciones": "Aplica para acceso a la API en ads.google.com/home/tools/manager-accounts/",
    },
    "meta_ads": {
        "nombre": "Meta Ads (Facebook/Instagram)",
        "categoria": "publicidad",
        "campos": ["ad_account_id", "access_token", "app_id", "app_secret"],
        "auth_tipo": "oauth",
        "acciones": ["crear campanas", "gestionar anuncios", "audiences", "ver metricas"],
        "instrucciones": "Usa el Business Manager en business.facebook.com para gestionar accesos",
    },

    # ── ANALYTICS ──
    "google_analytics": {
        "nombre": "Google Analytics",
        "categoria": "analytics",
        "campos": ["property_id", "credentials_json"],
        "auth_tipo": "service_account",
        "acciones": ["ver trafico", "reportes", "audiencias", "conversiones"],
        "instrucciones": "Crea un Service Account en console.cloud.google.com y dale acceso en Analytics",
    },

    # ── ALMACENAMIENTO ──
    "google_drive": {
        "nombre": "Google Drive",
        "categoria": "almacenamiento",
        "campos": ["credentials_json", "token_json", "folder_id"],
        "auth_tipo": "oauth",
        "acciones": ["subir archivos", "compartir", "organizar", "buscar documentos"],
        "instrucciones": "Habilita Google Drive API en console.cloud.google.com",
    },
    "dropbox": {
        "nombre": "Dropbox",
        "categoria": "almacenamiento",
        "campos": ["access_token", "app_key", "app_secret"],
        "auth_tipo": "oauth",
        "acciones": ["subir archivos", "compartir", "sincronizar"],
        "instrucciones": "Crea una app en dropbox.com/developers",
    },

    # ── DNS / DOMINIOS ──
    "cloudflare": {
        "nombre": "Cloudflare",
        "categoria": "dns",
        "campos": ["api_token", "zone_id", "email"],
        "auth_tipo": "api_key",
        "acciones": ["gestionar DNS", "SSL", "cache", "firewall", "workers"],
        "instrucciones": "Ve a dash.cloudflare.com > My Profile > API Tokens",
    },
}


# ─────────────────────────────────────────────────────────────────────────────
#  CIFRADO
# ─────────────────────────────────────────────────────────────────────────────

def _generar_clave():
    """Genera o lee la clave maestra del vault."""
    VAULT_DIR.mkdir(parents=True, exist_ok=True)

    if KEY_FILE.exists():
        return KEY_FILE.read_bytes()

    if CRYPTO_OK:
        clave = Fernet.generate_key()
    else:
        # Fallback: derivar de un secreto local
        seed = f"{os.getlogin()}-agencia-santi-{BASE_DIR}".encode()
        clave = base64.urlsafe_b64encode(hashlib.sha256(seed).digest())

    KEY_FILE.write_bytes(clave)

    # Proteger el archivo en Windows
    try:
        import subprocess
        subprocess.run(
            ["icacls", str(KEY_FILE), "/inheritance:r", "/grant:r",
             f"{os.getlogin()}:F"],
            capture_output=True, timeout=5
        )
    except Exception:
        pass

    return clave


def _cifrar(data: str) -> bytes:
    clave = _generar_clave()
    if CRYPTO_OK:
        f = Fernet(clave)
        return f.encrypt(data.encode("utf-8"))
    else:
        # Fallback: base64 + XOR simple (no produccion, pero funcional)
        encoded = base64.b64encode(data.encode("utf-8"))
        key_bytes = clave[:len(encoded)]
        xored = bytes(a ^ b for a, b in zip(encoded, key_bytes * (len(encoded) // len(key_bytes) + 1)))
        return base64.b64encode(xored)


def _descifrar(data: bytes) -> str:
    clave = _generar_clave()
    if CRYPTO_OK:
        f = Fernet(clave)
        return f.decrypt(data).decode("utf-8")
    else:
        xored = base64.b64decode(data)
        key_bytes = clave[:len(xored)]
        decoded = bytes(a ^ b for a, b in zip(xored, key_bytes * (len(xored) // len(key_bytes) + 1)))
        return base64.b64decode(decoded).decode("utf-8")


# ─────────────────────────────────────────────────────────────────────────────
#  OPERACIONES DEL VAULT
# ─────────────────────────────────────────────────────────────────────────────

def _cargar_vault() -> dict:
    """Carga y descifra el vault completo."""
    if not VAULT_FILE.exists():
        return {"proyectos": {}}
    try:
        data_enc = VAULT_FILE.read_bytes()
        data_json = _descifrar(data_enc)
        return json.loads(data_json)
    except Exception:
        return {"proyectos": {}}


def _guardar_vault(vault: dict):
    """Cifra y guarda el vault."""
    VAULT_DIR.mkdir(parents=True, exist_ok=True)
    data_json = json.dumps(vault, indent=2, ensure_ascii=False)
    data_enc = _cifrar(data_json)
    VAULT_FILE.write_bytes(data_enc)


def guardar_credencial(proyecto: str, plataforma: str, credenciales: dict) -> dict:
    """
    Guarda credenciales para un proyecto+plataforma.
    Retorna: {"exito": True/False, "mensaje": "..."}
    """
    if plataforma not in PLATAFORMAS:
        return {"exito": False, "mensaje": f"Plataforma '{plataforma}' no reconocida. Usa listar_plataformas()"}

    info_plat = PLATAFORMAS[plataforma]
    campos_req = info_plat["campos"]
    faltantes = [c for c in campos_req if c not in credenciales or not str(credenciales[c]).strip()]

    if faltantes:
        return {
            "exito": False,
            "mensaje": f"Faltan campos para {info_plat['nombre']}: {', '.join(faltantes)}",
            "campos_requeridos": campos_req,
            "instrucciones": info_plat["instrucciones"],
        }

    vault = _cargar_vault()

    if proyecto not in vault["proyectos"]:
        vault["proyectos"][proyecto] = {}

    vault["proyectos"][proyecto][plataforma] = {
        "credenciales": credenciales,
        "plataforma_nombre": info_plat["nombre"],
        "categoria": info_plat["categoria"],
        "fecha_guardado": datetime.now().isoformat(),
        "activo": True,
    }

    _guardar_vault(vault)

    return {
        "exito": True,
        "mensaje": f"Credenciales de {info_plat['nombre']} guardadas para proyecto '{proyecto}'",
        "acciones_disponibles": info_plat["acciones"],
    }


def obtener_credencial(proyecto: str, plataforma: str) -> dict | None:
    """Obtiene credenciales descifradas para un proyecto+plataforma."""
    vault = _cargar_vault()
    proy = vault.get("proyectos", {}).get(proyecto, {})
    entry = proy.get(plataforma)
    if not entry or not entry.get("activo"):
        return None
    return entry.get("credenciales")


def tiene_credencial(proyecto: str, plataforma: str) -> bool:
    """Verifica si existen credenciales para un proyecto+plataforma."""
    return obtener_credencial(proyecto, plataforma) is not None


def listar_credenciales_proyecto(proyecto: str) -> list[dict]:
    """Lista todas las credenciales configuradas para un proyecto (sin datos sensibles)."""
    vault = _cargar_vault()
    proy = vault.get("proyectos", {}).get(proyecto, {})
    resultado = []
    for plat_id, entry in proy.items():
        resultado.append({
            "plataforma": plat_id,
            "nombre": entry.get("plataforma_nombre", plat_id),
            "categoria": entry.get("categoria", ""),
            "activo": entry.get("activo", False),
            "fecha": entry.get("fecha_guardado", ""),
            "campos_guardados": list(entry.get("credenciales", {}).keys()),
        })
    return resultado


def eliminar_credencial(proyecto: str, plataforma: str) -> dict:
    """Elimina credenciales de un proyecto+plataforma."""
    vault = _cargar_vault()
    proy = vault.get("proyectos", {}).get(proyecto, {})
    if plataforma in proy:
        del proy[plataforma]
        _guardar_vault(vault)
        return {"exito": True, "mensaje": f"Credenciales de {plataforma} eliminadas"}
    return {"exito": False, "mensaje": "No encontrada"}


def credenciales_faltantes(proyecto: str, accion: str) -> list[dict]:
    """
    Dada una accion deseada, detecta qué plataformas necesitan credenciales.
    Ejemplo: accion="publicar en facebook" -> necesita facebook_pages
    """
    accion_lower = accion.lower()
    necesarias = []

    MAPA_ACCIONES = {
        "facebook":   ["facebook_pages", "messenger"],
        "instagram":  ["instagram"],
        "twitter":    ["twitter_x"],
        "tweet":      ["twitter_x"],
        "tiktok":     ["tiktok"],
        "linkedin":   ["linkedin"],
        "whatsapp":   ["whatsapp_business"],
        "telegram":   ["telegram_bot"],
        "messenger":  ["messenger"],
        "email":      ["gmail", "outlook", "smtp_generico"],
        "correo":     ["gmail", "outlook", "smtp_generico"],
        "gmail":      ["gmail"],
        "outlook":    ["outlook"],
        "sitio web":  ["github_pages", "cpanel_ftp", "vercel", "wordpress"],
        "pagina web": ["github_pages", "cpanel_ftp", "vercel", "wordpress"],
        "website":    ["github_pages", "cpanel_ftp", "vercel", "wordpress"],
        "deploy":     ["github_pages", "vercel", "netlify", "aws_s3"],
        "wordpress":  ["wordpress"],
        "shopify":    ["shopify"],
        "tienda":     ["shopify", "woocommerce", "mercadolibre"],
        "mercadolibre": ["mercadolibre"],
        "stripe":     ["stripe"],
        "paypal":     ["paypal"],
        "pago":       ["stripe", "paypal"],
        "anuncio":    ["meta_ads", "google_ads"],
        "campana":    ["meta_ads", "google_ads", "mailchimp"],
        "analytics":  ["google_analytics"],
        "drive":      ["google_drive"],
        "dropbox":    ["dropbox"],
        "dns":        ["cloudflare"],
        "dominio":    ["cloudflare"],
        "crm":        ["hubspot", "pipedrive"],
        "contacto":   ["hubspot", "pipedrive"],
        "mailchimp":  ["mailchimp"],
        "sendgrid":   ["sendgrid"],
    }

    plataformas_detectadas = set()
    for keyword, plats in MAPA_ACCIONES.items():
        if keyword in accion_lower:
            plataformas_detectadas.update(plats)

    for plat_id in plataformas_detectadas:
        if not tiene_credencial(proyecto, plat_id):
            info = PLATAFORMAS[plat_id]
            necesarias.append({
                "plataforma": plat_id,
                "nombre": info["nombre"],
                "campos_requeridos": info["campos"],
                "instrucciones": info["instrucciones"],
                "auth_tipo": info["auth_tipo"],
            })

    return necesarias


def listar_plataformas(categoria: str = None) -> list[dict]:
    """Lista todas las plataformas soportadas, opcionalmente filtradas por categoria."""
    resultado = []
    for plat_id, info in PLATAFORMAS.items():
        if categoria and info["categoria"] != categoria:
            continue
        resultado.append({
            "id": plat_id,
            "nombre": info["nombre"],
            "categoria": info["categoria"],
            "campos": info["campos"],
            "acciones": info["acciones"],
            "auth_tipo": info["auth_tipo"],
        })
    return resultado


def listar_categorias_plataformas() -> dict:
    """Devuelve resumen de categorias de plataformas soportadas."""
    cats = {}
    for info in PLATAFORMAS.values():
        cat = info["categoria"]
        cats[cat] = cats.get(cat, 0) + 1
    return cats


# ─────────────────────────────────────────────────────────────────────────────
#  CLI
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    args = sys.argv[1:]

    if not args or args[0] == "--help":
        print("Gestor de Credenciales — Agencia Santi")
        print()
        print("Uso:")
        print("  --listar-plataformas [categoria]    Lista plataformas soportadas")
        print("  --listar <proyecto>                 Lista credenciales de un proyecto")
        print("  --guardar <proyecto> <plataforma>   Guarda credenciales (modo interactivo)")
        print("  --verificar <proyecto> <accion>     Verifica que credenciales faltan")
        print("  --eliminar <proyecto> <plataforma>  Elimina credenciales")
        sys.exit(0)

    cmd = args[0]

    if cmd == "--listar-plataformas":
        cat = args[1] if len(args) > 1 else None
        plats = listar_plataformas(cat)
        cats = listar_categorias_plataformas()
        print(f"Plataformas soportadas: {len(plats)}")
        print(f"Categorias: {json.dumps(cats, ensure_ascii=False)}")
        print()
        for p in plats:
            print(f"  [{p['categoria']}] {p['nombre']} ({p['id']})")
            print(f"    Auth: {p['auth_tipo']} | Campos: {', '.join(p['campos'])}")
            print(f"    Acciones: {', '.join(p['acciones'])}")
            print()

    elif cmd == "--listar" and len(args) > 1:
        proyecto = args[1]
        creds = listar_credenciales_proyecto(proyecto)
        if not creds:
            print(f"No hay credenciales guardadas para '{proyecto}'")
        else:
            print(f"Credenciales de '{proyecto}' ({len(creds)}):")
            for c in creds:
                estado = "ACTIVA" if c["activo"] else "INACTIVA"
                print(f"  [{estado}] {c['nombre']} — campos: {', '.join(c['campos_guardados'])}")

    elif cmd == "--guardar" and len(args) > 2:
        proyecto = args[1]
        plataforma = args[2]
        if plataforma not in PLATAFORMAS:
            print(f"Plataforma '{plataforma}' no reconocida")
            sys.exit(1)
        info = PLATAFORMAS[plataforma]
        print(f"Configurar {info['nombre']} para proyecto '{proyecto}'")
        print(f"Instrucciones: {info['instrucciones']}")
        print()
        credenciales = {}
        for campo in info["campos"]:
            valor = input(f"  {campo}: ").strip()
            if valor:
                credenciales[campo] = valor
        resultado = guardar_credencial(proyecto, plataforma, credenciales)
        print(resultado["mensaje"])

    elif cmd == "--verificar" and len(args) > 2:
        proyecto = args[1]
        accion = " ".join(args[2:])
        faltantes = credenciales_faltantes(proyecto, accion)
        if not faltantes:
            print(f"Todas las credenciales necesarias para '{accion}' estan configuradas")
        else:
            print(f"Credenciales faltantes para '{accion}':")
            for f in faltantes:
                print(f"  {f['nombre']} ({f['plataforma']})")
                print(f"    Campos: {', '.join(f['campos_requeridos'])}")
                print(f"    Como obtenerlas: {f['instrucciones']}")
                print()

    elif cmd == "--eliminar" and len(args) > 2:
        resultado = eliminar_credencial(args[1], args[2])
        print(resultado["mensaje"])
