import uuid
from datetime import timedelta
from redis_client import redis_client
from fastapi import Header,HTTPException

def create_session(user_id):
    session_id = str(uuid.uuid4())
    redis_client.setex(f"session:{session_id}", timedelta(hours=24), value=user_id)
    return session_id

def get_user_id_from_session(session_id):
    return redis_client.get(f"session:{session_id}")

def get_current_user(session_token: str = Header(...)):
    user_id = get_user_id_from_session(session_token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired session")
    return user_id