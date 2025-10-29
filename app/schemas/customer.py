from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from uuid import UUID
from typing import Optional


class CustomerCreate(BaseModel):
    company: str = Field(..., min_length=1, max_length=255)
    cnpj: str = Field(..., min_length=1, max_length=32)
    responsible: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    phone: str = Field(..., min_length=1, max_length=32)
    main_product: str = Field(..., min_length=1, max_length=255)
    sku: str = Field(..., min_length=1, max_length=255)
    supplier: str = Field(..., min_length=1, max_length=255)


class CustomerInDB(CustomerCreate):
    id: UUID
    created_at: datetime

class CustomerUpdate(BaseModel):
    company: Optional[str] = Field(None, min_length=1, max_length=255)
    cnpj: Optional[str] = Field(None, min_length=1, max_length=32)
    responsible: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, min_length=1, max_length=32)
    main_product: Optional[str] = Field(None, min_length=1, max_length=255)
    sku: Optional[str] = Field(None, min_length=1, max_length=255)
    supplier: Optional[str] = Field(None, min_length=1, max_length=255)
