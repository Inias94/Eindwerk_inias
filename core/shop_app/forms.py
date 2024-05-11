from tkinter import Widget
from django import forms
from .models import Product, ProductInShoppingList


class ProductForm(forms.ModelForm):
    """This represents the form for the product model."""

    class Meta:
        model = Product
        fields = ['name', 'is_favorite']
        labels = {
            'name': 'Product name',
            'is_favorite': 'Add to favorite',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product name'
                }),
            'is_favorite': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'placeholder': 'Favorit?'
                }),
        }
        
        
class AddProductToShoppingListForm(forms.ModelForm):
    """Represents the form for adding products to a shopping list."""

    class Meta:
        model = ProductInShoppingList
        fields = ["product", "quantity", "unit"]
        labels = {
            'product': 'Product name',
            'quantity': 'quantity',
            'unit': 'unit'
        }
        widgets = {
            'product': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your product here...'
                }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control'
                }),
            'unit': forms.Select(attrs={
                'class': 'form-select'
                })
        }