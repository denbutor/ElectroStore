from pydantic import BaseModel, EmailStr, Field


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

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True

class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse