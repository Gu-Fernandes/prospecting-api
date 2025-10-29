from fastapi import APIRouter, status, HTTPException
from uuid import UUID

from app.schemas.customer import (
    CustomerCreate,
    CustomerInDB,
    CustomerUpdate,
)
from app.services.customers_service import (
    insert_customer,
    list_customers,
    update_customer,
    delete_customer,
    get_customer_by_id
)

router = APIRouter(
    prefix="/customers",
    tags=["customers"],
)

@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=dict,
)
async def create_customer(payload: CustomerCreate):
    """
    Cria um novo cliente no Supabase e retorna mensagem + dados salvos.
    """
    try:
        saved = insert_customer(payload)

        return {
            "message": f"{payload.company} cadastrado com sucesso!",
            "data": saved,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro inesperado ao salvar cliente: {str(e)}",
        )


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[CustomerInDB],
)
async def get_customers():
    """
    Retorna todos os clientes cadastrados (mais recentes primeiro).
    """
    try:
        return list_customers()

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro inesperado ao buscar clientes: {str(e)}",
        )


@router.patch(
    "/{customer_id}",
    status_code=status.HTTP_200_OK,
    response_model=CustomerInDB,
)
async def patch_customer(customer_id: UUID, changes: CustomerUpdate):
    """
    Atualiza parcialmente um cliente existente.
    Você pode mandar só os campos que deseja alterar.
    """
    try:
        updated = update_customer(customer_id, changes)
        return updated

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro inesperado ao atualizar cliente: {str(e)}",
        )


@router.delete(
    "/{customer_id}",
    status_code=status.HTTP_200_OK,
    response_model=dict,
)
async def remove_customer(customer_id: UUID):
    """
    Remove definitivamente um cliente.
    Retorna info básica da linha deletada.
    """
    try:
        deleted = delete_customer(customer_id)
        return {
            "message": f"Cliente '{deleted.get('company')}' removido com sucesso.",
            "deleted": deleted,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro inesperado ao remover cliente: {str(e)}",
        )


@router.get(
    "/{customer_id}",
    status_code=status.HTTP_200_OK,
    response_model=CustomerInDB,
)
async def get_customer(customer_id: UUID):
    """
    Retorna um cliente específico pelo ID.
    """
    try:
        customer = get_customer_by_id(customer_id)
        return customer

    except HTTPException:
        # se o service já levantou HTTPException (404, etc), repassa
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro inesperado ao buscar cliente: {str(e)}",
        )