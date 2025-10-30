# app/services/users_service.py
from typing import Optional
from fastapi import HTTPException, status

from app.services.supabase_client import supabase
from app.core.security import hash_password

TABLE = "users"

def get_user_by_email(email: str) -> Optional[dict]:
    res = supabase.table(TABLE).select("*").eq("email", email).limit(1).execute()
    rows = res.data or []
    return rows[0] if rows else None

def get_user_by_id(user_id: str) -> Optional[dict]:
    res = supabase.table(TABLE).select("*").eq("id", user_id).limit(1).execute()
    rows = res.data or []
    return rows[0] if rows else None

def create_user(email: str, password: str, name: Optional[str] = None) -> dict:
    # já cadastrado?
    if get_user_by_email(email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="E-mail já cadastrado.")

    pwd_hash = hash_password(password)

    # ❗ NADA de .select() aqui — apenas execute()
    res = supabase.table(TABLE).insert({
        "email": email,
        "password_hash": pwd_hash,
        "name": name,
    }).execute()

    rows = res.data or []
    if rows:
        return rows[0]

    # fallback seguro (caso o PostgREST não retorne representação)
    user = get_user_by_email(email)
    if user:
        return user

    raise HTTPException(status_code=500, detail="Falha ao inserir usuário.")
