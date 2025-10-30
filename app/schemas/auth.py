from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    name: str | None = None

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    name: str | None = None
    created_at: datetime

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginOut(TokenOut):
    user: UserOut
