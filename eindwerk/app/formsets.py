# Django imports
from django.forms import inlineformset_factory, modelformset_factory

# Project imports
from .models import Dish, ProductDish, DishMenu
from .forms import ProductDishForm, DishMenuForm

# Formset for creating multiple products while creating a Dish.
ProductDishFormSet = inlineformset_factory(
    Dish, ProductDish, form=ProductDishForm, can_delete=True, extra=1
)

# Formset for creating a menu with multiple dishes.
DishMenuFormSet = modelformset_factory(DishMenu, form=DishMenuForm, extra=0, can_delete=True)
