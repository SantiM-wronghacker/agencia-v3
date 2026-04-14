from tools.base import BaseTool, ToolResult, tool


@tool
class APIImageGenTool(BaseTool):
    name = "image_gen_api"
    description = (
        "Genera imágenes con IA usando APIs cloud como OpenAI DALL-E "
        "o Stability AI. Úsala cuando no haya GPU local disponible."
    )

    def run(self, action: str = "", **kwargs) -> ToolResult:
        if action == "generate":
            return self._generate(**kwargs)
        if action == "check":
            return self._check()
        return self._error(f"Acción '{action}' no soportada")

    def _get_provider(self) -> str:
        return self.credentials.get("provider", "openai")

    def _check(self) -> ToolResult:
        provider = self._get_provider()
        key = self.credentials.get("api_key", "")
        if not key:
            return self._error("Credencial api_key no configurada")
        return self._success(
            f"Image Gen API configurada con proveedor: {provider}",
            raw_data={"provider": provider},
        )

    def _generate(
        self,
        prompt: str = "",
        width: int = 1024,
        height: int = 1024,
        output_path: str = None,
        model: str = "",
        n: int = 1,
    ) -> ToolResult:
        if not prompt:
            return self._error("El parámetro 'prompt' es obligatorio")
        provider = self._get_provider()
        if provider == "openai":
            return self._generate_openai(prompt, width, height, output_path, model, n)
        if provider == "stability":
            return self._generate_stability(prompt, width, height, output_path)
        return self._error(f"Proveedor '{provider}' no soportado. Usa: openai, stability")

    def _generate_openai(
        self,
        prompt: str,
        width: int,
        height: int,
        output_path: str,
        model: str,
        n: int,
    ) -> ToolResult:
        api_key = self.credentials.get("api_key", "")
        if not api_key:
            return self._error("Credencial api_key no configurada")
        import httpx
        import base64
        from pathlib import Path

        size = f"{width}x{height}"
        allowed = {"256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"}
        if size not in allowed:
            size = "1024x1024"

        payload = {
            "model": model or "dall-e-3",
            "prompt": prompt,
            "n": min(n, 1),
            "size": size,
            "response_format": "b64_json",
        }
        try:
            r = httpx.post(
                "https://api.openai.com/v1/images/generations",
                headers={"Authorization": f"Bearer {api_key}"},
                json=payload,
                timeout=60,
            )
            r.raise_for_status()
            data = r.json()
            images = data.get("data", [])
            if not images:
                return self._error("API no devolvió imágenes")

            if output_path is None:
                safe = prompt[:30].replace(" ", "_").replace("/", "_")
                output_path = f"data/images/{safe}_api.png"

            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            img_bytes = base64.b64decode(images[0]["b64_json"])
            with open(output_path, "wb") as f:
                f.write(img_bytes)

            return self._success(
                f"Imagen generada con DALL-E: {output_path}",
                raw_data={"path": output_path, "prompt": prompt, "provider": "openai"},
            )
        except Exception as e:
            return self._error(f"Error al generar imagen con OpenAI: {e}")

    def _generate_stability(
        self,
        prompt: str,
        width: int,
        height: int,
        output_path: str,
    ) -> ToolResult:
        api_key = self.credentials.get("api_key", "")
        if not api_key:
            return self._error("Credencial api_key no configurada")
        import httpx
        from pathlib import Path

        try:
            r = httpx.post(
                "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Accept": "application/json",
                },
                json={
                    "text_prompts": [{"text": prompt}],
                    "width": width,
                    "height": height,
                    "samples": 1,
                    "steps": 30,
                },
                timeout=60,
            )
            r.raise_for_status()
            data = r.json()
            artifacts = data.get("artifacts", [])
            if not artifacts:
                return self._error("Stability AI no devolvió imágenes")

            import base64
            if output_path is None:
                safe = prompt[:30].replace(" ", "_").replace("/", "_")
                output_path = f"data/images/{safe}_stability.png"

            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            img_bytes = base64.b64decode(artifacts[0]["base64"])
            with open(output_path, "wb") as f:
                f.write(img_bytes)

            return self._success(
                f"Imagen generada con Stability AI: {output_path}",
                raw_data={"path": output_path, "prompt": prompt, "provider": "stability"},
            )
        except Exception as e:
            return self._error(f"Error al generar imagen con Stability AI: {e}")
