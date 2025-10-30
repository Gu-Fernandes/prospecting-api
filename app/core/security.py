from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# Contexto de hashing de senha (bcrypt)
_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# === Senha ===
def hash_password(plain_password: str) -> str:
    """Gera hash seguro (bcrypt) para armazenar no banco."""
    return _pwd_context.hash(plain_password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    """Compara senha em texto puro com o hash armazenado."""
    try:
        return _pwd_context.verify(plain_password, password_hash)
    except Exception:
        return False


# === JWT ===
def create_access_token(
    subject: str,
    minutes: Optional[int] = None,
    extra_claims: Optional[Dict[str, Any]] = None,
) -> str:
    """
    Cria um JWT com claims padrão:
    - sub: subject (id do usuário)
    - iat/nbf/exp: tempos em epoch (UTC)
    """
    now = datetime.now(timezone.utc)
    exp_minutes = minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES

    payload: Dict[str, Any] = {
        "sub": subject,
        "iat": int(now.timestamp()),
        "nbf": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=exp_minutes)).timestamp()),
    }
    if extra_claims:
        payload.update(extra_claims)

    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return token


def decode_access_token(token: str) -> Dict[str, Any]:
    """
    Decodifica e valida o JWT.
    - Retorna o payload (dict) se válido.
    - Lança JWTError se inválido/expirado.
    """
    payload = jwt.decode(
        token,
        settings.JWT_SECRET,
        algorithms=[settings.JWT_ALGORITHM],
        options={"verify_aud": False},
    )
    # Se quiser garantir que 'sub' exista:
    if "sub" not in payload or not payload["sub"]:
        raise JWTError("Token sem 'sub'.")
    return payload
