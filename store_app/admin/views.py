from sqladmin import ModelView
from store_app.db.models import (UserProfile, Category, Product, Review,
                                 Cart, CartItem, Favorite, FavoriteItem)


class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [UserProfile.id, UserProfile.username, UserProfile.email]

class CategoryAdmin(ModelView, model=Category):
    column_list = [Category.id, Category.category_name]

class ProductAdmin(ModelView, model=Product):
    column_list = [Product.id, Product.product_name]

class ReviewAdmin(ModelView, model=Review):
    column_list = [Review.id, Review.author_id, Review.product_review]

class CartAdmin(ModelView, model=Cart):
    column_list = [Cart.user_id, Cart.user]

class FavoriteAdmin(ModelView, model=Favorite):
    column_list = [Favorite.user_id, Favorite.user_favorite]