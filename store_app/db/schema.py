from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr
from store_app.db.models import StatusChoices


class UserProfileSchema(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str]
    username: str
    password: str
    email: EmailStr
    age: Optional[int]
    phone_number: Optional[str]
    status: StatusChoices
    created_date: datetime

    class Config:
        from_attributes = True


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


class CategorySchema(BaseModel):
    id: int
    category_name: str

    class Config:
        from_attributes = True


class ProductSchema(BaseModel):
    id: int
    product_name: str
    description: str
    price: int
    check_original: bool
    product_video: Optional[str]
    created_date: datetime
    category_id: int
    owner_id: int

    class Config:
        from_attributes = True

class ReviewSchema(BaseModel):
    id: int
    stars: Optional[int]
    text: Optional[str]
    author_id: int
    product_id: int

    class Config:
        from_attributes = True


class CartItemSchema(BaseModel):
    id: int
    product_id: int

    class Config:
        from_attributes = True


class CartSchema(BaseModel):
    user_id: int
    items: List[CartItemSchema] = []
    total_price: float

    class Config:
        from_attributes = True


class CartItemCreateSchema(BaseModel):
    product_id: int

    class Config:
        from_attributes = True


class FavoriteItemSchema(BaseModel):
    id: int
    product_id: int

    class Config:
        from_attributes = True


class FavoriteSchema(BaseModel):
    user_id: int
    favorite_item: List[FavoriteItemSchema] = []

    class Config:
        from_attributes = True


class FavoriteItemCreateSchema(BaseModel):
    product_id: int

    class Config:
        from_attributes = True














