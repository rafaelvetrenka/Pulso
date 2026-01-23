import uuid

SESSIONS = {}


def create_session():
    session_id = str(uuid.uuid4())
    SESSIONS[session_id] = []
    return session_id


def get_session(session_id: str):
    return SESSIONS.get(session_id)
