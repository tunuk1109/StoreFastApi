from sqladmin import Admin
from fastapi import FastAPI
from .views import UserProfileAdmin, CategoryAdmin, ProductAdmin, ReviewAdmin, CartAdmin, FavoriteAdmin
from store_app.db.database import engine


def setup_admin(app: FastAPI):
    admin = Admin(app, engine)
    admin.add_view(UserProfileAdmin)
    admin.add_view(CategoryAdmin)
    admin.add_view(ProductAdmin)
    admin.add_view(ReviewAdmin)
    admin.add_view(CartAdmin)
    admin.add_view(FavoriteAdmin)