from uuid import UUID

from fastapi import HTTPException

from app.schemas.product import ProductCreate, ProductUpdate
from app.services.supabase_client import supabase


def create_product(payload: ProductCreate) -> dict:
    code = (payload.code or "").strip()
    if not code:
        raise HTTPException(status_code=400, detail="Código obrigatório.")

    # unicidade case-insensitive
    exists = supabase.table("products").select("id").ilike("code", code).limit(1).execute()
    if (getattr(exists, "data", None) or []):
        raise HTTPException(status_code=409, detail="Produto já existe.")

    resp = supabase.table("products").insert({"code": code}).execute()
    rows = getattr(resp, "data", None) or []
    if not rows:
        raise HTTPException(status_code=500, detail="Falha ao criar produto.")
    return rows[0]


def list_products() -> list[dict]:
    resp = supabase.table("products").select("id, code, created_at").order("created_at", desc=True).execute()
    return getattr(resp, "data", None) or []


def get_product(product_id: UUID) -> dict:
    resp = (
        supabase.table("products")
        .select("id, code, created_at")
        .eq("id", str(product_id))
        .limit(1)
        .execute()
    )
    rows = getattr(resp, "data", None) or []
    if not rows:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    return rows[0]


def update_product(product_id: UUID, changes: ProductUpdate) -> dict:
    payload = changes.model_dump(exclude_unset=True, exclude_none=True)
    if "code" in payload:
        payload["code"] = payload["code"].strip()
        if not payload["code"]:
            raise HTTPException(status_code=400, detail="Código obrigatório.")

        # checa conflito (outro id com o mesmo code)
        conflict = (
            supabase.table("products")
            .select("id")
            .ilike("code", payload["code"])
            .neq("id", str(product_id))
            .limit(1)
            .execute()
        )
        if (getattr(conflict, "data", None) or []):
            raise HTTPException(status_code=409, detail="Já existe produto com este código.")

    resp = supabase.table("products").update(payload).eq("id", str(product_id)).execute()
    rows = getattr(resp, "data", None) or []
    if not rows:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    return rows[0]


def delete_product(product_id: UUID) -> dict: 
    resp = supabase.table("products").delete().eq("id", str(product_id)).execute()
    rows = getattr(resp, "data", None) or []
    if not rows:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    return rows[0]
