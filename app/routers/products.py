from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.deps import get_current_user
from app.schemas.product import ProductCreate, ProductInDB, ProductUpdate
from app.services.products_service import (
    create_product,
    delete_product,
    get_product,
    list_products,
    update_product,
)

router = APIRouter(
    prefix="/products",
    tags=["products"],
    dependencies=[Depends(get_current_user)],
)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ProductInDB)
def post_product(payload: ProductCreate):
    return create_product(payload)


@router.get("", response_model=List[ProductInDB])
def get_products():
    return list_products()


@router.get("/{product_id}", response_model=ProductInDB)
def get_product_by_id(product_id: UUID):
    return get_product(product_id)


@router.patch("/{product_id}", response_model=ProductInDB)
def patch_product(product_id: UUID, changes: ProductUpdate):
    return update_product(product_id, changes)


@router.delete("/{product_id}", response_model=dict)
def remove_product(product_id: UUID):
    deleted = delete_product(product_id)
    return {"message": f"Produto '{deleted.get('code')}' removido com sucesso.", "deleted": deleted}
