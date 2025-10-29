 
from dotenv import load_dotenv
import os

load_dotenv()  # carrega as variáveis do arquivo .env na raiz do projeto

class Settings:
    def __init__(self):
        self.SUPABASE_URL = os.getenv("SUPABASE_URL", "")
        self.SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

        if not self.SUPABASE_URL or not self.SUPABASE_KEY:
            raise RuntimeError(
                "SUPABASE_URL ou SUPABASE_KEY não definidos no .env"
            )

settings = Settings()
