from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import (
    Product,
    Dish,
    Unit,
    ShoppingList,
    UserProduct,
    UserDish,
    ProductDish,
    ProductShoppingList,
    UserMenu,
    DishMenu,
    MenuList,
    BugReport,
    User,
)


class UserModelTest(TestCase):
    """Test the User model."""

    def test_create_user(self):
        """Test creating a user."""
        user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )
        self.assertEqual(str(user), "testuser")


class ProductModelTest(TestCase):
    """Test the Product model."""

    def test_create_product(self):
        """Test creating a product."""
        product = Product.objects.create(name="Tomato", is_favorite=True)
        self.assertEqual(str(product), "Tomato")


class DishModelTest(TestCase):
    """Test the Dish model."""

    def test_create_dish(self):
        """Test creating a dish."""
        dish = Dish.objects.create(
            name="Tomato Soup", recipe="Tomatoes, water, salt", is_favorite=False
        )
        self.assertEqual(str(dish), "Tomato Soup")


class UnitModelTest(TestCase):
    """Test the Unit model."""

    def test_create_unit(self):
        """Test creating a unit."""
        unit = Unit.objects.create(name="Kilogram", abbreviation="kg")
        self.assertEqual(str(unit), "Kilogram")


class ShoppingListModelTest(TestCase):
    """Test the ShoppingList model."""

    def test_create_shopping_list(self):
        """Test creating a shopping list."""
        user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )
        shopping_list = ShoppingList.objects.create(user=user)
        self.assertIn(str(user), str(shopping_list))


class UserProductModelTest(TestCase):
    """Test the UserProduct model."""

    def test_create_user_product(self):
        """Test creating a user product."""
        user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )
        product = Product.objects.create(name="Tomato", is_favorite=True)
        user_product = UserProduct.objects.create(user=user, product=product)
        self.assertEqual(str(user_product), "testuser & Tomato")


class UserDishModelTest(TestCase):
    """Test the UserDish model."""

    def test_create_user_dish(self):
        """Test creating a user dish."""
        user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )
        dish = Dish.objects.create(
            name="Tomato Soup", recipe="Tomatoes, water, salt", is_favorite=False
        )
        user_dish = UserDish.objects.create(user=user, dish=dish)
        self.assertEqual(str(user_dish), "testuser dish: Tomato Soup")


class ProductDishModelTest(TestCase):
    """Test the ProductDish model."""

    def test_create_product_dish(self):
        """Test creating a product dish."""
        product = Product.objects.create(name="Tomato", is_favorite=True)
        dish = Dish.objects.create(
            name="Tomato Soup", recipe="Tomatoes, water, salt", is_favorite=False
        )
        product_dish = ProductDish.objects.create(
            product=product, dish=dish, quantity=2.5
        )
        self.assertEqual(str(product_dish), "Tomato")
        self.assertEqual(product_dish.get_quantity_display(), "2.50")


class ProductShoppingListModelTest(TestCase):
    """Test the ProductShoppingList model."""

    def test_create_product_shopping_list(self):
        """Test creating a product shopping list."""
        user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )
        shopping_list = ShoppingList.objects.create(user=user)
        product = Product.objects.create(name="Tomato", is_favorite=True)
        dish = Dish.objects.create(
            name="Tomato Soup", recipe="Tomatoes, water, salt", is_favorite=False
        )
        product_dish = ProductDish.objects.create(
            product=product, dish=dish, quantity=2.5
        )
        product_shopping_list = ProductShoppingList.objects.create(
            product_dish=product_dish, shoppinglist=shopping_list, quantity=3
        )
        self.assertEqual(str(product_shopping_list), "Tomato")
        self.assertEqual(product_shopping_list.get_quantity_display(), "3")


class UserMenuModelTest(TestCase):
    """Test the UserMenu model."""

    def test_create_user_menu(self):
        """Test creating a user menu."""
        user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )
        menu = MenuList.objects.create(name="Weekly Menu")
        user_menu = UserMenu.objects.create(user=user, menu=menu)
        self.assertEqual(str(user_menu), "Weekly Menu from testuser")


class DishMenuModelTest(TestCase):
    """Test the DishMenu model."""

    def test_create_dish_menu(self):
        """Test creating a dish menu."""
        menu = MenuList.objects.create(name="Weekly Menu")
        dish = Dish.objects.create(
            name="Tomato Soup", recipe="Tomatoes, water, salt", is_favorite=False
        )
        dish_menu = DishMenu.objects.create(menu=menu, dish=dish)
        self.assertEqual(str(dish_menu), "Weekly Menu containing Tomato Soup")


class MenuListModelTest(TestCase):
    """Test the MenuList model."""

    def test_create_menu_list(self):
        """Test creating a menu list."""
        menu = MenuList.objects.create(name="Weekly Menu")
        self.assertEqual(str(menu), "Weekly Menu")


class BugReportModelTest(TestCase):
    """Test the BugReport model."""

    def test_create_bug_report(self):
        """Test creating a bug report."""
        user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )
        bug_report = BugReport.objects.create(
            user=user,
            title="Bug in Recipe",
            description="Recipe is not saving correctly.",
        )
        self.assertEqual(str(bug_report), "Bug in Recipe")
