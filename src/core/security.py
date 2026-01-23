from fastapi import Header, HTTPException
from src.core.settings import API_KEY


def require_api_key(x_api_key: str | None = Header(default=None, alias="X-API-Key")) -> None:
    # Se API_KEY não está configurada, não bloqueia (modo dev)
    if API_KEY == "":
        return

    if x_api_key is None or x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
