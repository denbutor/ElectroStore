from typing import Any

from pydantic import BaseModel, EmailStr, Field, ConfigDict

class UserUpdate(BaseModel):
    email: EmailStr
    name: str
    surname: str
    phone_number: str = Field(min_length=10, max_length=13)
    city: str
    nova_post_department: str
    password: str = Field(min_length=8)

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    name: str
    surname: str
    phone_number: str = Field(min_length=10, max_length=13)
    city: str
    nova_post_department: str
    password: str = Field(min_length=8)


    class Config:
        from_attributes = True

        @classmethod
        def model_validate(cls, obj: Any):
            return super().model_validate(obj)

class UserResponse(UserBase):
    id: int
    role: str
    name: str
    surname: str
    phone_number: str = Field(min_length=10, max_length=13)
    city: str
    nova_post_department: str

    class Config:
        from_attributes = True

class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse