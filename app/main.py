from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.customers import router as customers_router

app = FastAPI(
    title="Prospecting API",
    version="0.0.1",
)

origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001",
    "https://prospeccao-clientes-iota.vercel.app/prospecting",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(customers_router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}
