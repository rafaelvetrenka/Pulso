from fastapi import APIRouter
from pydantic import BaseModel
from src.schemas.message import MessageIn, MessageOut
from src.services.messages import handle_message
from src.core.settings import SERVICE_NAME, APP_VERSION
from fastapi import Depends
from src.core.security import require_api_key



router = APIRouter()


@router.post("/message", response_model=MessageOut, tags=["messages"], dependencies=[Depends(require_api_key)])
def receive_message(data: MessageIn):
    return handle_message(data)



class HealthOut(BaseModel):
    status: str
    service: str
    version: str


@router.get("/health", response_model=HealthOut, tags=["health"])
def health():
    return {
        "status": "ok",
        "service": SERVICE_NAME,
        "version": APP_VERSION
    }

