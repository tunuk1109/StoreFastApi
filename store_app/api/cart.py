from store_app.db.models import Cart, Product, CartItem
from store_app.db.schema import CartSchema, CartItemSchema, CartItemCreateSchema
from store_app.db.database import SessionLocal
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter


cart_router = APIRouter(prefix='/cart', tags=['Cart'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@cart_router.post('/', response_model=CartItemSchema)
async def cart_add(item_data: CartItemCreateSchema, user_id: int,
                   db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        cart = Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    product = db.query(Product).filter(Product.id == item_data.product_id).first()
    if not product:
        raise HTTPException(status_code=401, detail='Product not found')

    product_item = db.query(CartItem).filter(CartItem.cart_id == cart.id,
                                             CartItem.product_id == item_data.product_id).first()
    if product_item:
        raise HTTPException(status_code=401, detail='Product is already exist')

    cart_item = CartItem(cart_id=cart.id, product_id=item_data.product_id)
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return cart_item


@cart_router.get('/', response_model=CartSchema)
async def cart_list(user_id: int, db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        raise HTTPException(status_code=401, detail='Cart not found')

    cart_items = db.query(CartItem).filter(CartItem.cart_id == cart.id).all()

    total_price = sum(db.query(Product.price).filter(Product.id == item.product_id).scalar() for item in cart_items)

    return {
        'id': cart.id,
        'user_id': cart.user_id,
        'items': cart.items,
        'total_price': total_price
    }


@cart_router.delete('/{product_id}')
async def cart_delete(product_id: int, user_id: int, db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail='Cart not found')

    cart_item = db.query(CartItem).filter(CartItem.cart_id == cart.id,
                                          CartItem.product_id == product_id).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail='Product not found in cart')

    db.delete(cart_item)
    db.commit()
    return {'message': 'Product is deleted in Cart'}




















