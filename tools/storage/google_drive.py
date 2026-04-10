from pathlib import Path

from tools.base import BaseTool, ToolResult, tool


@tool
class GoogleDriveTool(BaseTool):
    name = "google_drive"
    description = (
        "Gestiona archivos en Google Drive. "
        "Úsala para subir reportes, documentos "
        "y compartir archivos con clientes."
    )

    def run(self, action: str = "", **kwargs) -> ToolResult:
        if action == "upload":
            return self._upload(**kwargs)
        if action == "download":
            return self._download(**kwargs)
        if action == "list":
            return self._list(**kwargs)
        if action == "create_folder":
            return self._create_folder(**kwargs)
        return self._error(f"Acción '{action}' no soportada")

    def _get_service(self):
        try:
            from google.oauth2 import service_account
            from googleapiclient.discovery import build
            creds = service_account.Credentials.from_service_account_file(
                self.credentials["service_account_json"],
                scopes=["https://www.googleapis.com/auth/drive"],
            )
            return build("drive", "v3", credentials=creds)
        except ImportError:
            return None
        except Exception:
            return None

    def _upload(
        self,
        file_path: str = "",
        folder_id: str = None,
        file_name: str = None,
    ) -> ToolResult:
        if not self.credentials.get("service_account_json"):
            return self._error(
                "Credencial Google Drive no configurada: service_account_json"
            )
        p = Path(file_path)
        if not p.exists():
            return self._error(f"Archivo no encontrado: {file_path}")
        service = self._get_service()
        if not service:
            return self._error(
                "Error conectando a Google Drive. "
                "Verifica service_account_json y que google-api-python-client esté instalado."
            )
        try:
            from googleapiclient.http import MediaFileUpload
            import mimetypes
            name = file_name or p.name
            ct = mimetypes.guess_type(file_path)[0] or "application/octet-stream"
            metadata = {"name": name}
            fid = folder_id or self.credentials.get("folder_id")
            if fid:
                metadata["parents"] = [fid]
            media = MediaFileUpload(file_path, mimetype=ct)
            result = service.files().create(
                body=metadata, media_body=media, fields="id,name,webViewLink"
            ).execute()
            return self._success(
                f"Archivo subido: {result['name']}\n"
                f"ID: {result['id']}\n"
                f"URL: {result.get('webViewLink', '')}",
                raw_data=result,
            )
        except Exception as e:
            return self._error(f"Error subiendo a Drive: {e}")

    def _download(self, file_id: str = "", destination: str = ".") -> ToolResult:
        if not self.credentials.get("service_account_json"):
            return self._error("Credencial Drive no configurada")
        service = self._get_service()
        if not service:
            return self._error("Error conectando a Google Drive")
        try:
            from googleapiclient.http import MediaIoBaseDownload
            import io
            import os
            meta = service.files().get(fileId=file_id, fields="name").execute()
            out_path = os.path.join(destination, meta["name"])
            req = service.files().get_media(fileId=file_id)
            buf = io.BytesIO()
            dl = MediaIoBaseDownload(buf, req)
            done = False
            while not done:
                _, done = dl.next_chunk()
            with open(out_path, "wb") as f:
                f.write(buf.getvalue())
            return self._success(
                f"Archivo descargado: {out_path}",
                raw_data={"path": out_path, "file_id": file_id},
            )
        except Exception as e:
            return self._error(f"Error descargando de Drive: {e}")

    def _list(self, folder_id: str = None, limit: int = 20) -> ToolResult:
        if not self.credentials.get("service_account_json"):
            return self._error("Credencial Drive no configurada")
        service = self._get_service()
        if not service:
            return self._error("Error conectando a Google Drive")
        try:
            q = f"'{folder_id}' in parents" if folder_id else ""
            results = service.files().list(
                q=q, pageSize=limit,
                fields="files(id,name,mimeType,size,modifiedTime)",
            ).execute()
            files = results.get("files", [])
            lines = [f"- {f['name']} (ID: {f['id']})" for f in files]
            return self._success(
                "\n".join(lines) if lines else "Carpeta vacía",
                raw_data={"files": files},
            )
        except Exception as e:
            return self._error(f"Error listando Drive: {e}")

    def _create_folder(self, name: str = "", parent_id: str = None) -> ToolResult:
        if not self.credentials.get("service_account_json"):
            return self._error("Credencial Drive no configurada")
        service = self._get_service()
        if not service:
            return self._error("Error conectando a Google Drive")
        try:
            metadata = {
                "name": name,
                "mimeType": "application/vnd.google-apps.folder",
            }
            if parent_id:
                metadata["parents"] = [parent_id]
            result = service.files().create(body=metadata, fields="id,name").execute()
            return self._success(
                f"Carpeta '{name}' creada. ID: {result['id']}",
                raw_data=result,
            )
        except Exception as e:
            return self._error(f"Error creando carpeta: {e}")
