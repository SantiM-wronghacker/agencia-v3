from pathlib import Path

from tools.base import BaseTool, ToolResult, tool


@tool
class ImageResizeTool(BaseTool):
    name = "image_resize"
    description = (
        "Redimensiona y procesa imágenes para portales y redes sociales. "
        "Úsala para optimizar fotos de propiedades, productos o contenido."
    )

    def run(self, action: str = "", **kwargs) -> ToolResult:
        if action == "resize":
            return self._resize(**kwargs)
        if action == "convert":
            return self._convert(**kwargs)
        return self._error(f"Acción '{action}' no soportada")

    def _resize(
        self,
        input_path: str = "",
        output_path: str = None,
        width: int = 1200,
        height: int = 800,
    ) -> ToolResult:
        if not input_path:
            return self._error("El parámetro 'input_path' es obligatorio")
        p = Path(input_path)
        if not p.exists():
            return self._error(f"Archivo no encontrado: {input_path}")
        try:
            from PIL import Image  # type: ignore

            img = Image.open(input_path)
            img = img.resize((width, height), Image.LANCZOS)
            if output_path is None:
                output_path = str(p.parent / f"{p.stem}_{width}x{height}{p.suffix}")
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            img.save(output_path)
            return self._success(
                f"Imagen redimensionada a {width}x{height}: {output_path}",
                raw_data={"path": output_path, "width": width, "height": height},
            )
        except ImportError:
            return self._error("Pillow no instalado. Ejecuta: pip install Pillow")
        except Exception as e:
            return self._error(f"Error al redimensionar imagen: {e}")

    def _convert(
        self,
        input_path: str = "",
        output_format: str = "JPEG",
        output_path: str = None,
    ) -> ToolResult:
        if not input_path:
            return self._error("El parámetro 'input_path' es obligatorio")
        p = Path(input_path)
        if not p.exists():
            return self._error(f"Archivo no encontrado: {input_path}")
        try:
            from PIL import Image  # type: ignore

            img = Image.open(input_path)
            ext = output_format.lower()
            if output_path is None:
                output_path = str(p.parent / f"{p.stem}.{ext}")
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            img.save(output_path, format=output_format)
            return self._success(
                f"Imagen convertida a {output_format}: {output_path}",
                raw_data={"path": output_path, "format": output_format},
            )
        except ImportError:
            return self._error("Pillow no instalado. Ejecuta: pip install Pillow")
        except Exception as e:
            return self._error(f"Error al convertir imagen: {e}")
