from django.db.models.functions import Lower
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """The user model inherits data from the auth0 user. Only name & email is used."""

    def __str__(self) -> str:
        return f"{self.username}"


class UserProduct(models.Model):
    """This model represents the relation of a user and a product.
    It's done this way so people could see what products other users use (future proof).
    """

    # Foreign keys
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.OneToOneField("Product", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user} & {self.product}"


class UserDish(models.Model):
    """This model represents the relation of a user and a dish."""

    # Foreign keys
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_dishes")
    dish = models.OneToOneField("Dish", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user} dish: {self.dish}"


class Product(models.Model):
    """This model represents a product. This can be seen as product or as an ingredient.
    It has a name and a boolean field to filter for favorites."""

    name = models.CharField(max_length=50, unique=True)
    is_favorite = models.BooleanField(default=False, blank=True)

    def __str__(self) -> str:
        return f"{self.name}"


class Dish(models.Model):
    """This model represents a Dish. It has a dish name and a recipe.
    is_favorite is added here too."""

    name = models.CharField(max_length=100, unique=True)
    recipe = models.TextField()
    is_favorite = models.BooleanField(default=False, blank=True)

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        ordering = ["name"]


class ProductDish(models.Model):
    """This model represents the relation between the product and a dish.
    A product can have a certain amount of products in a dish.
    Example: amount=4, unit=kg."""

    quantity = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    # Foreign key
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    unit = models.ForeignKey("Unit", on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.product}"

    def get_quantity_display(self):
        return f"{self.quantity:.0f}" if self.quantity % 1 == 0 else f"{self.quantity:.2f}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["product", "dish"], name="unique_product_dish"
            )
        ]
        ordering = [Lower("product__name")]


class Unit(models.Model):
    """This model represents the unit. It is used to measure a certain amount."""

    name = models.CharField(max_length=20)
    abbreviation = models.CharField(max_length=15)

    def __str__(self) -> str:
        return f"{self.name}"


class ShoppingList(models.Model):
    """This model represents the shopping list. Here all this is to link all the user to the list."""

    date = models.DateTimeField(auto_now_add=True)
    # Foreign key
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        local_time = timezone.localtime(self.date)  # Getting the local timezone.
        return f'{local_time.strftime("%Y-%m-%d %H:%M")} by: {self.user}'


class ProductShoppingList(models.Model):
    """This model represents the relation of a product with/in a shopping list.
    A user will be able to add products to his shopping list this way."""

    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    # Foreign keys
    product_dish = models.ForeignKey(ProductDish, on_delete=models.CASCADE)
    shoppinglist = models.ForeignKey(ShoppingList, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return f"{self.product_dish.product.name}"

    def get_quantity_display(self):
        return f"{self.quantity:.0f}" if self.quantity % 1 == 0 else f"{self.quantity:.2f}"

    class Meta:
        ordering = [Lower('product_dish__product__name')]


class UserMenu(models.Model):
    """This model represents the relation between a user and a menu."""

    menu = models.ForeignKey("MenuList", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.menu} from {self.user}"


class DishMenu(models.Model):
    """This model represents the relation between a menu and a dish."""

    menu = models.ForeignKey("MenuList", on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.menu} containing {self.dish}"


class MenuList(models.Model):
    """This model represents a menu. The menu contains an amount of dishes linked to the user."""

    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return f"{self.name}"


class BugReport(models.Model):
    """This is so that users can report bugs. Only the developer will be able to see this."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self) -> str:
        return f"{self.title}"
