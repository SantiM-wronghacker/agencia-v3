"""PackageBuilder — genera un paquete instalable para el cliente."""
from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path

from config.settings import settings

# Raíz del proyecto (export/ está un nivel abajo de la raíz)
_SRC_ROOT = Path(__file__).parent.parent

_MODELS = {
    "basic": "phi3:mini",
    "intermediate": "mistral:7b",
    "pro": "qwen2.5:32b",
}

_HEARTBEAT_TEMPLATE = '''\
"""Servicio de heartbeat — corre en background en el cliente."""
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    import urllib.request as _req
    import urllib.error as _err
except ImportError:
    pass

_DIR = Path(__file__).parent
_CONFIG = _DIR.parent / "config" / "client.json"
_STATUS = _DIR / "last_status.json"
_BLOCKED = _DIR / "BLOCKED"

INTERVAL = 86400  # 24 horas


def _load_config() -> dict:
    with open(_CONFIG, encoding="utf-8") as f:
        return json.load(f)


def _send_heartbeat(cfg: dict) -> dict | None:
    url = cfg["license_server_url"].rstrip("/") + "/heartbeat"
    payload = json.dumps({{
        "client_id": cfg["client_id"],
        "license_key": cfg["license_key"],
        "package_type": cfg["package_type"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }}).encode()
    try:
        req = _req.Request(
            url,
            data=payload,
            headers={{"Content-Type": "application/json"}},
            method="POST",
        )
        with _req.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except Exception:
        return None


def run() -> None:
    while True:
        try:
            cfg = _load_config()
            result = _send_heartbeat(cfg)
            if result is not None:
                _STATUS.write_text(json.dumps(result, indent=2), encoding="utf-8")
                if result.get("active") is False:
                    _BLOCKED.touch()
                else:
                    if _BLOCKED.exists():
                        _BLOCKED.unlink()
        except Exception:
            pass
        time.sleep(INTERVAL)


if __name__ == "__main__":
    run()
'''

_CLIENT_SETTINGS_TEMPLATE = '''\
"""Configuración del cliente — solo Ollama, sin APIs cloud."""
import os

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = "{model}"
LLM_PROVIDER = "ollama"

DB_PATH = os.getenv("DB_PATH", "data/agencia.db")
EXPORT_PATH = "export/"
'''

_INSTALL_BAT_TEMPLATE = """\
@echo off
echo ================================
echo  Instalando Agencia IA - {client_name}
echo  Paquete: {package_type}
echo ================================
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
  echo ERROR: Python no encontrado.
  echo Descarga Python desde https://python.org
  pause
  exit /b 1
)

REM Crear entorno virtual
echo Creando entorno virtual...
python -m venv .venv
call .venv\\Scripts\\activate.bat

REM Instalar dependencias
echo Instalando dependencias...
pip install -r requirements.txt

REM Verificar Ollama
ollama --version >nul 2>&1
if errorlevel 1 (
  echo.
  echo Ollama no encontrado. Descargando...
  echo Visita https://ollama.ai para instalarlo manualmente
  echo Luego ejecuta: ollama pull {ollama_model}
  pause
) else (
  echo Descargando modelo de IA ({ollama_model})...
  echo Esto puede tomar varios minutos segun tu conexion...
  ollama pull {ollama_model}
)

REM Iniciar servicio de licencia en background
echo Iniciando servicio de mantenimiento...
start /B pythonw license\\heartbeat.py

REM Iniciar API
echo Iniciando sistema...
start /B python -m uvicorn api.main:app --host 0.0.0.0 --port 8001

REM Abrir dashboard
timeout /t 3 /nobreak >nul
start http://localhost:3000

echo.
echo ================================
echo  Sistema iniciado correctamente
echo  Dashboard: http://localhost:3000
echo  API:       http://localhost:8001
echo ================================
pause
"""

_REQUIREMENTS = """\
fastapi>=0.111.0
uvicorn[standard]>=0.30.0
ollama>=0.2.0
pydantic>=2.7.0
python-dotenv>=1.0.0
httpx>=0.27.0
"""


class PackageBuilder:
    def __init__(
        self,
        client_id: str,
        client_name: str,
        package_type: str,
        license_key: str,
        license_server_url: str,
        groups: list[str],
        output_base: Path | None = None,
    ):
        self.client_id = client_id
        self.client_name = client_name
        self.package_type = package_type
        self.license_key = license_key
        self.license_server_url = license_server_url
        self.groups = groups

        base = output_base if output_base is not None else Path(settings.EXPORT_PATH)
        self.output_path = base / client_id

    # ------------------------------------------------------------------
    # Public
    # ------------------------------------------------------------------

    def build(self) -> Path:
        self._create_structure()
        self._copy_agents()
        self._copy_templates()
        self._copy_groups()
        self._generate_config()
        self._copy_dashboard()
        self._generate_requirements()
        self._generate_installer()
        self._generate_heartbeat_service()
        return self.output_path

    # ------------------------------------------------------------------
    # Steps
    # ------------------------------------------------------------------

    def _create_structure(self) -> None:
        for folder in (
            "agents", "templates", "groups", "config",
            "dashboard", "license", "data", "models",
        ):
            (self.output_path / folder).mkdir(parents=True, exist_ok=True)

    def _copy_agents(self) -> None:
        dest = self.output_path / "agents"
        for sub in ("core", "categorias"):
            src = _SRC_ROOT / "agents" / sub
            if not src.exists():
                continue
            dst = dest / sub
            self._copy_tree(src, dst, exts={".py", ".txt"})

    def _copy_templates(self) -> None:
        src = _SRC_ROOT / "templates"
        dest = self.output_path / "templates"
        if src.exists():
            self._copy_tree(src, dest, exts={".txt"})

    def _copy_groups(self) -> None:
        src_dir = _SRC_ROOT / "groups"
        dest_dir = self.output_path / "groups"
        for name in self.groups:
            src = src_dir / f"{name}.py"
            if src.exists():
                shutil.copy2(src, dest_dir / f"{name}.py")
        # copy __init__.py if it exists
        init = src_dir / "__init__.py"
        if init.exists():
            shutil.copy2(init, dest_dir / "__init__.py")

    def _generate_config(self) -> None:
        model = self._model_for_package()

        # config/client.json
        client_json = {
            "client_id": self.client_id,
            "client_name": self.client_name,
            "package_type": self.package_type,
            "license_key": self.license_key,
            "license_server_url": self.license_server_url,
            "groups": self.groups,
            "installed_at": datetime.utcnow().isoformat(),
            "ollama_model": model,
        }
        (self.output_path / "config" / "client.json").write_text(
            json.dumps(client_json, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        # config/settings.py — solo Ollama
        (self.output_path / "config" / "settings.py").write_text(
            _CLIENT_SETTINGS_TEMPLATE.format(model=model),
            encoding="utf-8",
        )

    def _copy_dashboard(self) -> None:
        build_dir = _SRC_ROOT / "dashboard" / "build"
        dest = self.output_path / "dashboard"
        if build_dir.exists():
            self._copy_tree(build_dir, dest, exts=None)  # all files
        else:
            src_dir = _SRC_ROOT / "dashboard" / "src"
            if src_dir.exists():
                self._copy_tree(src_dir, dest, exts={".ts", ".tsx", ".js", ".jsx", ".css", ".html"})
            (dest / "NOTE.txt").write_text(
                "Ejecuta `npm run build` en dashboard/ y copia build/ aquí.\n",
                encoding="utf-8",
            )

        # Siempre genera config.js con los valores del cliente
        (dest / "config.js").write_text(
            f'const API_URL = "http://localhost:8001";\n'
            f'const CLIENT_ID = "{self.client_id}";\n'
            f'const PACKAGE = "{self.package_type}";\n',
            encoding="utf-8",
        )

    def _generate_requirements(self) -> None:
        (self.output_path / "requirements.txt").write_text(
            _REQUIREMENTS, encoding="utf-8"
        )

    def _generate_heartbeat_service(self) -> None:
        # The template uses {{ }} for literal braces in the format string
        script = _HEARTBEAT_TEMPLATE.format()  # no substitutions needed — values are runtime-read from JSON
        (self.output_path / "license" / "heartbeat.py").write_text(
            script, encoding="utf-8"
        )

    def _generate_installer(self) -> None:
        model = self._model_for_package()
        content = _INSTALL_BAT_TEMPLATE.format(
            client_name=self.client_name,
            package_type=self.package_type,
            ollama_model=model,
        )
        (self.output_path / "install.bat").write_text(content, encoding="utf-8")

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _model_for_package(self) -> str:
        return _MODELS.get(self.package_type, "phi3:mini")

    @staticmethod
    def _copy_tree(src: Path, dest: Path, exts: set[str] | None) -> None:
        """Recursively copy src to dest, optionally filtering by extensions."""
        dest.mkdir(parents=True, exist_ok=True)
        for item in src.rglob("*"):
            if "__pycache__" in item.parts:
                continue
            if item.is_dir():
                (dest / item.relative_to(src)).mkdir(parents=True, exist_ok=True)
                continue
            if exts is not None and item.suffix not in exts:
                continue
            target = dest / item.relative_to(src)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)
