from tools.base import BaseTool, ToolResult, tool

_BASE = "https://api.dropboxapi.com/2"
_CONTENT_BASE = "https://content.dropboxapi.com/2"


@tool
class DropboxTool(BaseTool):
    name = "dropbox"
    description = (
        "Gestiona archivos en Dropbox. "
        "Úsala para subir y compartir archivos "
        "con clientes que usan Dropbox."
    )

    def run(self, action: str = "", **kwargs) -> ToolResult:
        if action == "upload":
            return self._upload(**kwargs)
        if action == "download":
            return self._download(**kwargs)
        if action == "list":
            return self._list(**kwargs)
        if action == "share":
            return self._share(**kwargs)
        return self._error(f"Acción '{action}' no soportada")

    def _get_headers(self):
        token = self.credentials.get("access_token")
        if not token:
            return None
        return {"Authorization": f"Bearer {token}"}

    def _upload(self, file_path: str = "", dropbox_path: str = None) -> ToolResult:
        headers = self._get_headers()
        if not headers:
            return self._error("Credencial Dropbox no configurada: access_token")
        from pathlib import Path
        p = Path(file_path)
        if not p.exists():
            return self._error(f"Archivo no encontrado: {file_path}")
        db_path = dropbox_path or f"/{p.name}"
        import httpx, json as _json
        try:
            with open(file_path, "rb") as f:
                content = f.read()
            r = httpx.post(
                f"{_CONTENT_BASE}/files/upload",
                content=content,
                headers={
                    **headers,
                    "Content-Type": "application/octet-stream",
                    "Dropbox-API-Arg": _json.dumps({"path": db_path, "mode": "overwrite"}),
                },
                timeout=60,
            )
            r.raise_for_status()
            data = r.json()
            return self._success(
                f"Archivo subido a Dropbox: {data.get('path_display', db_path)}",
                raw_data=data,
            )
        except Exception as e:
            return self._error(f"Error subiendo a Dropbox: {e}")

    def _download(self, dropbox_path: str = "", destination: str = ".") -> ToolResult:
        headers = self._get_headers()
        if not headers:
            return self._error("Credencial Dropbox no configurada")
        import httpx, os, json as _json
        try:
            r = httpx.post(
                f"{_CONTENT_BASE}/files/download",
                headers={
                    **headers,
                    "Dropbox-API-Arg": _json.dumps({"path": dropbox_path}),
                },
                timeout=60,
            )
            r.raise_for_status()
            filename = os.path.basename(dropbox_path)
            out_path = os.path.join(destination, filename)
            with open(out_path, "wb") as f:
                f.write(r.content)
            return self._success(
                f"Archivo descargado: {out_path}",
                raw_data={"path": out_path},
            )
        except Exception as e:
            return self._error(f"Error descargando de Dropbox: {e}")

    def _list(self, folder_path: str = "") -> ToolResult:
        headers = self._get_headers()
        if not headers:
            return self._error("Credencial Dropbox no configurada")
        import httpx
        try:
            r = httpx.post(
                f"{_BASE}/files/list_folder",
                json={"path": folder_path},
                headers={**headers, "Content-Type": "application/json"},
                timeout=15,
            )
            r.raise_for_status()
            entries = r.json().get("entries", [])
            lines = [f"- {e['name']} ({e['.tag']})" for e in entries]
            return self._success(
                "\n".join(lines) if lines else "Carpeta vacía",
                raw_data={"entries": entries},
            )
        except Exception as e:
            return self._error(f"Error listando Dropbox: {e}")

    def _share(self, dropbox_path: str = "") -> ToolResult:
        headers = self._get_headers()
        if not headers:
            return self._error("Credencial Dropbox no configurada")
        import httpx
        try:
            r = httpx.post(
                f"{_BASE}/sharing/create_shared_link_with_settings",
                json={"path": dropbox_path, "settings": {"requested_visibility": "public"}},
                headers={**headers, "Content-Type": "application/json"},
                timeout=15,
            )
            r.raise_for_status()
            url = r.json().get("url", "")
            return self._success(
                f"Link compartido: {url}",
                raw_data={"url": url},
            )
        except Exception as e:
            return self._error(f"Error creando link: {e}")
