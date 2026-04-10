from tools.base import BaseTool, ToolResult, tool

_DEFAULT_HOST = "http://localhost:7860"


@tool
class LocalImageGenTool(BaseTool):
    name = "image_gen_local"
    description = (
        "Genera imágenes con IA usando Stable Diffusion local. "
        "Úsala para crear imágenes de marketing, posts o "
        "materiales visuales. Requiere Automatic1111 en "
        "localhost:7860."
    )

    def _get_host(self) -> str:
        return self.credentials.get("host", _DEFAULT_HOST)

    def _is_available(self) -> bool:
        import httpx

        try:
            r = httpx.get(
                f"{self._get_host()}/sdapi/v1/sd-models", timeout=3
            )
            return r.status_code == 200
        except Exception:
            return False

    def run(self, action: str = "", **kwargs) -> ToolResult:
        if action == "generate":
            return self._generate(**kwargs)
        if action == "check":
            return self._check()
        return self._error(f"Acción '{action}' no soportada")

    def _check(self) -> ToolResult:
        if not self._is_available():
            return self._error(
                f"Stable Diffusion no disponible en {self._get_host()}. "
                "Asegúrate de que Automatic1111 esté corriendo."
            )
        import httpx

        try:
            r = httpx.get(
                f"{self._get_host()}/sdapi/v1/sd-models", timeout=5
            )
            models = [m.get("title", "") for m in r.json()]
            return self._success(
                f"Stable Diffusion disponible. Modelos: {', '.join(models[:3])}",
                raw_data={"models": models},
            )
        except Exception as e:
            return self._error(f"Error al verificar Stable Diffusion: {e}")

    def _generate(
        self,
        prompt: str = "",
        negative_prompt: str = "",
        width: int = 512,
        height: int = 512,
        steps: int = 20,
        cfg_scale: float = 7.0,
        output_path: str = None,
    ) -> ToolResult:
        if not prompt:
            return self._error("El parámetro 'prompt' es obligatorio")
        if not self._is_available():
            return self._error(
                f"Stable Diffusion no disponible en {self._get_host()}. "
                "Asegúrate de que Automatic1111 esté corriendo."
            )
        import httpx
        import base64
        from pathlib import Path

        payload = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "width": width,
            "height": height,
            "steps": steps,
            "cfg_scale": cfg_scale,
        }
        try:
            r = httpx.post(
                f"{self._get_host()}/sdapi/v1/txt2img",
                json=payload,
                timeout=120,
            )
            r.raise_for_status()
            data = r.json()
            images = data.get("images", [])
            if not images:
                return self._error("Stable Diffusion no devolvió imágenes")

            if output_path is None:
                safe = prompt[:30].replace(" ", "_").replace("/", "_")
                output_path = f"data/images/{safe}.png"

            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            img_bytes = base64.b64decode(images[0])
            with open(output_path, "wb") as f:
                f.write(img_bytes)

            return self._success(
                f"Imagen generada: {output_path}",
                raw_data={"path": output_path, "prompt": prompt},
            )
        except Exception as e:
            return self._error(f"Error al generar imagen: {e}")
