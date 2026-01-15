from fastapi import FastAPI
from store_app.db.database import SessionLocal
from store_app.api import category, product, auth, cart, review, favorite, social_auth
import uvicorn
from starlette.middleware.sessions import SessionMiddleware
from config import SECRET_KEY
from store_app.admin.setup import setup_admin



async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


store_app = FastAPI(title='Online Store')


store_app.include_router(category.category_router)
store_app.include_router(product.product_router)
store_app.include_router(auth.auth_router)
store_app.include_router(cart.cart_router)
store_app.include_router(review.review_router)
store_app.include_router(favorite.favorite_router)
store_app.include_router(social_auth.social_router)
store_app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
setup_admin(store_app)


if __name__ == '__main__':
    uvicorn.run(store_app, host='127.0.0.1', port=8000)