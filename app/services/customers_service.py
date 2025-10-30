from uuid import UUID
from fastapi import HTTPException
from app.schemas.customer import CustomerCreate, CustomerUpdate
from app.services.supabase_client import supabase


def insert_customer(payload: CustomerCreate) -> dict:
    data = payload.model_dump()
    # normaliza strings
    for k, v in list(data.items()):
        if isinstance(v, str):
            data[k] = v.strip()

    resp = supabase.table("customers").insert(data).execute()
    rows = getattr(resp, "data", None) or []
    if not rows:
        raise HTTPException(status_code=500, detail="Falha ao inserir cliente.")
    return rows[0]


def list_customers() -> list[dict]:
    # aqui pode usar select() porque é operação de leitura
    resp = supabase.table("customers").select("*").order("created_at", desc=True).execute()
    return getattr(resp, "data", None) or []


def get_customer_by_id(customer_id: UUID) -> dict:
    resp = supabase.table("customers").select("*").eq("id", str(customer_id)).limit(1).execute()
    rows = getattr(resp, "data", None) or []
    if not rows:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    return rows[0]


def update_customer(customer_id: UUID, changes: CustomerUpdate) -> dict:
    payload = changes.model_dump(exclude_unset=True, exclude_none=True)
    if not payload:
        raise HTTPException(status_code=400, detail="Nenhum campo para atualizar.")

    for k, v in list(payload.items()):
        if isinstance(v, str):
            payload[k] = v.strip()

    resp = supabase.table("customers").update(payload).eq("id", str(customer_id)).execute()
    rows = getattr(resp, "data", None) or []
    if not rows:
        # se não atualizou nada, é provável que o ID não exista
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    return rows[0]


def delete_customer(customer_id: UUID) -> dict:
    resp = supabase.table("customers").delete().eq("id", str(customer_id)).execute()
    rows = getattr(resp, "data", None) or []
    if not rows:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    return rows[0]
