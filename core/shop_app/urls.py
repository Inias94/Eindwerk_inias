from django.urls import path

from . import views
from .views import (
    AddProductToShoppingListView,
    AddProductView,
    IndexView,
    ProductInShoppingListView,
    ProductListView,
    logout,
)

app_name = 'shop_app'

urlpatterns = [

    # Main path.
    path('', IndexView.as_view(), name='index'),
    path('index/', IndexView.as_view(), name='index'),

    # Products.
    path('product-list/', ProductListView.as_view(), name='product-list'),
    path('product/add/', AddProductView.as_view(), name='product-add'),
    # path('create-product/', views.create_product, name='create-product'),

    # Dish.
    # path('dish/add/', AddDishView.as_view(), name='dish-add'),
    
    # Products in shopping list.
    path('product_shoppinglist_list/', ProductInShoppingListView.as_view(), name='product_shoppinglist_list'),
    path('product_shoppinglist/add', AddProductToShoppingListView.as_view(), name='product_shoppinglist_add'),



    # Authentication.
    # Login is handled by social-django combined with social-auth
    path('logout/', logout, name='logout'),

]
