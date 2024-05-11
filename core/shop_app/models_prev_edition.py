# from django.contrib.auth.models import AbstractUser
# from django.db import models


# class User(AbstractUser):
#     products = models.ManyToManyField(
#         "Product", through="UserProduct", related_name="users"
#     )
#     dishes = models.ManyToManyField("Dish", through="UserDish", related_name="users")

#     def __repr__(self):
#         return f"<User: {self.username}>"


# class UserProduct(models.Model):
#     """
#     This model represents the relation of a user and a product.

#     Args:
#         models (_type_): _description_
#         user (ForeignKey): The user that has the product.
#         product (ForeignKey): The product that the user has.
#         amount (DecimalField): The amount of the product that the user has.
#     """

#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     product = models.ForeignKey("Product", on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

#     def __repr__(self) -> str:
#         return f"<UserProduct: {self.user} - has {self.amount} of {self.product}>"


# class UserDish(models.Model):
#     """This model represents the relation of a user and a dish.

#     Args:
#         models (_type_): _description_
#         user (ForeignKey): The user that has the dish.
#         dish (ForeignKey): The dish that the user has.
#     """

#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     dish = models.ForeignKey("Dish", on_delete=models.CASCADE)

#     def __repr__(self) -> str:
#         return f"<UserDish: {self.user} - has {self.dish}>"


# class Product(models.Model):
#     """
#     This model represents a product. Products have a name, a description and a unit.

#     Args:
#         models (_type_): _description_
#         name (CharField): The name of the product.
#         description (TextField): The description of the product.
#         units (ManyToManyField): The units of the product (kg/l,etc...).
#     """

#     name = models.CharField(max_length=100, unique=True)
#     description = models.TextField()
#     is_favorite = models.BooleanField(default=False, blank=True)
#     units = models.ForeignKey("Unit", on_delete=models.CASCADE)

#     def __repr__(self) -> str:
#         return f"<Product: {self.name}>, <description: {self.description}>, <units: {self.units}>, <is_favorite: {self.is_favorite}>"


# class Dish(models.Model):
#     """This model repepresents a dish. Dishes have a name and a recipe. Dishes exist out ot multiple products.

#     Args:
#         models (_type_): _description_
#         name (CharField): The name of the dish.
#         recipe (TextField): The recipe of the dish.
#     """

#     name = models.CharField(max_length=100, unique=True)
#     recipe = models.TextField()
#     is_favorite = models.BooleanField(default=False, blank=True)

#     def __repr__(self) -> str:
#         return f"<Dish: {self.name}>, <recipe: {self.recipe}>, <is_favorite: {self.is_favorite}>"


# class ProductInDish(models.Model):
#     """
#     This model represents the relationship of a product and a dish.

#     Args:
#         models (_type_): _description_
#         product (ForeignKey): The product that is in the dish.
#         dish (ForeignKey): The dish that the product is in.
#         quantity (DecimalField): The quantity of the product in the dish.
#     """

#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
#     quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)

#     def __repr__(self) -> str:
#         return f"<ProductInDish: {self.product} - has {self.quantity} of {self.dish}>"


# class Unit(models.Model):
#     """
#     This model represents the units of a product.
#     Units are used to measure the quantity of a product.
#     This can be kg, g, ml and just an amount of items as well.

#     Args:
#         models (_type_): _description_
#         name (CharField): The name of the unit (kilogram, liters, grams, etc).
#         abbreviation (CharField): The abbreviation of the unit (kg, l, g, etc).
#     """

#     KILOGRAM = "kilogram"
#     GRAM = "gram"
#     LITER = "liter"
#     CENTILITER = "centiliter"
#     MILLILITER = "milliliter"
#     HOEVEELHEID = "hoeveelheid"

#     UNITS_CHOICES = (
#         (KILOGRAM, "kg"),
#         (GRAM, "g"),
#         (LITER, "l"),
#         (CENTILITER, "cl"),
#         (MILLILITER, "ml"),
#         (HOEVEELHEID, "aantal"),
#     )

#     # name = models.CharField(max_length=100, choices=UNITS_CHOICES)
#     abbreviation = models.CharField(max_length=15, choices=UNITS_CHOICES)

#     def __str__(self):
#         return f"{self.get_abbreviation_display()}"


# class ShoppingList(models.Model):
#     """
#     This model represents the users shopping list.

#     Args:
#         models (_type_): _description_
#         user (ForeignKey): The user that has the shopping list.
#         products (ManyToManyField): The products in the shopping list.
#         created_at (DateTimeField): The time the shopping list was created.
#         updated_at (DateTimeField): The time the shopping list was updated.
#     """

#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     products = models.ManyToManyField(Product)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __repr__(self) -> str:
#         return f"<ShoppingList: {self.user} - has {self.products}>"
