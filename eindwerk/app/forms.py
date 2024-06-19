from django import forms
from .models import (
    ShoppingList,
    Product,
    ProductDish,
    Dish,
    Unit,
    MenuList,
    DishMenu,
    ProductShoppingList,
    BugReport,
)


class CapitalizeField(forms.CharField):
    """Custom formfield to capitalize the 1st word in a field."""

    def clean(self, value):
        value = super().clean(value)
        if value:
            words = value.split()
            if len(words) == 1:
                return value.capitalize()
            else:
                return value
        return value


class ProductForm(forms.ModelForm):
    """Form for creating an individual product. Products have a name and can be marked as favorites."""

    class Meta:
        model = Product
        fields = ["name", "is_favorite"]
        labels = {
            "name": "Product naam",
            "is_favorite": "Favoriet",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Product naam",
                }
            ),
            "is_favorite": forms.CheckboxInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Favoriet",
                }
            ),
        }

    def clean_name(self):
        name = self.cleaned_data.get("name", "")
        words = name.split()
        if len(words) == 1:
            return name.capitalize()
        else:
            return name


class ProductDishForm(forms.ModelForm):
    """Form for linking products to a dish with a certain amount and unit."""

    product_name = CapitalizeField(max_length=100, required=True, label="Product naam")
    product_is_favorite = forms.BooleanField(required=False, label="Favoriet")

    class Meta:
        model = ProductDish
        fields = ["product_name", "quantity", "unit", "product_is_favorite"]
        labels = {
            "product_name": "Product naam",
            "product_is_favorite": "Favoriet",
            "quantity": "Hoeveelheid",
            "unit": "Eenheid",
        }
        widgets = {
            "quantity": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Hoeveelheid",
                }
            ),
            "unit": forms.Select(
                attrs={
                    "class": "form-select",
                    "placeholder": "Maateenheid",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(ProductDishForm, self).__init__(*args, **kwargs)
        self.fields["product_name"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Product naam"}
        )
        self.fields["product_is_favorite"].widget.attrs.update(
            {"class": "form-check-input"}
        )


class DishForm(forms.ModelForm):
    """Form for creating a dish, a dish has a name, recipe and can be marked as favorite."""

    class Meta:
        model = Dish
        fields = ["name", "recipe", "is_favorite"]
        labels = {
            "name": "Gerecht",
            "is_favorite": "Favoriet",
            "recipe": "Recept",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Gerecht",
                }
            ),
            "recipe": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Recept",
                }
            ),
            "is_favorite": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                    "placeholder": "Favoriet",
                }
            ),
        }

    def clean_name(self):
        name = self.cleaned_data.get("name", "")
        words = name.split()
        if len(words) == 1:
            return name.capitalize()
        else:
            return name


class ShoppingListForm(forms.ModelForm):
    """Form for creating a new shopping list."""

    class Meta:
        model = ShoppingList
        fields = []


class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ["name", "abbreviation"]
        labels = {
            "name": "Maateenheid",
            "abbreviation": "Afkorting",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Maateenheid",
                }
            ),
            "abbreviation": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Afkorting",
                }
            ),
        }


class MenuForm(forms.ModelForm):
    class Meta:
        model = MenuList
        fields = ["name"]
        labels = {"name": "Menu-naam"}
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Menu-naam",
                }
            ),
        }

    def clean_name(self):
        name = self.cleaned_data.get("name", "")
        words = name.split()
        if len(words) == 1:
            return name.capitalize()
        else:
            return name


class DishMenuForm(forms.ModelForm):
    class Meta:
        model = DishMenu
        fields = ["dish"]
        widgets = {
            "dish": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
        }


class ProductShoppingListForm(forms.ModelForm):
    class Meta:
        model = ProductShoppingList
        fields = ["quantity"]
        labels = {
            "quantity": "Hoeveelheid",
            "product_name": "Product naam",
        }
        widgets = {
            "quantity": forms.NumberInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }


class BugReportForm(forms.ModelForm):
    class Meta:
        model = BugReport
        fields = ["title", "description"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Titel van een het probleem",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Beschrijving van het probleem",
                }
            ),
        }
        labels = {"title": "Probleem", "description": "Probleem beschrijving"}

    def clean_title(self):
        title = self.cleaned_data.get("title", "")
        words = title.split()
        if len(words) == 1:
            return title.capitalize()
        else:
            return title
