"""
Rutas y aplicación FastAPI para el Dashboard API v2.
"""
from __future__ import annotations

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

from fastapi import FastAPI, HTTPException, Query, WebSocket, WebSocketDisconnect, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

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
