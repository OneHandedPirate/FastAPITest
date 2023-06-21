from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field


class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: str = Field(min_length=5)
    password: str = Field(min_length=8)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class EmployeeResponse(BaseModel):
    salary: float
    promotion_date: datetime

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda dt: dt.strftime('%d.%m.%Y')
        }
