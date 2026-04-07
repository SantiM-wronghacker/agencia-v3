from pydantic import BaseModel


class HeartbeatRequest(BaseModel):
    client_id: str
    license_key: str
    package_type: str
    timestamp: str


class HeartbeatResponse(BaseModel):
    active: bool
    status: str        # active | warning | grace | blocked
    message: str
    days_remaining: int
    hours_offline: int


class ClientCreate(BaseModel):
    name: str
    license_key: str | None = None   # si None se genera automático
    package_type: str = "basic"
    paid_until: str                  # ISO date "2026-05-01"


class ClientUpdate(BaseModel):
    active: bool | None = None
    paid_until: str | None = None
    package_type: str | None = None
