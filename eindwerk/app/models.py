from django.utils import timezone

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """The user model inherits data from the auth0 user. Only name & email is used"""

    def __str__(self) -> str:
        return f'{self.username}'


class UserProduct(models.Model):
    """This model represents the relation of a user and a product.
    It's done this way so people could see what products other users use(future proof).
    """

    # Foreign keys
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE, unique=True)

    def __str__(self) -> str:
        return f"{self.user} & {self.product}"


class UserDish(models.Model):
    """This model represents the relation of a user and a dish."""

    # Foreign keys
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_dishes")
    dish = models.ForeignKey("Dish", on_delete=models.CASCADE, unique=True)

    def __str__(self) -> str:
        return f"{self.user} dish: {self.dish}"


class Product(models.Model):
    """This model represents a product. This can be seen as product or as an ingredient.
    It has a name and a boolean field to filter for favorites."""

    name = models.CharField(max_length=50, unique=True)
    is_favorite = models.BooleanField(default=False, blank=True)

    def __str__(self) -> str:
        return f'{self.name}'


class Dish(models.Model):
    """This model represents a Dish. It has a dish name and a recipe is_favorite is added here to."""

    name = models.CharField(max_length=50, unique=True)
    recipe = models.TextField()
    is_favorite = models.BooleanField(default=False, blank=True)

    def __str__(self) -> str:
        return f'{self.name}'

    class Meta:
        ordering = ['name']


class ProductDish(models.Model):
    """This model represents the relation betweeen the product and a dish.

    A product can have a certain amount of products in a dish.
    Example: amount=4, unit=kg"""

    quantity = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Foreign key
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    unit = models.ForeignKey("Unit", on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.product} in {self.dish}"

    class Meta:
        unique_together = ('product', 'dish')
        constraints = [
            models.UniqueConstraint(fields=['product', 'dish'],
                                    name='unique_product_dish')
        ]


class Unit(models.Model):
    """This model represents the unit. Is is used to measure a certain amount"""

    name = models.CharField(max_length=20)
    abbreviation = models.CharField(max_length=15)

    def __str__(self) -> str:
        return f'{self.name}'


class ShoppingList(models.Model):
    """This model represents the shoppinglist. Here all this is to link all the user to the list."""

    date = models.DateTimeField(auto_now_add=True)
    # Foreign key
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        local_time = timezone.localtime(self.date)  # Getting the local timezone.
        return f'{local_time.strftime("%Y-%m-%d %H:%M")} by: {self.user}'


class ProductShoppingList(models.Model):
    """This model represents the relation of a product with/in a shoppinglist.
    A user will be able to add products to his shoppinglist this way."""

    amount = models.PositiveBigIntegerField()

    # Foreign keys
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.DO_NOTHING)
    shoppinglist = models.ForeignKey(ShoppingList, on_delete=models.DO_NOTHING)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["product", "shoppinglist"],
                name="unique_product_shoppinglist",
            )
        ]

    def __str__(self) -> str:
        return f'{self.product}'


# TODO: MenuLijst: Relatie tussen gerechten en winkellijst

class MenuList(models.Model):
    """This model represents a menu. The menu contains an amount of dishes linked to the user"""

    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.dish}'
