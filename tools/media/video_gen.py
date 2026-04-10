from tools.base import BaseTool, ToolResult, tool

_DEFAULT_HOST = "http://localhost:7860"


@tool
class VideoGenTool(BaseTool):
    name = "video_gen"
    description = (
        "Genera vídeos cortos con IA usando modelos locales. "
        "Úsala para crear clips de marketing, reels o contenido "
        "animado. Requiere un servidor de generación de vídeo "
        "compatible con la API de Automatic1111."
    )

    def _get_host(self) -> str:
        return self.credentials.get("host", _DEFAULT_HOST)

    def _is_available(self) -> bool:
        import httpx

        try:
            r = httpx.get(f"{self._get_host()}/sdapi/v1/sd-models", timeout=3)
            return r.status_code == 200
        except Exception:
            return False

    def run(self, action: str = "", **kwargs) -> ToolResult:
        if action == "generate":
            return self._generate(**kwargs)
        if action == "img2vid":
            return self._img2vid(**kwargs)
        if action == "check":
            return self._check()
        return self._error(f"Acción '{action}' no soportada")

    def _check(self) -> ToolResult:
        if not self._is_available():
            return self._error(
                f"Servidor de vídeo no disponible en {self._get_host()}."
            )
        return self._success(
            f"Servidor de generación de vídeo disponible en {self._get_host()}"
        )

    def _generate(
        self,
        prompt: str = "",
        negative_prompt: str = "",
        width: int = 512,
        height: int = 512,
        steps: int = 20,
        frames: int = 16,
        output_path: str = None,
    ) -> ToolResult:
        if not prompt:
            return self._error("El parámetro 'prompt' es obligatorio")
        if not self._is_available():
            return self._error(
                f"Servidor de vídeo no disponible en {self._get_host()}. "
                "Asegúrate de que el servidor esté corriendo."
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
            "n_iter": frames,
        }
        try:
            r = httpx.post(
                f"{self._get_host()}/sdapi/v1/txt2img",
                json=payload,
                timeout=300,
            )
            r.raise_for_status()
            data = r.json()
            images = data.get("images", [])
            if not images:
                return self._error("El servidor no devolvió frames de vídeo")

            if output_path is None:
                safe = prompt[:30].replace(" ", "_").replace("/", "_")
                output_path = f"data/videos/{safe}.mp4"

            Path(output_path).parent.mkdir(parents=True, exist_ok=True)

            # Save frames as individual PNGs then assemble with ffmpeg
            frame_paths = []
            frames_dir = Path(output_path).parent / "_frames_tmp"
            frames_dir.mkdir(parents=True, exist_ok=True)

            for i, img_b64 in enumerate(images):
                frame_path = frames_dir / f"frame_{i:04d}.png"
                frame_paths.append(frame_path)
                with open(frame_path, "wb") as f:
                    f.write(base64.b64decode(img_b64))

            import subprocess
            result = subprocess.run(
                [
                    "ffmpeg", "-y",
                    "-framerate", "8",
                    "-i", str(frames_dir / "frame_%04d.png"),
                    "-c:v", "libx264",
                    "-pix_fmt", "yuv420p",
                    output_path,
                ],
                capture_output=True,
                timeout=120,
            )

            # Clean up temp frames
            for fp in frame_paths:
                fp.unlink(missing_ok=True)
            try:
                frames_dir.rmdir()
            except Exception:
                pass

            if result.returncode != 0:
                return self._error(
                    f"Error al ensamblar vídeo con ffmpeg: {result.stderr.decode()}"
                )

            return self._success(
                f"Vídeo generado: {output_path} ({len(images)} frames)",
                raw_data={"path": output_path, "frames": len(images), "prompt": prompt},
            )
        except Exception as e:
            return self._error(f"Error al generar vídeo: {e}")

    def _img2vid(
        self,
        image_path: str = "",
        frames: int = 16,
        output_path: str = None,
    ) -> ToolResult:
        from pathlib import Path

        if not image_path:
            return self._error("El parámetro 'image_path' es obligatorio")
        p = Path(image_path)
        if not p.exists():
            return self._error(f"Archivo no encontrado: {image_path}")
        if not self._is_available():
            return self._error(
                f"Servidor de vídeo no disponible en {self._get_host()}."
            )
        import httpx
        import base64

        try:
            with open(image_path, "rb") as f:
                img_b64 = base64.b64encode(f.read()).decode()

            r = httpx.post(
                f"{self._get_host()}/sdapi/v1/img2img",
                json={
                    "init_images": [img_b64],
                    "n_iter": frames,
                    "denoising_strength": 0.5,
                },
                timeout=300,
            )
            r.raise_for_status()
            data = r.json()
            images = data.get("images", [])
            if not images:
                return self._error("El servidor no devolvió frames")

            if output_path is None:
                output_path = f"data/videos/{p.stem}_animated.mp4"

            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            frames_dir = Path(output_path).parent / "_frames_tmp"
            frames_dir.mkdir(parents=True, exist_ok=True)

            frame_paths = []
            for i, img in enumerate(images):
                fp = frames_dir / f"frame_{i:04d}.png"
                frame_paths.append(fp)
                with open(fp, "wb") as f:
                    f.write(base64.b64decode(img))

            import subprocess
            result = subprocess.run(
                [
                    "ffmpeg", "-y",
                    "-framerate", "8",
                    "-i", str(frames_dir / "frame_%04d.png"),
                    "-c:v", "libx264",
                    "-pix_fmt", "yuv420p",
                    output_path,
                ],
                capture_output=True,
                timeout=120,
            )

            for fp in frame_paths:
                fp.unlink(missing_ok=True)
            try:
                frames_dir.rmdir()
            except Exception:
                pass

            if result.returncode != 0:
                return self._error(
                    f"Error al ensamblar vídeo con ffmpeg: {result.stderr.decode()}"
                )

            return self._success(
                f"Vídeo generado desde imagen: {output_path}",
                raw_data={"path": output_path, "frames": len(images)},
            )
        except Exception as e:
            return self._error(f"Error img2vid: {e}")
