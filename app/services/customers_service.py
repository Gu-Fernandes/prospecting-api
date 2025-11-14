from uuid import UUID

from fastapi import HTTPException

from app.schemas.customer import CustomerCreate, CustomerUpdate
from app.services.supabase_client import supabase


def _fetch_products_by_codes(codes: list[str]) -> list[dict]:
    if not codes:
        return []
    # case-sensitive (front seleciona da lista). Se quiser, normalize p/ upper().
    resp = supabase.table("products").select("id, code").in_("code", codes).execute()
    rows = getattr(resp, "data", None) or []
    found = {r["code"] for r in rows}
    missing = [c for c in codes if c not in found]
    if missing:
        raise HTTPException(status_code=400, detail=f"Produtos não encontrados: {', '.join(missing)}")
    return rows


def _replace_customer_products(customer_id: str, product_ids: list[str]) -> None:
    # apaga vínculos antigos
    supabase.table("customer_products").delete().eq("customer_id", customer_id).execute()
    # insere vínculos novos
    if product_ids:
        rows = [{"customer_id": customer_id, "product_id": pid} for pid in product_ids]
        supabase.table("customer_products").insert(rows).execute()


def insert_customer(payload: CustomerCreate) -> dict:
    base = payload.model_dump(exclude={"products"}, exclude_unset=True)
    # normaliza strings
    for k, v in list(base.items()):
        if isinstance(v, str):
            base[k] = v.strip()

    resp = supabase.table("customers").insert(base).execute()
    rows = getattr(resp, "data", None) or []
    if not rows:
        raise HTTPException(status_code=500, detail="Falha ao inserir cliente.")
    saved = rows[0]
    cid = saved["id"]

    # vincula produtos (se vierem)
    codes = (payload.products or [])
    if codes:
        prows = _fetch_products_by_codes(codes)
        _replace_customer_products(cid, [r["id"] for r in prows])

    return saved


def list_customers() -> list[dict]:
    # lê da VIEW para já trazer products: string[]
    resp = supabase.table("v_customers").select("*").order("created_at", desc=True).execute()
    return getattr(resp, "data", None) or []


def get_customer_by_id(customer_id: UUID) -> dict:
    resp = supabase.table("v_customers").select("*").eq("id", str(customer_id)).limit(1).execute()
    rows = getattr(resp, "data", None) or []
    if not rows:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    return rows[0]


def update_customer(customer_id: UUID, changes: CustomerUpdate) -> dict:
    # separa atualização base e substituição da lista de produtos
    body = changes.model_dump(exclude_unset=True)
    codes = body.pop("products", None)

    # normaliza strings
    for k, v in list(body.items()):
        if isinstance(v, str):
            body[k] = v.strip()

    if body:
        resp = supabase.table("customers").update(body).eq("id", str(customer_id)).execute()
        rows = getattr(resp, "data", None) or []
        if not rows:
            raise HTTPException(status_code=404, detail="Cliente não encontrado.")

    if codes is not None:
        prows = _fetch_products_by_codes(list(codes)) if codes else []
        _replace_customer_products(str(customer_id), [r["id"] for r in prows])

    # retorna da VIEW
    return get_customer_by_id(customer_id)


def delete_customer(customer_id: UUID) -> dict:
    resp = supabase.table("customers").delete().eq("id", str(customer_id)).execute()
    rows = getattr(resp, "data", None) or []
    if not rows:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    return rows[0]
