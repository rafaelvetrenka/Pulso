import uuid
import enum
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, JSON, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from core.db import Base

# --- Enums (Definidos no PDF v2.1) ---
class SessionState(enum.Enum):
    NEW = "NEW"
    ACTIVE = "ACTIVE"
    WAITING_HUMAN = "WAITING_HUMAN"
    CLOSED = "CLOSED"

class MessageRole(enum.Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    HUMAN = "human"

# --- Tabela de Sessões ---
class Session(Base):
    __tablename__ = "sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # tenant_id = Column(UUID(as_uuid=True), nullable=False) 
    
    channel = Column(String, default="web", nullable=False)
    state = Column(Enum(SessionState), default=SessionState.NEW, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Metadados flexíveis (device, page, etc)
    metadata_ = Column("metadata", JSON, nullable=True) # "metadata" é reservado no python, usamos alias no banco

    # Relacionamento: Uma sessão tem várias mensagens
    messages = relationship("Message", back_populates="session", cascade="all, delete-orphan")

# --- Tabela de Mensagens ---
class Message(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.id"), nullable=False)
    
    role = Column(Enum(MessageRole), nullable=False)
    content = Column(Text, nullable=False)
    
    # Rastreabilidade (Obrigatório pelo PDF)
    request_id = Column(String, nullable=True)
    idempotency_key = Column(String, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    metadata_ = Column("metadata", JSON, nullable=True)

    # Relacionamento: Pertence a uma sessão
    session = relationship("Session", back_populates="messages")