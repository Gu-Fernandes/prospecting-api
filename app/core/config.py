import os
from dotenv import load_dotenv

load_dotenv()  # carrega .env em dev

def _split_csv(env_name: str) -> list[str]:
    raw = os.getenv(env_name, "")
    return [p.strip() for p in raw.split(",") if p.strip()]

class Settings:
    # Supabase
    SUPABASE_URL = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
    SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY", "")

    # JWT
    JWT_SECRET = os.getenv("JWT_SECRET", "change-me")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "120"))
    JWT_EXPIRE_MINUTES = ACCESS_TOKEN_EXPIRE_MINUTES  # alias usado no código

    # “porteira” /auth/register
    ADMIN_SECRET = os.getenv("ADMIN_SECRET", "create-users-secret")

    # CORS
    CORS_ORIGINS = _split_csv("CORS_ORIGINS")
    CORS_REGEX = os.getenv("CORS_REGEX", "")

settings = Settings()
