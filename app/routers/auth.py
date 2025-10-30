 
from fastapi import APIRouter, HTTPException, status, Header, Depends
from app.core.config import settings
from app.core.security import verify_password, create_access_token
from app.schemas.auth import UserCreate, LoginIn, UserOut, LoginOut
from app.services.users_service import create_user, get_user_by_email
from app.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut, status_code=201)
def register_user(body: UserCreate, x_admin_secret: str = Header(default="")):
    if x_admin_secret != settings.ADMIN_SECRET:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Chave de administração inválida.")
    try:
        user = create_user(body.email, body.password, body.name)
        return {
            "id": user["id"],
            "email": user["email"],
            "name": user.get("name"),
            "created_at": user["created_at"],
        }
    except HTTPException:
        raise
    except Exception as e:
        # agora o 500 vem em JSON com detalhe útil
        raise HTTPException(status_code=500, detail=f"Erro ao registrar: {e}")

@router.post("/login", response_model=LoginOut)
def login(body: LoginIn):
    user = get_user_by_email(body.email)
    if not user or not verify_password(body.password, user.get("password_hash", "")):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="E-mail ou senha inválidos.")
    token = create_access_token(str(user["id"]))
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "email": user["email"],
            "name": user.get("name"),
            "created_at": user["created_at"],
        },
    }

@router.get("/me", response_model=UserOut)
def me(current_user=Depends(get_current_user)):
    return {
        "id": current_user["id"],
        "email": current_user["email"],
        "name": current_user.get("name"),
        "created_at": current_user["created_at"],
    }
