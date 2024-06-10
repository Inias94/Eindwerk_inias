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

    # This url is disabled for now, currently no need to create a product that is not linked to any other object.
    # path('product/create/', views.ProductCreateView.as_view(), name='product_create'),

    # Dish
    path('dish/', views.DishListView.as_view(), name='dish_list'),
    path('dish/create/', views.DishCreateView.as_view(), name='dish_create'),
    path('dish/<int:pk>/', views.DishDetailView.as_view(), name='dish_detail'),
    path('dish/<int:pk>/update/', views.DishUpdateView.as_view(), name='dish_update'),

    # ProductDish
    path('product_dish/<int:pk>/update/', views.ProductDishUpdateView.as_view(), name='product_dish_update'),
    path('product_dish/<int:pk>/delete/', views.ProductDishDeleteView.as_view(), name='product_dish_delete'),

    # Shoppinglist
    path('shoppinglist', views.ShoppingListListView.as_view(), name='shoppinglist'),
    path('shoppinglist/create/', views.ShoppingListCreateView.as_view(), name='shoppinglist_create'),
    path('shoppinglist/<int:pk>/update', views.ShoppingListUpdateView.as_view(), name='shoppinglist_update'),

    # Unit
    path('unit/', views.UnitListView.as_view(), name='unit_list'),
    path('unit/create/', views.UnitCreateView.as_view(), name='unit_create'),
]
