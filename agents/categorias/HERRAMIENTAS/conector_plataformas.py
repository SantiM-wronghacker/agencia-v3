"""
AREA: CEREBRO
DESCRIPCION: Conector universal de APIs externas. Ejecuta acciones reales en plataformas
             usando credenciales del vault: publicar en redes, responder mensajes, deploy
             a hosting, enviar emails, gestionar ecommerce, etc.
TECNOLOGIA: Python stdlib (urllib, json, smtplib, ftplib)
"""

import os
import sys
import json
import ftplib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent

# Importar gestor de credenciales
sys.path.insert(0, str(BASE_DIR))
from gestor_credenciales import obtener_credencial, tiene_credencial, credenciales_faltantes, PLATAFORMAS


# ─────────────────────────────────────────────────────────────────────────────
#  UTILIDADES HTTP
# ─────────────────────────────────────────────────────────────────────────────

def _api_call(url: str, method: str = "GET", data: dict = None,
              headers: dict = None, token: str = None) -> dict:
    """Llamada HTTP generica a API externa."""
    hdrs = {"Content-Type": "application/json", "User-Agent": "AgenciaSanti/1.0"}
    if token:
        hdrs["Authorization"] = f"Bearer {token}"
    if headers:
        hdrs.update(headers)

    body_bytes = None
    if data:
        body_bytes = json.dumps(data).encode("utf-8")

    req = Request(url, data=body_bytes, headers=hdrs, method=method)
    try:
        resp = urlopen(req, timeout=30)
        resp_body = resp.read().decode("utf-8", errors="replace")
        try:
            return {"ok": True, "status": resp.status, "data": json.loads(resp_body)}
        except json.JSONDecodeError:
            return {"ok": True, "status": resp.status, "data": resp_body}
    except HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        return {"ok": False, "status": e.code, "error": body[:500]}
    except Exception as e:
        return {"ok": False, "status": 0, "error": str(e)}


# ─────────────────────────────────────────────────────────────────────────────
#  CONECTORES POR PLATAFORMA
# ─────────────────────────────────────────────────────────────────────────────

# ── FACEBOOK PAGES ──

def facebook_publicar(proyecto: str, mensaje: str, link: str = None) -> dict:
    """Publica un post en la pagina de Facebook del proyecto."""
    creds = obtener_credencial(proyecto, "facebook_pages")
    if not creds:
        return {"ok": False, "error": "Sin credenciales de Facebook Pages", "necesita": "facebook_pages"}

    page_id = creds["page_id"]
    token = creds["page_access_token"]
    data = {"message": mensaje, "access_token": token}
    if link:
        data["link"] = link

    return _api_call(
        f"https://graph.facebook.com/v18.0/{page_id}/feed",
        method="POST", data=data
    )


def facebook_responder_mensajes(proyecto: str) -> dict:
    """Lee mensajes no leidos de la pagina y genera respuestas."""
    creds = obtener_credencial(proyecto, "facebook_pages")
    if not creds:
        return {"ok": False, "error": "Sin credenciales de Facebook Pages"}

    page_id = creds["page_id"]
    token = creds["page_access_token"]

    # Leer conversaciones
    result = _api_call(
        f"https://graph.facebook.com/v18.0/{page_id}/conversations?fields=messages{{message,from,created_time}}&access_token={token}"
    )
    return result


def facebook_enviar_mensaje(proyecto: str, recipient_id: str, texto: str) -> dict:
    """Envia un mensaje via Messenger de la pagina."""
    creds = obtener_credencial(proyecto, "facebook_pages")
    if not creds:
        return {"ok": False, "error": "Sin credenciales de Facebook Pages"}

    token = creds["page_access_token"]
    data = {
        "recipient": {"id": recipient_id},
        "message": {"text": texto},
        "access_token": token,
    }
    return _api_call(
        "https://graph.facebook.com/v18.0/me/messages",
        method="POST", data=data
    )


# ── INSTAGRAM ──

def instagram_publicar(proyecto: str, image_url: str, caption: str) -> dict:
    """Publica una foto en Instagram Business."""
    creds = obtener_credencial(proyecto, "instagram")
    if not creds:
        return {"ok": False, "error": "Sin credenciales de Instagram"}

    ig_id = creds["instagram_account_id"]
    token = creds["access_token"]

    # Paso 1: crear media container
    container = _api_call(
        f"https://graph.facebook.com/v18.0/{ig_id}/media",
        method="POST",
        data={"image_url": image_url, "caption": caption, "access_token": token}
    )
    if not container.get("ok"):
        return container

    creation_id = container["data"].get("id")
    if not creation_id:
        return {"ok": False, "error": "No se obtuvo creation_id"}

    # Paso 2: publicar
    return _api_call(
        f"https://graph.facebook.com/v18.0/{ig_id}/media_publish",
        method="POST",
        data={"creation_id": creation_id, "access_token": token}
    )


# ── WHATSAPP BUSINESS ──

def whatsapp_enviar(proyecto: str, telefono: str, mensaje: str) -> dict:
    """Envia un mensaje de WhatsApp Business."""
    creds = obtener_credencial(proyecto, "whatsapp_business")
    if not creds:
        return {"ok": False, "error": "Sin credenciales de WhatsApp Business"}

    phone_id = creds["phone_number_id"]
    token = creds["access_token"]

    data = {
        "messaging_product": "whatsapp",
        "to": telefono,
        "type": "text",
        "text": {"body": mensaje},
    }
    return _api_call(
        f"https://graph.facebook.com/v18.0/{phone_id}/messages",
        method="POST", data=data, token=token
    )


# ── TELEGRAM ──

def telegram_enviar(proyecto: str, mensaje: str, chat_id: str = None) -> dict:
    """Envia un mensaje via Telegram Bot."""
    creds = obtener_credencial(proyecto, "telegram_bot")
    if not creds:
        return {"ok": False, "error": "Sin credenciales de Telegram Bot"}

    bot_token = creds["bot_token"]
    cid = chat_id or creds.get("chat_id", "")

    return _api_call(
        f"https://api.telegram.org/bot{bot_token}/sendMessage",
        method="POST",
        data={"chat_id": cid, "text": mensaje, "parse_mode": "HTML"}
    )


# ── EMAIL (SMTP) ──

def email_enviar(proyecto: str, destinatario: str, asunto: str, cuerpo: str,
                 plataforma: str = "smtp_generico") -> dict:
    """Envia un email usando SMTP."""
    creds = obtener_credencial(proyecto, plataforma)
    if not creds:
        # Intentar gmail, outlook, smtp_generico en ese orden
        for alt in ["gmail", "outlook", "smtp_generico", "sendgrid"]:
            creds = obtener_credencial(proyecto, alt)
            if creds:
                plataforma = alt
                break
        if not creds:
            return {"ok": False, "error": "Sin credenciales de email configuradas"}

    if plataforma == "sendgrid":
        return _sendgrid_enviar(creds, destinatario, asunto, cuerpo)

    # SMTP generico / Gmail / Outlook
    host = creds.get("host", "smtp.gmail.com")
    puerto = int(creds.get("puerto", 587))
    usuario = creds.get("usuario", "")
    password = creds.get("password", "")
    usar_tls = str(creds.get("usar_tls", "true")).lower() in ("true", "1", "si")

    msg = MIMEMultipart()
    msg["From"] = usuario
    msg["To"] = destinatario
    msg["Subject"] = asunto
    msg.attach(MIMEText(cuerpo, "html"))

    try:
        if usar_tls:
            server = smtplib.SMTP(host, puerto, timeout=15)
            server.starttls()
        else:
            server = smtplib.SMTP_SSL(host, puerto, timeout=15)
        server.login(usuario, password)
        server.sendmail(usuario, destinatario, msg.as_string())
        server.quit()
        return {"ok": True, "mensaje": f"Email enviado a {destinatario}"}
    except Exception as e:
        return {"ok": False, "error": f"Error SMTP: {e}"}


def _sendgrid_enviar(creds: dict, destinatario: str, asunto: str, cuerpo: str) -> dict:
    """Envia via SendGrid API."""
    data = {
        "personalizations": [{"to": [{"email": destinatario}]}],
        "from": {"email": creds.get("from_email", "")},
        "subject": asunto,
        "content": [{"type": "text/html", "value": cuerpo}],
    }
    return _api_call(
        "https://api.sendgrid.com/v3/mail/send",
        method="POST", data=data, token=creds["api_key"]
    )


# ── FTP / CPANEL ──

def ftp_subir_archivo(proyecto: str, archivo_local: str, ruta_remota: str) -> dict:
    """Sube un archivo via FTP."""
    creds = obtener_credencial(proyecto, "cpanel_ftp")
    if not creds:
        return {"ok": False, "error": "Sin credenciales FTP"}

    try:
        ftp = ftplib.FTP()
        ftp.connect(creds["host"], int(creds.get("puerto", 21)), timeout=15)
        ftp.login(creds["usuario"], creds["password"])

        with open(archivo_local, "rb") as f:
            ftp.storbinary(f"STOR {ruta_remota}", f)

        ftp.quit()
        return {"ok": True, "mensaje": f"Archivo subido a {ruta_remota}"}
    except Exception as e:
        return {"ok": False, "error": f"Error FTP: {e}"}


def ftp_subir_directorio(proyecto: str, dir_local: str, dir_remoto: str) -> dict:
    """Sube un directorio completo via FTP."""
    creds = obtener_credencial(proyecto, "cpanel_ftp")
    if not creds:
        return {"ok": False, "error": "Sin credenciales FTP"}

    try:
        ftp = ftplib.FTP()
        ftp.connect(creds["host"], int(creds.get("puerto", 21)), timeout=30)
        ftp.login(creds["usuario"], creds["password"])

        subidos = 0
        errores = 0
        local_path = Path(dir_local)

        for archivo in local_path.rglob("*"):
            if archivo.is_file():
                rel = archivo.relative_to(local_path)
                remoto = f"{dir_remoto}/{rel.as_posix()}"

                # Crear directorios remotos
                partes = remoto.rsplit("/", 1)
                if len(partes) > 1:
                    try:
                        ftp.mkd(partes[0])
                    except Exception:
                        pass

                try:
                    with open(archivo, "rb") as f:
                        ftp.storbinary(f"STOR {remoto}", f)
                    subidos += 1
                except Exception:
                    errores += 1

        ftp.quit()
        return {"ok": True, "mensaje": f"Subidos {subidos} archivos ({errores} errores)", "subidos": subidos}
    except Exception as e:
        return {"ok": False, "error": f"Error FTP: {e}"}


# ── WORDPRESS ──

def wordpress_crear_post(proyecto: str, titulo: str, contenido: str,
                         status: str = "draft") -> dict:
    """Crea un post en WordPress via REST API."""
    creds = obtener_credencial(proyecto, "wordpress")
    if not creds:
        return {"ok": False, "error": "Sin credenciales de WordPress"}

    url_base = creds["url_sitio"].rstrip("/")
    import base64
    auth = base64.b64encode(
        f"{creds['usuario']}:{creds['password_app']}".encode()
    ).decode()

    return _api_call(
        f"{url_base}/wp-json/wp/v2/posts",
        method="POST",
        data={"title": titulo, "content": contenido, "status": status},
        headers={"Authorization": f"Basic {auth}"}
    )


def wordpress_editar_pagina(proyecto: str, page_id: int, contenido: str) -> dict:
    """Edita una pagina existente en WordPress."""
    creds = obtener_credencial(proyecto, "wordpress")
    if not creds:
        return {"ok": False, "error": "Sin credenciales de WordPress"}

    url_base = creds["url_sitio"].rstrip("/")
    import base64
    auth = base64.b64encode(
        f"{creds['usuario']}:{creds['password_app']}".encode()
    ).decode()

    return _api_call(
        f"{url_base}/wp-json/wp/v2/pages/{page_id}",
        method="POST",
        data={"content": contenido},
        headers={"Authorization": f"Basic {auth}"}
    )


# ── GITHUB PAGES ──

def github_push_file(proyecto: str, ruta_archivo: str, contenido: str,
                     mensaje_commit: str = "Update via Agencia Santi") -> dict:
    """Sube/actualiza un archivo en GitHub repo."""
    creds = obtener_credencial(proyecto, "github_pages")
    if not creds:
        return {"ok": False, "error": "Sin credenciales de GitHub"}

    import base64
    repo = creds["repo"]  # "usuario/repo"
    token = creds["token"]

    # Obtener SHA actual si el archivo existe
    check = _api_call(
        f"https://api.github.com/repos/{repo}/contents/{ruta_archivo}",
        token=token
    )
    sha = check.get("data", {}).get("sha") if check.get("ok") else None

    data = {
        "message": mensaje_commit,
        "content": base64.b64encode(contenido.encode("utf-8")).decode(),
    }
    if sha:
        data["sha"] = sha

    return _api_call(
        f"https://api.github.com/repos/{repo}/contents/{ruta_archivo}",
        method="PUT", data=data, token=token
    )


# ── MERCADOLIBRE ──

def mercadolibre_publicar(proyecto: str, titulo: str, precio: float,
                          categoria_id: str, descripcion: str = "") -> dict:
    """Publica un producto en MercadoLibre."""
    creds = obtener_credencial(proyecto, "mercadolibre")
    if not creds:
        return {"ok": False, "error": "Sin credenciales de MercadoLibre"}

    token = creds["access_token"]
    data = {
        "title": titulo,
        "price": precio,
        "category_id": categoria_id,
        "currency_id": "MXN",
        "available_quantity": 1,
        "buying_mode": "buy_it_now",
        "listing_type_id": "gold_special",
        "condition": "new",
    }
    if descripcion:
        data["description"] = {"plain_text": descripcion}

    return _api_call(
        "https://api.mercadolibre.com/items",
        method="POST", data=data, token=token
    )


# ─────────────────────────────────────────────────────────────────────────────
#  DISPATCHER: ejecuta accion segun plataforma
# ─────────────────────────────────────────────────────────────────────────────

ACCIONES = {
    "facebook_publicar":     facebook_publicar,
    "facebook_responder":    facebook_responder_mensajes,
    "facebook_mensaje":      facebook_enviar_mensaje,
    "instagram_publicar":    instagram_publicar,
    "whatsapp_enviar":       whatsapp_enviar,
    "telegram_enviar":       telegram_enviar,
    "email_enviar":          email_enviar,
    "ftp_subir":             ftp_subir_archivo,
    "ftp_subir_directorio":  ftp_subir_directorio,
    "wordpress_post":        wordpress_crear_post,
    "wordpress_editar":      wordpress_editar_pagina,
    "github_push":           github_push_file,
    "mercadolibre_publicar": mercadolibre_publicar,
}


def ejecutar_accion(proyecto: str, accion: str, **kwargs) -> dict:
    """
    Ejecuta una accion en una plataforma externa.
    Primero verifica credenciales, luego ejecuta.
    """
    if accion not in ACCIONES:
        return {
            "ok": False,
            "error": f"Accion '{accion}' no reconocida",
            "acciones_disponibles": list(ACCIONES.keys()),
        }

    fn = ACCIONES[accion]
    try:
        return fn(proyecto, **kwargs)
    except TypeError as e:
        return {"ok": False, "error": f"Parametros incorrectos: {e}"}
    except Exception as e:
        return {"ok": False, "error": f"Error ejecutando {accion}: {e}"}


def verificar_y_ejecutar(proyecto: str, descripcion_tarea: str) -> dict:
    """
    Verifica credenciales necesarias para una tarea.
    Si faltan, retorna que credenciales necesita.
    Si estan completas, indica que puede proceder.
    """
    faltantes = credenciales_faltantes(proyecto, descripcion_tarea)

    if faltantes:
        return {
            "puede_ejecutar": False,
            "credenciales_faltantes": faltantes,
            "mensaje": f"Para ejecutar esta tarea necesito que configures {len(faltantes)} plataforma(s):",
            "plataformas": [f["nombre"] for f in faltantes],
        }

    return {
        "puede_ejecutar": True,
        "mensaje": "Todas las credenciales estan configuradas. Puedo proceder.",
    }


# ─────────────────────────────────────────────────────────────────────────────
#  CLI
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    args = sys.argv[1:]

    if not args or args[0] == "--help":
        print("Conector de Plataformas — Agencia Santi")
        print()
        print("Uso:")
        print("  --acciones                          Lista acciones disponibles")
        print("  --verificar <proyecto> <tarea>       Verifica credenciales para una tarea")
        print("  --ejecutar <proyecto> <accion> ...   Ejecuta una accion")
        sys.exit(0)

    if args[0] == "--acciones":
        print("Acciones disponibles:")
        for nombre in sorted(ACCIONES.keys()):
            fn = ACCIONES[nombre]
            doc = (fn.__doc__ or "").strip().split("\n")[0]
            print(f"  {nombre}: {doc}")

    elif args[0] == "--verificar" and len(args) > 2:
        proyecto = args[1]
        tarea = " ".join(args[2:])
        resultado = verificar_y_ejecutar(proyecto, tarea)
        print(resultado["mensaje"])
        if not resultado["puede_ejecutar"]:
            for f in resultado["credenciales_faltantes"]:
                print(f"  [{f['plataforma']}] {f['nombre']}")
                print(f"    Campos: {', '.join(f['campos_requeridos'])}")
                print(f"    {f['instrucciones']}")
                print()
