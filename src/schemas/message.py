from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class MessageIn(BaseModel):
    message: str = Field(..., min_length=1, description="Mensagem do usuário")
    session_id: Optional[str] = Field(None, description="ID da sessão (UUID). Se não enviado, será criado.")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Metadados opcionais do cliente (device, page, etc.)")


class MessageOut(BaseModel):
    reply: str = Field(..., description="Resposta do assistente")
    session_id: str = Field(..., description="ID da sessão (UUID)")
    handoff_required: bool = Field(..., description="True quando for necessário encaminhar para humano")
