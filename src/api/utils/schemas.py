from pydantic import BaseModel
from typing import Optional, List

class ProductBaseModel(BaseModel):
    name: str
    description: Optional[str]
    price: int

# class ProductCreateModel(ProductBaseModel):
#     user_id: int

class ProductUpdateModel(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[int]

class ProductResponseModel(ProductBaseModel):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class User(BaseModel):
    name: str
    email: str
    password: str

class UserResponseModel(BaseModel):
    name: str
    email: str
    products: Optional[List[ProductBaseModel]] = None  

class UserUpdateModel(BaseModel):
    name: str


class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
