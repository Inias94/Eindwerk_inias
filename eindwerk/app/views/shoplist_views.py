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


class ShopListListView(LoginRequiredMixin, ListView):
    """This view give a list of the users shopping lists"""
    login_url = settings.LOGIN_URL
    model = ShoppingList
    template_name = "shoplist/list.html"


class ShoppingListDetailView(LoginRequiredMixin, DetailView):

    login_url = settings.LOGIN_URL
    model = ShoppingList
    context_object_name = "shoppinglist"
    template_name = "shoplist/detail.html"


class CreateShoppingListFromMenuView(LoginRequiredMixin, View):
    login_url = settings.LOGIN_URL

    def get(self, request, *args, **kwargs):
        user = request.user
        menu_id = self.kwargs.get("menu_id")
        menu = get_object_or_404(MenuList, id=menu_id)

        shoppinglist = ShoppingList.objects.create(user=user)

        product_quantities = {}

        dishes = menu.dishmenu_set.all()
        for dish_menu in dishes:
            dish = dish_menu.dish
            product_dishes = ProductDish.objects.filter(dish=dish)

            for product_dish in product_dishes:
                product_name = product_dish.product.name
                quantity = product_dish.quantity or 0

                if product_name in product_quantities:
                    product_quantities[product_name] += Decimal(quantity)
                else:
                    product_quantities[product_name] = quantity

        for product_name, total_quantity in product_quantities.items():
            product_dish = ProductDish.objects.filter(
                product__name=product_name, dish__in=[dm.dish for dm in dishes]
            ).first()
            ProductShoppingList.objects.create(
                product_dish=product_dish,
                shoppinglist=shoppinglist,
                quantity=total_quantity,
            )

        return redirect("shoppinglist_detail", pk=shoppinglist.pk)


class UpdateItemFromShoppingListView(LoginRequiredMixin, UpdateView):

    login_url = settings.LOGIN_URL
    model = ProductShoppingList
    context_object_name = "product_shoppinglist_product"
    form_class = ProductShoppingListForm
    template_name = "shoplist/update.html"

    def get_success_url(self):
        # Haal de shoppinglist op van het item dat is bijgewerkt
        shoppinglist = self.object.shoppinglist
        # Ga terug naar de detailpagina van deze shoppinglist
        return reverse("shoppinglist_detail", kwargs={"pk": shoppinglist.pk})


class DeleteItemFromShoppingListView(LoginRequiredMixin, DeleteView):

    login_url = settings.LOGIN_URL
    model = ProductShoppingList
    context_object_name = "product_shoppinglist_product"
    template_name = "shoplist/delete_item.html"

    def get_success_url(self):
        shoppinglist = self.object.shoppinglist
        return reverse("shoppinglist_detail", kwargs={"pk": shoppinglist.pk})


class AddItemToShoppingListView(LoginRequiredMixin, CreateView):
    login_url = settings.LOGIN_URL
    model = ProductShoppingList
    context_object_name = "product_shoppinglist_product"
    form_class = ProductShoppingListForm