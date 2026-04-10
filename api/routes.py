"""
Rutas y aplicación FastAPI para el Dashboard API v2.
"""
from __future__ import annotations

import asyncio
import csv
import io
import json
import logging
import os
import time
import uuid
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Any, Optional

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Query, WebSocket, WebSocketDisconnect, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from .models import AlertConfig, DashboardMetrics, DirectorAssignRequest, DirectorAssignResponse, HealthResponse, RunAgentRequest, TaskCreate, TaskSchema, TaskStatus, TaskUpdate
from .repository import TaskRepository
from .store import TaskStore
from .team_director import TeamDirector
from .websocket import ConnectionManager

logger = logging.getLogger(__name__)

# --- Aplicación FastAPI -----------------------------------------------------

@asynccontextmanager
async def _lifespan(application: FastAPI):
    """Initialize repository and load config on startup."""
    get_repo()
    _load_alert_config()
    logger.info("Dashboard API v2 started with SQLite persistence")
    yield


app = FastAPI(
    title="Dashboard API v2",
    version="2.0.0",
    description="API para el dashboard de la agencia IA",
    lifespan=_lifespan,
)

_allowed_origins = os.environ.get("DASHBOARD_CORS_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Estado -----------------------------------------------------------------

_start_time: float = time.time()
_task_store = TaskStore()
manager = ConnectionManager()

# SQLite repository (lazy-init to allow test override)
_repo: Optional[TaskRepository] = None

# Alert configuration (default values, can be updated via API)
_alert_config = AlertConfig()
_ALERT_CONFIG_PATH = os.environ.get(
    "DASHBOARD_ALERT_CONFIG", os.path.join("data", "alert_config.json")
)


def _load_alert_config() -> None:
    """Load alert configuration from file if it exists."""
    global _alert_config
    try:
        if os.path.exists(_ALERT_CONFIG_PATH):
            with open(_ALERT_CONFIG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            _alert_config = AlertConfig(**data)
    except Exception:
        logger.warning("Could not load alert config, using defaults", exc_info=True)


def _save_alert_config() -> None:
    """Save alert configuration to file."""
    try:
        os.makedirs(os.path.dirname(_ALERT_CONFIG_PATH) or ".", exist_ok=True)
        with open(_ALERT_CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(_alert_config.model_dump(), f, indent=2)
    except Exception:
        logger.warning("Could not save alert config", exc_info=True)


def get_repo() -> TaskRepository:
    """Get or create the TaskRepository singleton."""
    global _repo
    if _repo is None:
        _repo = TaskRepository()
    return _repo


def set_repo(repo: Optional[TaskRepository]) -> None:
    """Override the repository (for testing)."""
    global _repo
    _repo = repo


# --- Endpoints --------------------------------------------------------------


@app.get("/api/v2/dashboard/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """Estado de salud del servicio."""
    return HealthResponse(
        status="ok",
        version=app.version,
        uptime=time.time() - _start_time,
        services={
            "api": "running",
            "database": "sqlite",
            "websocket": f"{len(manager.active_connections)} conexiones",
        },
    )


@app.get("/api/v2/dashboard/metrics", response_model=DashboardMetrics)
async def metrics() -> DashboardMetrics:
    """Métricas en tiempo real calculadas a partir de la base de datos."""
    repo = get_repo()
    counts = repo.count_by_status()
    total = sum(counts.values())
    completed = counts.get("completed", 0)
    failed = counts.get("failed", 0)
    pending = counts.get("pending", 0)
    running = counts.get("running", 0)
    success_rate = (completed / total * 100.0) if total > 0 else 0.0

    return DashboardMetrics(
        total_tasks=total,
        completed=completed,
        failed=failed,
        pending=pending,
        running=running,
        success_rate=round(success_rate, 2),
    )


@app.post("/api/v2/dashboard/tasks", response_model=TaskSchema, status_code=status.HTTP_201_CREATED)
async def create_task(body: TaskCreate) -> TaskSchema:
    """Crea una nueva tarea."""
    now = datetime.now(timezone.utc)
    task = TaskSchema(
        id=str(uuid.uuid4()),
        name=body.name,
        description=body.description,
        status=TaskStatus.PENDING,
        created_at=now,
        updated_at=now,
    )
    repo = get_repo()
    repo.create(task)
    # Keep in-memory store in sync for backward compatibility
    _task_store[task.id] = task
    await manager.broadcast(_ws_event("task_created", task.model_dump(mode="json")))
    return task


@app.get("/api/v2/dashboard/tasks", response_model=list[TaskSchema])
async def list_tasks(
    status_filter: Optional[TaskStatus] = Query(None, alias="status"),
    search: Optional[str] = Query(None),
) -> list[TaskSchema]:
    """Lista tareas con filtros opcionales de estado y búsqueda."""
    repo = get_repo()
    return repo.list_tasks(status_filter=status_filter, search=search)


@app.get("/api/v2/dashboard/tasks/export")
async def export_tasks(
    format: str = Query("json", pattern="^(csv|json)$"),
) -> StreamingResponse:
    """Export tasks as CSV or JSON."""
    repo = get_repo()
    tasks = repo.list_tasks()

    if format == "csv":
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["id", "name", "status", "description", "created_at", "updated_at", "result"])
        for t in tasks:
            writer.writerow([
                t.id, t.name, t.status.value, t.description or "",
                t.created_at.isoformat(), t.updated_at.isoformat(),
                json.dumps(t.result) if t.result is not None else "",
            ])
        output.seek(0)
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=tasks.csv"},
        )
    else:
        data = [t.model_dump(mode="json") for t in tasks]
        content = json.dumps(data, indent=2, default=str)
        return StreamingResponse(
            iter([content]),
            media_type="application/json",
            headers={"Content-Disposition": "attachment; filename=tasks.json"},
        )


@app.get("/api/v2/dashboard/tasks/{task_id}", response_model=TaskSchema)
async def get_task(task_id: str) -> TaskSchema:
    """Obtiene una tarea por su ID."""
    repo = get_repo()
    task = repo.get(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    return task




@app.patch("/api/v2/dashboard/tasks/{task_id}", response_model=TaskSchema)
async def update_task(task_id: str, body: TaskUpdate) -> TaskSchema:
    """Actualiza parcialmente una tarea (nombre, descripción, estado)."""
    repo = get_repo()
    task = repo.get(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")

    if body.name is not None:
        task.name = body.name
    if body.description is not None:
        task.description = body.description
    if body.status is not None:
        task.status = body.status
    task.updated_at = datetime.now(timezone.utc)

    repo.update(task)
    _task_store[task.id] = task
    await manager.broadcast(_ws_event("task_updated", task.model_dump(mode="json")))
    return task


@app.post("/api/v2/dashboard/tasks/{task_id}/cancel", response_model=TaskSchema)
async def cancel_task(task_id: str) -> TaskSchema:
    """Cancela una tarea si está en estado PENDING o RUNNING."""
    repo = get_repo()
    task = repo.get(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")

    if task.status not in (TaskStatus.PENDING, TaskStatus.RUNNING):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se puede cancelar una tarea con estado {task.status.value}",
        )

    now = datetime.now(timezone.utc)
    task.status = TaskStatus.CANCELLED
    task.updated_at = datetime.now(timezone.utc)
    repo.update(task)
    _task_store[task_id] = task
    await manager.broadcast(_ws_event("task_cancelled", task.model_dump(mode="json")))
    return task


@app.get("/api/v2/dashboard/tasks/{task_id}/logs", response_model=list[str])
async def get_task_logs(task_id: str) -> list[str]:
    """Devuelve los logs de una tarea."""
    repo = get_repo()
    task = repo.get(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    return task.logs


# --- Agent execution (stub) -------------------------------------------------


@app.post("/api/v2/dashboard/run-agent", response_model=TaskSchema, status_code=status.HTTP_201_CREATED)
async def run_agent(body: RunAgentRequest) -> TaskSchema:
    """Execute an agent as a background task (stub implementation).

    This endpoint creates a task linked to agent execution. In future
    iterations it will run the agent via subprocess or direct import.
    Currently it creates a task with status RUNNING and logs indicating
    the agent execution is stubbed.
    """
    now = datetime.now(timezone.utc)
    task = TaskSchema(
        id=str(uuid.uuid4()),
        name=f"Agent: {body.category}/{body.agent_name}",
        description=f"Input: {body.input}",
        status=TaskStatus.RUNNING,
        created_at=now,
        updated_at=now,
        logs=[
            f"[stub] Agent execution requested: {body.category}/{body.agent_name}",
            f"[stub] Input: {body.input}",
            "[stub] Real agent execution not yet implemented - task marked as completed",
        ],
        result={"stub": True, "message": "Agent execution not yet integrated"},
    )
    # Mark as completed since it's a stub
    task.status = TaskStatus.COMPLETED
    task.updated_at = datetime.now(timezone.utc)

    repo = get_repo()
    repo.create(task)
    _task_store[task.id] = task
    await manager.broadcast(_ws_event("task_created", task.model_dump(mode="json")))
    return task


# --- Alerts configuration ---------------------------------------------------


@app.get("/api/v2/dashboard/alerts/config", response_model=AlertConfig)
async def get_alert_config() -> AlertConfig:
    """Get current alert configuration."""
    return _alert_config


@app.put("/api/v2/dashboard/alerts/config", response_model=AlertConfig)
async def update_alert_config(body: AlertConfig) -> AlertConfig:
    """Update alert configuration."""
    global _alert_config
    _alert_config = body
    _save_alert_config()
    return _alert_config


@app.get("/api/v2/dashboard/alerts")
async def get_alerts() -> dict:
    """Get current alerts based on metrics and alert config."""
    repo = get_repo()
    counts = repo.count_by_status()
    total = sum(counts.values())
    failed = counts.get("failed", 0)
    completed = counts.get("completed", 0)
    success_rate = (completed / total * 100.0) if total > 0 else 100.0

    alerts = []
    if failed > _alert_config.max_failed:
        alerts.append({
            "type": "failed_threshold",
            "severity": "warning",
            "message": f"Failed tasks ({failed}) exceed threshold ({_alert_config.max_failed})",
        })
    if total > 0 and success_rate < _alert_config.min_success_rate:
        alerts.append({
            "type": "low_success_rate",
            "severity": "warning",
            "message": f"Success rate ({success_rate:.1f}%) below threshold ({_alert_config.min_success_rate}%)",
        })

    return {"alerts": alerts, "config": _alert_config.model_dump()}


# --- WebSocket ---------------------------------------------------------------


def _ws_event(event_type: str, payload: Any) -> dict:
    """Create a WebSocket event envelope with timestamp."""
    return {
        "event": event_type,
        "payload": payload,
        "ts": datetime.now(timezone.utc).isoformat(),
    }


def _event_envelope(event_type: str, data: Any) -> dict:
    """Create a WebSocket event envelope (echo responses)."""
    return {"event": event_type, "data": data}


@app.websocket("/api/v2/dashboard/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    """Endpoint WebSocket para actualizaciones en tiempo real."""
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(
                _event_envelope("echo", data), websocket
            )
    except WebSocketDisconnect:
        manager.disconnect(websocket)


# --- TeamDirector dev endpoint ----------------------------------------------

_director = TeamDirector()


@app.post("/api/v2/dashboard/director/assign", response_model=DirectorAssignResponse)
async def director_assign(body: DirectorAssignRequest) -> DirectorAssignResponse:
    """Assign a task via the TeamDirector (dev endpoint).

    Returns 400 if the role is not registered.
    """
    try:
        result = _director.assign(body.role, body.task)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    return DirectorAssignResponse(**result)


# ---------------------------------------------------------------------------
# v3 — grupos, runs y memoria
# ---------------------------------------------------------------------------

from api.dependencies import get_db, get_orchestrator  # noqa: E402


class _GroupRunRequest(BaseModel):
    task: str
    mode: Optional[str] = None


router = APIRouter()


@router.get("/groups")
async def list_groups(orchestrator=Depends(get_orchestrator)) -> list[dict]:
    """Lista todos los grupos registrados en el orchestrator."""
    return orchestrator.list_groups()


async def _run_group_bg(
    orchestrator,
    group_name: str,
    task: str,
    run_id: str,
) -> None:
    """Background task: ejecuta el grupo y emite eventos WebSocket."""
    await manager.broadcast(
        _ws_event(
            "group_run_started",
            {"run_id": run_id, "group_name": group_name, "task_preview": task[:100]},
        )
    )
    try:
        result = await asyncio.to_thread(
            orchestrator.run, group_name, task, run_id
        )
        for step in result.steps:
            await manager.broadcast(
                _ws_event(
                    "group_step_completed",
                    {
                        "run_id": run_id,
                        "group_name": group_name,
                        "step_index": step.step_index,
                        "role": step.role,
                        "success": step.success,
                    },
                )
            )
        await manager.broadcast(
            _ws_event(
                "group_run_finished",
                {
                    "run_id": run_id,
                    "group_name": group_name,
                    "success": result.success,
                    "duration_ms": result.total_duration_ms,
                },
            )
        )
    except Exception as exc:
        await manager.broadcast(
            _ws_event(
                "group_run_finished",
                {"run_id": run_id, "group_name": group_name, "success": False, "error": str(exc)},
            )
        )


@router.post("/groups/{group_name}/run")
async def run_group(
    group_name: str,
    body: _GroupRunRequest,
    orchestrator=Depends(get_orchestrator),
) -> dict:
    """Lanza un grupo en background y retorna el run_id inmediatamente."""
    group = orchestrator.get_group(group_name)
    if group is None:
        raise HTTPException(status_code=404, detail=f"Grupo '{group_name}' no encontrado")

    if body.mode is not None:
        from core.group import _VALID_MODES
        if body.mode not in _VALID_MODES:
            raise HTTPException(status_code=400, detail=f"Modo '{body.mode}' no válido")
        group.mode = body.mode

    run_id = str(uuid.uuid4())
    asyncio.create_task(_run_group_bg(orchestrator, group_name, body.task, run_id))
    return {"run_id": run_id, "status": "started", "group_name": group_name}


@router.get("/groups/{group_name}/runs/{run_id}")
async def get_group_run(
    group_name: str,
    run_id: str,
    db=Depends(get_db),
) -> dict:
    """Estado actual de un run específico."""
    run = db.get_run(run_id)
    if run is None or run.get("group_name") != group_name:
        raise HTTPException(status_code=404, detail=f"Run '{run_id}' no encontrado")
    steps = db.get_steps(run_id)
    return {**run, "steps": steps}


@router.get("/groups/{group_name}/runs")
async def list_group_runs(
    group_name: str,
    db=Depends(get_db),
) -> list[dict]:
    """Últimos 20 runs del grupo con sus steps."""
    all_runs = db.get_recent_runs(limit=100)
    runs = [r for r in all_runs if r.get("group_name") == group_name][:20]
    result = []
    for run in runs:
        steps = db.get_steps(run["id"])
        result.append({**run, "steps": steps})
    return result


@router.get("/memory/search")
async def memory_search(
    q: str = Query(..., min_length=1),
    limit: int = Query(10, ge=1, le=100),
    db=Depends(get_db),
) -> list[dict]:
    """Búsqueda FTS5 en observaciones."""
    if not q.strip():
        raise HTTPException(status_code=400, detail="El parámetro 'q' no puede estar vacío")
    from memory.fts import FTSSearch
    return FTSSearch(db).search(q, limit=limit)


class _ExportRequest(BaseModel):
    client_name: str
    package_type: str
    license_key: str
    license_server_url: str
    groups: list[str]


@router.post("/export/{client_id}")
async def export_client(
    client_id: str,
    body: _ExportRequest,
    orchestrator=Depends(get_orchestrator),
) -> dict:
    """Genera un paquete instalable para el cliente."""
    # Validate groups exist
    invalid = [g for g in body.groups if orchestrator.get_group(g) is None]
    if invalid:
        raise HTTPException(
            status_code=400,
            detail=f"Grupos no encontrados: {', '.join(invalid)}",
        )

    from export.builder import PackageBuilder

    builder = PackageBuilder(
        client_id=client_id,
        client_name=body.client_name,
        package_type=body.package_type,
        license_key=body.license_key,
        license_server_url=body.license_server_url,
        groups=body.groups,
    )
    try:
        path = builder.build()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    files_generated = sum(1 for f in path.rglob("*") if f.is_file())

    return {
        "client_id": client_id,
        "package_path": str(path),
        "package_type": body.package_type,
        "groups_included": body.groups,
        "ollama_model": builder._model_for_package(),
        "files_generated": files_generated,
    }


app.include_router(router)


# ---------------------------------------------------------------------------
# Webhooks — recibe eventos externos y dispara grupos
# ---------------------------------------------------------------------------

_WEBHOOK_ENDPOINTS_FILE = "data/webhook_endpoints.json"
_WEBHOOK_EVENTS_FILE = "data/webhook_events.json"


def _load_json_file(path: str) -> list:
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return []


def _append_json_file(path: str, entry: dict) -> None:
    items = _load_json_file(path)
    items.append(entry)
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)


@app.post("/webhooks/{client_id}/{trigger_name}")
async def receive_webhook(client_id: str, trigger_name: str) -> dict:
    """Recibe un webhook y dispara el grupo configurado en background."""
    endpoints = _load_json_file(_WEBHOOK_ENDPOINTS_FILE)
    endpoint = next(
        (e for e in endpoints if e.get("name") == trigger_name and e.get("active")),
        None,
    )
    event = {
        "endpoint_name": trigger_name,
        "client_id": client_id,
        "received_at": datetime.now(timezone.utc).isoformat(),
        "summary": f"Webhook from {client_id}/{trigger_name}",
    }
    _append_json_file(_WEBHOOK_EVENTS_FILE, event)

    if endpoint:
        group_name = endpoint.get("group_name", "")
        return {
            "received": True,
            "trigger": trigger_name,
            "group_triggered": group_name,
        }
    return {"received": True}


# ---------------------------------------------------------------------------
# Scheduler — CRUD de tareas programadas
# ---------------------------------------------------------------------------

_SCHEDULER_FILE = "data/scheduled_tasks.json"


class _SchedulerTaskCreate(BaseModel):
    group_name: str
    cron: str
    task_template: str = ""
    description: str = ""


@app.get("/scheduler/tasks")
async def list_scheduler_tasks() -> list:
    """Lista todas las tareas programadas."""
    return _load_json_file(_SCHEDULER_FILE)


@app.post("/scheduler/tasks", status_code=201)
async def create_scheduler_task(body: _SchedulerTaskCreate) -> dict:
    """Crea una nueva tarea programada tras validar el cron."""
    from tools.automation.scheduler import SchedulerTool
    tool_obj = SchedulerTool()
    result = tool_obj.run(
        action="schedule",
        group_name=body.group_name,
        task=body.task_template or body.description,
        cron_expression=body.cron,
    )
    if not result.success:
        raise HTTPException(status_code=400, detail=result.error)
    return result.raw_data


@app.delete("/scheduler/tasks/{task_id}", status_code=200)
async def delete_scheduler_task(task_id: str) -> dict:
    """Cancela (desactiva) una tarea programada."""
    tasks = _load_json_file(_SCHEDULER_FILE)
    found = False
    for t in tasks:
        if t.get("id") == task_id:
            t["active"] = False
            found = True
            break
    if not found:
        raise HTTPException(status_code=404, detail=f"Tarea '{task_id}' no encontrada")
    os.makedirs("data", exist_ok=True)
    with open(_SCHEDULER_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)
    return {"deleted": True, "task_id": task_id}
