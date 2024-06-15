from django.urls import path

from .views.dish_views import *
from .views.index_views import *
from .views.menu_views import *
from .views.product_dish_views import *
from .views.product_views import *
from .views.shoppinglist_views import *
from .views.unit_views import *

# Login url is in the settings.py file. LOGIN_URL
# Logout url is in the authenticatiuon app: authenticaction.urls

urlpatterns = [
    # Homepage/index urls
    path("", IndexView.as_view(), name="index"),
    path("index/", IndexView.as_view(), name="index"),
    # Product
    path(
        "products/", ProductListView.as_view(), name="products"
    ),  # This only gives the products of the user
    # This url is disabled for now, currently no need to create a product that is not linked to any other object.
    # path('product/create/', ProductCreateView.as_view(), name='product_create'),
    # Dish
    path("dish/", DishListView.as_view(), name="dish_list"),
    path("dish/create/", DishCreateView.as_view(), name="dish_create"),
    path("dish/<int:pk>/", DishDetailView.as_view(), name="dish_detail"),
    path("dish/<int:pk>/update/", DishUpdateView.as_view(), name="dish_update"),
    path("dish/<int:pk>/delete/", DishDeleteView.as_view(), name="dish_delete"),
    # ProductDish
    path(
        "product_dish/<int:pk>/update/",
        ProductDishUpdateView.as_view(),
        name="product_dish_update",
    ),
    path(
        "product_dish/<int:pk>/delete/",
        ProductDishDeleteView.as_view(),
        name="product_dish_delete",
    ),
    # Shoppinglist
    path("shoppinglist", ShoppingListListView.as_view(), name="shoppinglist"),
    path(
        "shoppinglist/create/",
        ShoppingListCreateView.as_view(),
        name="shoppinglist_create",
    ),
    path(
        "shoppinglist/<int:pk>/update",
        ShoppingListUpdateView.as_view(),
        name="shoppinglist_update",
    ),
    # TODO Shoppinglist heeft nog nuttige functie!!
    # Unit
    path("unit/", UnitListView.as_view(), name="unit_list"),
    path("unit/create/", UnitCreateView.as_view(), name="unit_create"),
    path("unit/<int:pk>/update", UnitUpdateView.as_view(), name="unit_update"),
    path("unit/<int:pk>/delete/", UnitDeleteView.as_view(), name="unit_delete"),
    # Menu
    path("menu/", MenuListView.as_view(), name="menu_list"),
    path("menu/create/", MenuCreateView.as_view(), name="menu_create"),
    path("menu/<int:pk>/update", MenuUpdateView.as_view(), name="menu_update"),
]
