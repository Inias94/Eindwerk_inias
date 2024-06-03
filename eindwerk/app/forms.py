from django import forms

from .models import ShoppingList, Product, ProductDish, Dish, Unit


class ProductForm(forms.ModelForm):
    """Form for creating an individual product. Products have a name and can be marked as favorites."""

    class Meta:
        model = Product
        fields = ['name', 'is_favorite']
        labels = {
            'name': 'Product name',
            'is_favorite': 'Favorite?',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Product name',
            }),
            'is_favorite': forms.CheckboxInput(attrs={
                'class': 'form-control',
                'placeholder': 'Favorite?',
            })
        }


class ProductDishForm(forms.ModelForm):
    """Form for linking products to a dish with a certain amount and unit."""
    
    product_name = forms.CharField(max_length=100, required=True, label='Product Name')
    product_is_favorite = forms.BooleanField(required=False, label='Product is Favorite')

    class Meta:
        model = ProductDish
        fields = ['quantity', 'unit']
        widgets = {
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Amount',
            }),
            'unit': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Unit',
            })
        }
    
    def save(self, commit=True):
        product_name = self.cleaned_data.get('product_name')
        product_is_favorite = self.cleaned_data.get('product_is_favorite')
        product, created = Product.objects.get_or_create(name=product_name, defaults={'is_favorite': product_is_favorite})
        self.instance.product = product
        return super().save(commit)



class DishForm(forms.ModelForm):
    """Form for creating a dish, a dish has a name, recipe and can be marked as favorite."""

    class Meta:
        model = Dish
        fields = ['name', 'recipe', 'is_favorite']
        labels = {
            'name': 'Dish name',
            'is_favorite': 'Favorite?',
            'recipe': 'Recipe',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dish name',
            }),
            'recipe': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Recipe',
            }),
            'is_favorite': forms.CheckboxInput(attrs={
                'class': 'form-control',
                'placeholder': 'Favorite?',
            })
        }


class ShoppingListForm(forms.ModelForm):
    """Form for creating a new shopping list."""

    class Meta:
        model = ShoppingList
        fields = []


class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['name', 'abbreviation']
        labels = {
            'name': 'Unit name',
            'abbreviation': 'Unit abbreviation',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Unit name',
            }),
            'abbreviation': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Unit abbreviation',
            })
        }
