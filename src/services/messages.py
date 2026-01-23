from src.core.config import create_session, get_session
from src.schemas.message import MessageIn, MessageOut


def handle_message(payload: MessageIn) -> MessageOut:
    session_id = payload.session_id

    # Se não vier session_id ou se for desconhecido, cria nova sessão
    if not session_id or not get_session(session_id):
        session_id = create_session()

    session = get_session(session_id)

    # salva mensagem do usuário na sessão (simples)
    session.append({
        "from": "user",
        "message": payload.message,
        "metadata": payload.metadata
    })

    reply_text = "Pulso recebeu sua mensagem."

    # salva mensagem do assistente (placeholder)
    session.append({
        "from": "assistant",
        "message": reply_text
    })

    return MessageOut(
        reply=reply_text,
        session_id=session_id,
        handoff_required=False
    )
