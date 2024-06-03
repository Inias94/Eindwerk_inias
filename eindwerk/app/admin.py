from django.contrib import admin
from .models import Product, ProductDish, ProductShoppingList, ShoppingList, User, Unit, UserDish, UserProduct, Dish

admin.site.register(Product)
admin.site.register(ProductDish)
admin.site.register(ProductShoppingList)
admin.site.register(ShoppingList)
admin.site.register(User)
admin.site.register(Unit)
admin.site.register(UserDish)
admin.site.register(UserProduct)
admin.site.register(Dish)