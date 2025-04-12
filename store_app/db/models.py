from sqlalchemy.orm import Mapped, mapped_column, relationship
from store_app.db.database import  Base
from typing import Optional, List
from enum import Enum as PyEnum
from sqlalchemy import String, Integer, Enum, Boolean, DateTime, ForeignKey, Text
from datetime import datetime
from passlib.hash import bcrypt

class StatusChoices(str, PyEnum):
    gold = 'gold'
    silver = 'silver'
    bronze = 'bronze'
    simple = 'simple'


class UserProfile(Base):
    __tablename__ = 'user_profile'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(32))
    last_name: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    status: Mapped[StatusChoices] = mapped_column(Enum(StatusChoices), default=StatusChoices.simple)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    tokens: Mapped[List['RefreshToken']] = relationship('RefreshToken', back_populates='user',
                                                        cascade='all, delete-orphan')
    product_owner: Mapped[List['Product']] = relationship('Product', back_populates='owner',
                                                          cascade='all, delete-orphan')
    review: Mapped[List['Review']] = relationship('Review', back_populates='author',
                                                  cascade='all, delete-orphan')
    cart_user: Mapped['Cart'] = relationship('Cart', back_populates='user',
                                             cascade='all, delete-orphan', uselist=False)
    favorite_user: Mapped[List['Favorite']] = relationship('Favorite', back_populates='user_favorite',
                                                           cascade='all, delete-orphan', uselist=False)


    def set_password(self, password: str):
        self.password = bcrypt.hash(password)

    def check_password(self, password: str):
        return bcrypt.verify(password, self.password)

    def __repr__(self):
        return f'{self.first_name}, {self.last_name}'


class RefreshToken(Base):
    __tablename__ = 'refresh_token'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))

    user: Mapped['UserProfile'] = relationship('UserProfile', back_populates='tokens')


class Category(Base):
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category_name: Mapped[str] = mapped_column(String(32), unique=True)

    product: Mapped[List['Product']] = relationship('Product', back_populates='category',
                                                    cascade='all, delete-orphan')

    def __repr__(self):
        return f'{self.category_name}'



class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_name: Mapped[str] = mapped_column(String(64))
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[int] = mapped_column(Integer)
    check_original: Mapped[bool] = mapped_column(Boolean, default=False)
    product_video: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))
    owner_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))

    category: Mapped['Category'] = relationship('Category', back_populates='product')
    owner: Mapped['UserProfile'] = relationship('UserProfile', back_populates='product_owner')
    review_product: Mapped[List['Review']] = relationship('Review', back_populates='product_review',
                                                          cascade='all, delete-orphan')

class Review(Base):
    __tablename__ = 'review'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    stars: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    author_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))

    author: Mapped['UserProfile'] = relationship('UserProfile', back_populates='review')
    product_review: Mapped['Product'] = relationship('Product', back_populates='review_product')


class Cart(Base):
    __tablename__ = 'cart'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'), unique=True)

    user: Mapped['UserProfile'] = relationship('UserProfile', back_populates='cart_user')
    items: Mapped[List['CartItem']] = relationship('CartItem', back_populates='cart',
                                                   cascade='all, delete-orphan')


class CartItem(Base):
    __tablename__ = 'cart_item'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey('cart.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))

    cart: Mapped['Cart'] = relationship('Cart', back_populates='items')
    product: Mapped['Product'] = relationship('Product')


class Favorite(Base):
    __tablename__ = 'favorite'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'), unique=True)

    user_favorite: Mapped['UserProfile'] = relationship('UserProfile', back_populates='favorite_user')
    favorite_item: Mapped[List['FavoriteItem']] = relationship('FavoriteItem', back_populates='favorite',
                                                               cascade='all, delete-orphan')

class FavoriteItem(Base):
    __tablename__ = 'favorite_item'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    favorite_id: Mapped[int] = mapped_column(ForeignKey('favorite.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))

    favorite: Mapped['Favorite'] = relationship('Favorite', back_populates='favorite_item')
    product_favorite: Mapped['Product'] = relationship('Product')


