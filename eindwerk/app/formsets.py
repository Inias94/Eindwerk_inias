# Django imports
from django.forms import inlineformset_factory

# Project imports
from .models import Dish, ProductDish
from .forms import ProductDishForm

# Formset for creating multiple products while creating a Dish.
ProductDishFormSet = inlineformset_factory(
    Dish, ProductDish, form=ProductDishForm, can_delete=True, extra=0
)
