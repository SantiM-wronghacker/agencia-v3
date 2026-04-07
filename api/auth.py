"""
Autenticación JWT para el Dashboard API.
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
import logging
import os
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .models import TokenData, UserRole

logger = logging.getLogger(__name__)

SECRET_KEY = os.getenv("DASHBOARD_SECRET_KEY", "dev-secret-key-change-in-production")
ALGORITHM = "HS256"
TOKEN_EXPIRE_HOURS = 24

security = HTTPBearer(auto_error=False)

# --- JWT backend -----------------------------------------------------------
# Intenta usar python-jose; si no está disponible, usa un fallback con base64.

try:
    from jose import JWTError, jwt as jose_jwt  # type: ignore[import-untyped]

    def create_access_token(data: dict[str, Any]) -> str:
        """Crea un token JWT usando python-jose."""
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(hours=TOKEN_EXPIRE_HOURS)
        to_encode.update({"exp": expire})
        return jose_jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    def verify_token(token: str) -> dict[str, Any]:
        """Verifica y decodifica un token JWT usando python-jose."""
        try:
            payload: dict[str, Any] = jose_jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido o expirado",
            ) from exc

except ImportError:
    logger.warning("python-jose no disponible; usando fallback base64 para JWT")

    def _b64url_encode(data: bytes) -> str:
        return base64.urlsafe_b64encode(data).rstrip(b"=").decode()

    def _b64url_decode(data: str) -> bytes:
        padding = 4 - len(data) % 4
        return base64.urlsafe_b64decode(data + "=" * padding)

    def _sign(header_payload: str) -> str:
        return _b64url_encode(
            hmac.new(SECRET_KEY.encode(), header_payload.encode(), hashlib.sha256).digest()
        )

    def create_access_token(data: dict[str, Any]) -> str:  # type: ignore[misc]
        """Crea un token JWT con fallback base64/HMAC."""
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(hours=TOKEN_EXPIRE_HOURS)
        to_encode["exp"] = expire.timestamp()
        header = _b64url_encode(json.dumps({"alg": ALGORITHM, "typ": "JWT"}).encode())
        payload = _b64url_encode(json.dumps(to_encode, default=str).encode())
        header_payload = f"{header}.{payload}"
        signature = _sign(header_payload)
        return f"{header_payload}.{signature}"

    def verify_token(token: str) -> dict[str, Any]:  # type: ignore[misc]
        """Verifica y decodifica un token JWT con fallback base64/HMAC."""
        try:
            parts = token.split(".")
            if len(parts) != 3:
                raise ValueError("Formato de token inválido")
            header_payload = f"{parts[0]}.{parts[1]}"
            expected_sig = _sign(header_payload)
            if not hmac.compare_digest(expected_sig, parts[2]):
                raise ValueError("Firma inválida")
            payload_bytes = _b64url_decode(parts[1])
            payload: dict[str, Any] = json.loads(payload_bytes)
            exp = payload.get("exp")
            if exp is not None and float(exp) < time.time():
                raise ValueError("Token expirado")
            return payload
        except (ValueError, json.JSONDecodeError, KeyError) as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido o expirado",
            ) from exc


# --- FastAPI dependencies ---------------------------------------------------

async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> TokenData:
    """Dependencia que extrae y valida el usuario actual del token JWT."""
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no proporcionadas",
        )
    payload = verify_token(credentials.credentials)
    try:
        return TokenData(
            sub=payload["sub"],
            role=UserRole(payload["role"]),
            exp=datetime.fromtimestamp(
                float(payload["exp"]), tz=timezone.utc
            ),
        )
    except (KeyError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token con datos incompletos",
        ) from exc


def require_role(role: UserRole) -> Callable[..., TokenData]:
    """Devuelve una dependencia que verifica que el usuario tenga el rol requerido."""

    async def _check(current_user: TokenData = Depends(get_current_user)) -> TokenData:
        role_hierarchy = {UserRole.VIEWER: 0, UserRole.USER: 1, UserRole.ADMIN: 2}
        if role_hierarchy.get(current_user.role, 0) < role_hierarchy.get(role, 0):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Se requiere rol {role.value} o superior",
            )
        return current_user

    return _check
