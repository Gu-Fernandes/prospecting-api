from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.customers import router as customers_router
from app.routers.auth import router as auth_router   

app = FastAPI(
    title="Prospecting API",
    version="0.0.1",
)

# Origens permitidas (local + produção Vercel + previews Vercel)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
        "https://prospeccao-clientes-iota.vercel.app",
    ],
    allow_origin_regex=r"https://.*\.vercel\.app$",  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas
app.include_router(auth_router)       # /auth/*
app.include_router(customers_router)  # /customers/*

@app.get("/health")
async def health_check():
    return {"status": "ok"}
