from tools.base import BaseTool, ToolResult, tool


@tool
class SystemMonitorTool(BaseTool):
    name = "system_monitor"
    description = (
        "Monitorea recursos del sistema donde está instalado. "
        "Úsala para verificar CPU, RAM, disco "
        "y estado de servicios."
    )

    def _check_psutil(self):
        try:
            import psutil
            return psutil
        except ImportError:
            return None

    def run(self, action: str = "", **kwargs) -> ToolResult:
        if action == "get_cpu":
            return self._get_cpu()
        if action == "get_memory":
            return self._get_memory()
        if action == "get_disk":
            return self._get_disk(**kwargs)
        if action == "get_all":
            return self._get_all()
        if action == "check_service":
            return self._check_service(**kwargs)
        return self._error(f"Acción '{action}' no soportada")

    def _get_cpu(self) -> ToolResult:
        ps = self._check_psutil()
        if not ps:
            return self._error("psutil no instalado. Ejecuta: pip install psutil")
        cpu_pct = ps.cpu_percent(interval=1)
        cpu_count = ps.cpu_count()
        try:
            freq = ps.cpu_freq()
            freq_str = f"\nFrecuencia: {freq.current:.0f}MHz" if freq else ""
        except Exception:
            freq_str = ""
        return self._success(
            f"CPU: {cpu_pct:.1f}% uso\nNúcleos: {cpu_count}{freq_str}",
            raw_data={"cpu_percent": cpu_pct, "cpu_count": cpu_count},
        )

    def _get_memory(self) -> ToolResult:
        ps = self._check_psutil()
        if not ps:
            return self._error("psutil no instalado. Ejecuta: pip install psutil")
        mem = ps.virtual_memory()
        return self._success(
            f"RAM: {mem.percent:.1f}% uso\n"
            f"Usada: {mem.used/1e9:.1f}GB\n"
            f"Disponible: {mem.available/1e9:.1f}GB\n"
            f"Total: {mem.total/1e9:.1f}GB",
            raw_data={
                "percent": mem.percent,
                "used_gb": mem.used / 1e9,
                "total_gb": mem.total / 1e9,
            },
        )

    def _get_disk(self, path: str = "/") -> ToolResult:
        ps = self._check_psutil()
        if not ps:
            return self._error("psutil no instalado. Ejecuta: pip install psutil")
        import platform
        if platform.system() == "Windows" and path == "/":
            path = "C:\\"
        try:
            disk = ps.disk_usage(path)
        except Exception as e:
            return self._error(f"Error leyendo disco '{path}': {e}")
        return self._success(
            f"Disco ({path}): {disk.percent:.1f}% uso\n"
            f"Usado: {disk.used/1e9:.1f}GB\n"
            f"Libre: {disk.free/1e9:.1f}GB\n"
            f"Total: {disk.total/1e9:.1f}GB",
            raw_data={"percent": disk.percent, "free_gb": disk.free / 1e9},
        )

    def _get_all(self) -> ToolResult:
        parts = []
        for fn in [self._get_cpu, self._get_memory, lambda: self._get_disk()]:
            r = fn()
            parts.append(r.output if r.success else f"Error: {r.error}")
        return self._success(
            "\n\n".join(parts),
            raw_data={"sections": ["cpu", "memory", "disk"]},
        )

    def _check_service(self, service_name: str = "") -> ToolResult:
        ps = self._check_psutil()
        if not ps:
            return self._error("psutil no instalado. Ejecuta: pip install psutil")
        if not service_name:
            return self._error("El parámetro 'service_name' es obligatorio")
        found = False
        pid = None
        try:
            for proc in ps.process_iter(["name", "pid"]):
                if service_name.lower() in (proc.info["name"] or "").lower():
                    found = True
                    pid = proc.info["pid"]
                    break
        except Exception:
            pass
        status = "ACTIVO" if found else "NO ENCONTRADO"
        pid_str = f" (PID: {pid})" if pid else ""
        return self._success(
            f"Servicio '{service_name}': {status}{pid_str}",
            raw_data={"service": service_name, "found": found, "pid": pid},
        )
