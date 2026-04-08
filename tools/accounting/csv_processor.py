import csv
from pathlib import Path

from tools.base import BaseTool, ToolResult, tool


@tool
class CSVProcessorTool(BaseTool):
    name = "csv_processor"
    description = (
        "Procesa archivos CSV. "
        "Úsala para leer, filtrar y resumir "
        "datos de archivos CSV."
    )

    def run(self, action: str = "", **kwargs) -> ToolResult:
        if action == "read":
            return self._read(**kwargs)
        if action == "filter":
            return self._filter(**kwargs)
        if action == "summarize":
            return self._summarize(**kwargs)
        return self._error(f"Acción '{action}' no soportada")

    def _load_csv(self, file_path: str) -> tuple[list[dict], list[str]] | tuple[None, str]:
        """Returns (rows, headers) or (None, error_message)."""
        if not file_path or not Path(file_path).exists():
            return None, f"Archivo no encontrado: {file_path}"
        try:
            with open(file_path, newline="", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                headers = reader.fieldnames or []
                rows = list(reader)
            return rows, list(headers)
        except Exception as e:
            return None, f"Error al leer CSV: {e}"

    def _read(self, file_path: str = "", max_rows: int = 100) -> ToolResult:
        rows, headers_or_err = self._load_csv(file_path)
        if rows is None:
            return self._error(headers_or_err)

        headers = headers_or_err
        limited = rows[:max_rows]

        lines = [" | ".join(headers)]
        lines.append("-" * (len(lines[0])))
        for row in limited:
            lines.append(" | ".join(str(row.get(h, "")) for h in headers))

        total_note = f"\n(Mostrando {len(limited)} de {len(rows)} filas)" if len(rows) > max_rows else ""

        return self._success(
            "\n".join(lines) + total_note,
            raw_data={"rows": limited, "headers": headers, "total": len(rows)},
        )

    def _filter(
        self, file_path: str = "", column: str = "", value: str = ""
    ) -> ToolResult:
        rows, headers_or_err = self._load_csv(file_path)
        if rows is None:
            return self._error(headers_or_err)

        headers = headers_or_err
        if column not in headers:
            return self._error(f"Columna '{column}' no encontrada. Columnas: {', '.join(headers)}")

        filtered = [r for r in rows if r.get(column, "") == value]

        if not filtered:
            return self._success(
                f"Sin resultados: ninguna fila tiene {column}='{value}'",
                raw_data={"rows": [], "count": 0},
            )

        lines = [" | ".join(headers)]
        for row in filtered:
            lines.append(" | ".join(str(row.get(h, "")) for h in headers))

        return self._success(
            "\n".join(lines),
            raw_data={"rows": filtered, "count": len(filtered)},
        )

    def _summarize(
        self,
        file_path: str = "",
        group_by: str = None,
        numeric_column: str = None,
    ) -> ToolResult:
        rows, headers_or_err = self._load_csv(file_path)
        if rows is None:
            return self._error(headers_or_err)

        headers = headers_or_err
        lines = [f"Resumen de {Path(file_path).name}:"]
        lines.append(f"  Total de filas: {len(rows)}")
        lines.append(f"  Columnas: {', '.join(headers)}")

        if group_by and group_by in headers:
            counts: dict = {}
            for row in rows:
                key = row.get(group_by, "")
                counts[key] = counts.get(key, 0) + 1
            lines.append(f"\n  Conteo por '{group_by}':")
            for val, count in sorted(counts.items(), key=lambda x: -x[1]):
                lines.append(f"    {val}: {count}")

        if numeric_column and numeric_column in headers:
            values = []
            for row in rows:
                try:
                    values.append(float(row.get(numeric_column, 0)))
                except (ValueError, TypeError):
                    pass
            if values:
                lines.append(f"\n  Estadísticas de '{numeric_column}':")
                lines.append(f"    Suma: {sum(values):,.2f}")
                lines.append(f"    Promedio: {sum(values) / len(values):,.2f}")
                lines.append(f"    Mínimo: {min(values):,.2f}")
                lines.append(f"    Máximo: {max(values):,.2f}")

        return self._success(
            "\n".join(lines),
            raw_data={"total": len(rows), "headers": headers},
        )
