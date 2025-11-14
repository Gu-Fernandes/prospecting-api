from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status

from app.deps import get_current_user
from app.schemas.customer import CustomerCreate, CustomerInDB, CustomerUpdate
from app.services.customers_service import (
    delete_customer,
    get_customer_by_id,
    insert_customer,
    list_customers,
    update_customer,
)

router = APIRouter(
    prefix="/customers",
    tags=["customers"],
    dependencies=[Depends(get_current_user)],
)

@router.post("", status_code=status.HTTP_201_CREATED, response_model=CustomerInDB)
def create_customer(payload: CustomerCreate):
    return insert_customer(payload)

@router.get("", response_model=list[CustomerInDB])
def get_customers():
    return list_customers()

@router.get("/{customer_id}", response_model=CustomerInDB)
def get_customer(customer_id: UUID):
    return get_customer_by_id(customer_id)

@router.patch("/{customer_id}", response_model=CustomerInDB)
def patch_customer(customer_id: UUID, changes: CustomerUpdate):
    if not changes.model_dump(exclude_unset=True, exclude_none=True):
        raise HTTPException(status_code=400, detail="Nenhum campo para atualizar.")
    return update_customer(customer_id, changes)

@router.delete("/{customer_id}", response_model=dict)
def remove_customer(customer_id: UUID):
    deleted = delete_customer(customer_id)
    return {
        "message": f"Cliente '{deleted.get('company')}' removido com sucesso.",
        "deleted": deleted,
    }
