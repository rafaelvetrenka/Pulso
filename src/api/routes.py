from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class MessageIn(BaseModel):
    message: str


@router.post("/message")
def receive_message(data: MessageIn):
    return {
        "reply": "Pulso recebeu sua mensagem.",
        "echo": data.message
    }
