from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """This model represents a user. A user can have many products and dishes.

    Fields:
        products: is a many-to-many relationship with the Product model.
        dishes: is a many-to-many relationship with the Dish model.
    """

    products = models.ManyToManyField(
        "Product", through="UserProduct", related_name="users"
    )
    dishes = models.ManyToManyField("Dish", through="UserDish", related_name="users")

    def __str__(self) -> str:
        return super().__str__()


class Product(models.Model):
    """This model represents a product. Products have a name, a description and a unit.

    Fields:
        name: The name of the product.
        description: The description of the product.
        is_favorite: Add to favorite product.
    """

    name = models.CharField(max_length=100, unique=True, null=True)
    # description = models.TextField(null=True) MIJNEN BAAS VOND DIT NIET NODIG :-)
    is_favorite = models.BooleanField(blank=True, default=False)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f'{self.name}'


class Dish(models.Model):
    """This model repepresents a dish. Dishes have a name and a recipe. Dishes exist out ot multiple products.
    Dishes can be favorite.

    Fields:
        name: The name of the dish.
        recipe: The recipe of the dish.
        is_favorite: Add to favorite dish.
        products: is a many-to-many relationship with the Product model.
    """

    name = models.CharField(max_length=100, unique=True, null=True)
    recipe = models.TextField(null=True)
    is_favorite = models.BooleanField(blank=True, default=False)
    products = models.ManyToManyField(
        "Product", through="DishProduct", related_name="dishes"
    )

    def __str__(self) -> str:
        return f"<Dish: {self.name}>, <recipe: {self.recipe}>, <is_favorite: {self.is_favorite}>"


class Unit(models.Model):
    """This model represents a unit. Units are used to measure products.

    Fields:
        name: The name of the unit. (e.g. kilogram, grams, etc.)
        symbol: The symbol of the unit. (e.g. kg, g, etc.)
    """

    name = models.CharField(max_length=20, unique=True, null=True, blank=True)
    symbol = models.CharField(max_length=5, unique=True, null=True, blank=True)

    def __str__(self) -> str:
        return self.symbol

    def __repr__(self) -> str:
        return self.name


class UserProduct(models.Model):
    """This model represents the relation between a user and a product.

    Fields:
        user: The relation with the user
        product: The relation with the product
        quantity: The quantity of the product
        unit: The unit of the product
    """

    user = models.ForeignKey("User", on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    unit = models.ForeignKey("Unit", on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        """This Meta class defines that the relation between a user and a product needs to be unique."""

        unique_together = ("user", "product")

    def __str__(self) -> str:
        return f"<UserProduct: {self.user} - {self.product} - {self.quantity}>"


class UserDish(models.Model):
    """This model represents the relation between a user and a dish.

    Fields:
        user: The relation with the user
        dish: The relation with the dish
        quantity: The quantity of the dish
        unit: The unit of the dish
    """

    user = models.ForeignKey("User", on_delete=models.CASCADE)
    dish = models.ForeignKey("Dish", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    unit = models.ForeignKey("Unit", on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        """This Meta class defines that the relation between a user and a dish needs to be unique."""

        unique_together = ("user", "dish")

    def __str__(self) -> str:
        return f"<UserDish: {self.user} - {self.dish} - {self.quantity}>"


class DishProduct(models.Model):
    """This model represents the relation between a dish and a product.

    Fields:
        dish: The relation with the dish
        product: The relation with the product
        quantity: The quantity of the product
        unit: The unit of the product
    """

    dish = models.ForeignKey("Dish", on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    unit = models.ForeignKey("Unit", on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        """This Meta class defines that the relation between a dish and a product needs to be unique."""

        unique_together = ("dish", "product")

    def __str__(self) -> str:
        return f"<DishProduct: {self.dish} - {self.product} - {self.quantity}>"


class ShoppingList(models.Model):
    """This model represents a shopping list. A user will be able to fill this with products. (Dishes will be able to be added to.)

    Fields:
        user: The relation with the user
    """

    user = models.ForeignKey("User", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"<Shoppinglist: {self.user}>"


class ProductInShoppingList(models.Model):
    """This model represents the relation between a product and the shopping list.

    Fields:
        product: The relation with the product
        shopping_list: The relation with the shopping list
        quantity: The quantity of the product
        unit: The unit of the product
    """

    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    shopping_list = models.ForeignKey("ShoppingList", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    unit = models.ForeignKey("Unit", on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        """This Meta class defines that the relation between a product and a shopping list needs to be unique."""

        unique_together = ("product", "shopping_list")

    def __str__(self) -> str:
        return f"<ProductInShoppingList: {self.product} - {self.shopping_list} - {self.quantity}>"
