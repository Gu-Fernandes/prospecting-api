from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class CustomerBase(BaseModel):
    company: str = Field(..., min_length=1, max_length=255)
    cnpj: str = Field(..., min_length=1, max_length=32)
    responsible: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    phone: str = Field(..., min_length=1, max_length=32)

    # mantidos no cliente (não por produto)
    sku: Optional[str] = None
    supplier: Optional[str] = None


class CustomerCreate(CustomerBase):
    # códigos de produto (devem existir em products)
    products: Optional[List[str]] = None


class CustomerInDB(CustomerBase):
    id: UUID
    created_at: datetime 
    products: List[str] = []


class CustomerUpdate(BaseModel):
    company: Optional[str] = Field(None, min_length=1, max_length=255)
    cnpj: Optional[str] = Field(None, min_length=1, max_length=32)
    responsible: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, min_length=1, max_length=32)

    sku: Optional[str] = None
    supplier: Optional[str] = None 
    products: Optional[List[str]] = None
