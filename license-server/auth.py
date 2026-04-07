import os

from fastapi import Header, HTTPException


def verify_admin(x_admin_token: str | None = Header(default=None)):
    if x_admin_token is None or x_admin_token != os.getenv("ADMIN_TOKEN", "dev-token"):
        raise HTTPException(status_code=403, detail="Token inválido")
    return x_admin_token
