from store_app.db.models import Favorite, Product, FavoriteItem
from store_app.db.schema import FavoriteItemSchema, FavoriteSchema, FavoriteItemCreateSchema
from store_app.db.database import SessionLocal
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter


favorite_router = APIRouter(prefix='/favorite', tags=['Favorite'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@favorite_router.post('/', response_model=FavoriteItemSchema)
async def favorite_add(item_data: FavoriteItemCreateSchema, user_id: int,
                   db: Session = Depends(get_db)):
    favorite = db.query(Favorite).filter(Favorite.user_id == user_id).first()
    if not favorite:
        favorite = Favorite(user_id=user_id)
        db.add(favorite)
        db.commit()
        db.refresh(favorite)

    product = db.query(Product).filter(Product.id == item_data.product_id).first()
    if not product:
        raise HTTPException(status_code=401, detail='Product not found')

    product_item = db.query(FavoriteItem).filter(FavoriteItem.favorite_id == favorite.id,
                                             FavoriteItem.product_id == item_data.product_id).first()
    if product_item:
        raise HTTPException(status_code=401, detail='Product is already exist')

    favorite_item = FavoriteItem(favorite_id=favorite.id, product_id=item_data.product_id)
    db.add(favorite_item)
    db.commit()
    db.refresh(favorite_item)
    return favorite_item


@favorite_router.get('/', response_model=FavoriteSchema)
async def favorite_list(user_id: int, db: Session = Depends(get_db)):
    favorite = db.query(Favorite).filter(Favorite.user_id == user_id).first()
    if not favorite:
        raise HTTPException(status_code=401, detail='Favorite not found')
    return favorite


@favorite_router.delete('/{product_id}', response_model=dict)
async def favorite_delete(product_id: int, user_id: int, db: Session = Depends(get_db)):
    favorite = db.query(Favorite).filter(Favorite.user_id == user_id).first()
    if not favorite:
        raise HTTPException(status_code=404, detail='Cart not found')

    favorite_item = db.query(FavoriteItem).filter(FavoriteItem.favorite_id == favorite.id,
                                          FavoriteItem.product_id == product_id).first()

    if not favorite_item:
        raise HTTPException(status_code=404, detail='Product not found in cart')

    db.delete(favorite_item)
    db.commit()
    return {'message': 'Product is deleted in Favorite'}
