import pytest
from core.shop_app.models_prev_edition import Dish, Product, Unit


@pytest.fixture
def new_product():
    return Product(
        name="Cola",
        description="Frisdrank",
    )
