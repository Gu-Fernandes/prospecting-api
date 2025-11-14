from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    code: str = Field(..., min_length=1, max_length=255)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    code: Optional[str] = Field(None, min_length=1, max_length=255)


class ProductInDB(ProductBase):
    id: UUID
    created_at: datetime
