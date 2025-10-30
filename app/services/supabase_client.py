from supabase import create_client, Client
from app.core.config import settings

if not settings.SUPABASE_URL:
    raise RuntimeError("SUPABASE_URL não definida no .env.")

key = settings.SUPABASE_SERVICE_KEY or settings.SUPABASE_KEY
if not key:
    raise RuntimeError("Defina SUPABASE_SERVICE_KEY (recomendado) ou SUPABASE_KEY no .env.")

supabase: Client = create_client(settings.SUPABASE_URL, key)
