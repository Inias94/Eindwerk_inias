from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Dish,
    Product,
    DishProduct,
    ShoppingList,
    Unit,
    User,
    UserDish,
    UserProduct,
    ProductInShoppingList
)

admin.site.register(User)
admin.site.register(Dish)
admin.site.register(Product)
admin.site.register(DishProduct)
admin.site.register(ShoppingList)
admin.site.register(Unit)
admin.site.register(UserDish)
admin.site.register(UserProduct)
admin.site.register(ProductInShoppingList)
