# Django imports
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from decimal import Decimal

# Project imports
from django.conf import settings
from ..models import ProductDish, MenuList, ShoppingList, ProductShoppingList
from ..forms import ProductShoppingListForm


"Nakijken of deze code nog van toepassing is!"
# class ShopListListView(LoginRequiredMixin, ListView):
#     """This view list"""
#     login_url = settings.LOGIN_URL
#     model = ShoppingList
#     template_name = "shoplist/list.html"


class ShoppingListDetailView(LoginRequiredMixin, DetailView):
    """This view shows all the details of the shopping list, products, units and amount.
    This only for shoppinglists related tot he user"""

    login_url = settings.LOGIN_URL
    model = ShoppingList
    context_object_name = "shoppinglist"
    template_name = "shoplist/detail.html"

    def get_queryset(self):
        return ShoppingList.objects.filter(user=self.request.user)


class CreateShoppingListFromMenuView(LoginRequiredMixin, View):
    login_url = settings.LOGIN_URL

    def get(self, request, *args, **kwargs):
        user = request.user
        menu_id = self.kwargs.get("menu_id")
        menu = get_object_or_404(MenuList, id=menu_id)

        shoppinglist = ShoppingList.objects.create(user=user)

        product_quantities = {}

        dishes = menu.dishmenu_set.all()  # Gets all DishMenu instances related to the menu.
        dish_ids = [dish_menu.dish_id for dish_menu in dishes]  # Extract dish IDs

        # Get all ProductDishes related to dishes in the menu
        product_dishes = ProductDish.objects.filter(dish_id__in=dish_ids)

        for product_dish in product_dishes:
            product_name = product_dish.product.name
            quantity = product_dish.quantity or 0

            # Use product_dish.unit instead of product_dish.product.unit
            unit = product_dish.unit

            # Check if (product_name, unit) already exists in product_quantities
            if (product_name, unit) in product_quantities:
                product_quantities[(product_name, unit)] += Decimal(quantity)
            else:
                product_quantities[(product_name, unit)] = Decimal(quantity)

        for (product_name, unit), total_quantity in product_quantities.items():
            # Get ProductDish where product name and unit match, and dish is in dishes
            product_dish = ProductDish.objects.filter(
                product__name=product_name, unit=unit, dish_id__in=dish_ids
            ).first()

            if product_dish:
                ProductShoppingList.objects.create(
                    product_dish=product_dish,
                    shoppinglist=shoppinglist,
                    quantity=total_quantity,
                )
            else:
                # Handle the case where product_dish is not found
                pass

        return redirect("shoppinglist_detail", pk=shoppinglist.pk)


class UpdateItemFromShoppingListView(LoginRequiredMixin, UpdateView):
    """View to update an item in a shopping list for a specified product related to the user."""

    login_url = settings.LOGIN_URL
    model = ProductShoppingList
    context_object_name = "product_shoppinglist_product"
    form_class = ProductShoppingListForm
    template_name = "shoplist/update.html"

    def get_queryset(self):
        return ProductShoppingList.objects.filter(shoppinglist__user=self.request.user)

    def get_success_url(self):
        # Haal de shoppinglist op van het item dat is bijgewerkt
        shoppinglist = self.object.shoppinglist
        # Ga terug naar de detailpagina van deze shoppinglist
        return reverse("shoppinglist_detail", kwargs={"pk": shoppinglist.pk})


class DeleteItemFromShoppingListView(LoginRequiredMixin, DeleteView):
    """View to delete an item in a shopping list for a specified product related to the user."""

    login_url = settings.LOGIN_URL
    model = ProductShoppingList
    context_object_name = "product_shoppinglist_product"
    template_name = "shoplist/delete_item.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        context['shoppinglist'] = obj.shoppinglist
        return context

    def get_success_url(self):
        shoppinglist = self.object.shoppinglist
        return reverse("shoppinglist_detail", kwargs={"pk": shoppinglist.pk})


class AddItemToShoppingListView(LoginRequiredMixin, CreateView):
    """View to add an item to a shopping list for a specified product related to the user."""
    login_url = settings.LOGIN_URL
    model = ProductShoppingList
    context_object_name = "product_shoppinglist_product"
    form_class = ProductShoppingListForm

    def get_queryset(self):
        return ProductShoppingList.objects.filter(user=self.request.user)