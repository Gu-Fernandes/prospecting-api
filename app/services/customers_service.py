from fastapi import HTTPException
from uuid import UUID

from app.schemas.customer import CustomerCreate, CustomerUpdate
from app.services.supabase_client import supabase


def insert_customer(payload: CustomerCreate) -> dict:
    row = payload.model_dump()

    resp = supabase.table("customers").insert(row).execute()

    data = getattr(resp, "data", None)
    if not data or len(data) == 0:
        raise HTTPException(
            status_code=500,
            detail="Falha ao inserir cliente no Supabase",
        )

    return data[0]


def list_customers() -> list[dict]:
    resp = (
        supabase
        .table("customers")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )

    data = getattr(resp, "data", None)
    if data is None:
        raise HTTPException(
            status_code=500,
            detail="Falha ao buscar clientes no Supabase",
        )

    return data


def update_customer(customer_id: UUID | str, changes: CustomerUpdate) -> dict:
    """
    Atualiza um cliente existente no Supabase com os campos enviados.
    Retorna o registro atualizado.
    """
    # Pydantic gera todos os campos, inclusive os None.
    # A gente só quer mandar pro Supabase os que realmente vieram.
    payload = {
        k: v
        for k, v in changes.model_dump().items()
        if v is not None
    }

    if not payload:
        # Nenhum campo pra atualizar
        raise HTTPException(
            status_code=400,
            detail="Nenhuma alteração fornecida.",
        )

    resp = (
        supabase
        .table("customers")
        .update(payload)
        .eq("id", str(customer_id))
        .execute()
    )

    data = getattr(resp, "data", None)

    if not data or len(data) == 0:
        # pode ser que não exista esse id
        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado ou não atualizado.",
        )

def delete_customer(customer_id: UUID | str) -> dict:
    """
    Remove um cliente pelo ID. Retorna o registro deletado.
    Se não existir, levanta 404.
    """

    resp = (
        supabase
        .table("customers")
        .delete()
        .eq("id", str(customer_id))
        .execute()
    )

    data = getattr(resp, "data", None)

    # O Supabase retorna em `data` as linhas deletadas.
    # Se vier vazio, é porque não encontrou nada com esse id.
    if not data or len(data) == 0:
        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado.",
        )
    

def get_customer_by_id(customer_id: UUID | str) -> dict:
    """
    Busca um único cliente pelo ID.
    Se não existir, levanta 404.
    """
    resp = (
        supabase
        .table("customers")
        .select("*")
        .eq("id", str(customer_id))
        .limit(1)
        .execute()
    )

    data = getattr(resp, "data", None)

    # se não achou nada com esse id
    if not data or len(data) == 0:
        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado.",
        )

    # retorna o primeiro (único)
    return data[0]    
 
