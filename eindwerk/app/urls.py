from django.urls import path

from . import views

# Login url is in the settings.py file. LOGIN_URL
# Logout url is in the authenticatiuon app: authenticaction.urls

urlpatterns = [
    # Homepage/index urls
    path('', views.IndexView.as_view(), name='index'),
    path('index/', views.IndexView.as_view(), name='index'),

    # Product
    path('products/', views.ProductListView.as_view(), name='products'),
    # path('product/create/', views.ProductCreateView.as_view(), name='product_create'),


    # Dish
    path('dish/', views.DishListView.as_view(), name='dish_list'),
    path('dish/create/', views.create_dish, name='dish_create'),
    # path('add_productform_to_create_dish/', views.add_productform_to_create_dish, name='add_productform_to_create_dish'),
    # path('dish/create/', views.DishCreateView.as_view(), name='dish_create'),

    
    # Shoppinglist
    path('shoppinglist', views.ShoppingListListView.as_view(), name='shoppinglist'),
    path('shoppinglist/create/', views.ShoppingListCreateView.as_view(), name='shoppinglist_create'),
    path('shoppinglist/<int:pk>/update', views.ShoppingListUpdateView.as_view(), name='shoppinglist_update'),


    # Unit
    path('unit/', views.UnitListView.as_view(), name='unit_list'),
    path('unit/create/', views.UnitCreateView.as_view(), name='unit_create'),
]