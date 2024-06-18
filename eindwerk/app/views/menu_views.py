# Django imports
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404

# Project imports
from django.conf import settings
from ..models import MenuList, UserMenu, DishMenu, Dish, ProductDish
from ..forms import MenuForm
from ..formsets import DishMenuFormSet


class MenuListView(LoginRequiredMixin, ListView):
    """This view lists your items in your menu."""

    login_url = settings.LOGIN_URL
    model = MenuList
    template_name = "menu/list.html"

    def get_queryset(self, **kwargs):
        return MenuList.objects.filter(usermenu__user=self.request.user)


class MenuCreateView(CreateView):
    """This view lets you create a new menu. Dishes can be added to this Menu model in an other View.

    Models:
        - MenuList
        - UserMenu

    Forms:
        - MenuForm
    """

    login_url = settings.LOGIN_URL
    model = MenuList
    form_class = MenuForm
    template_name = "menu/create.html"
    success_url = reverse_lazy("menu_list")

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            UserMenu.objects.get_or_create(user=self.request.user, menu=self.object)
            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form)


class MenuUpdateView(LoginRequiredMixin, UpdateView):
    """This view lets a user change his menu, onyl menu's related to the user.

    Models:
        - MenuList

    Forms:
        - MenuForm
    """

    login_url = settings.LOGIN_URL
    model = MenuList
    form_class = MenuForm
    template_name = "menu/update.html"
    success_url = reverse_lazy("menu_list")

    def get_queryset(self):
        return MenuList.objects.filter(usermenu__user=self.request.user)


class MenuDeleteView(LoginRequiredMixin, DeleteView):
    """This view lets a user delete menu's relates to him.

    Models:
        - MenuList
    """

    login_url = settings.LOGIN_URL
    model = MenuList
    success_url = reverse_lazy("menu_list")
    template_name = "menu/delete.html"

    def get_queryset(self, **kwargs):
        return MenuList.objects.filter(usermenu__user=self.request.user)


class MenuDetailView(LoginRequiredMixin, DetailView):
    """This view lets you view the detail of a menu related to the user. And dishes related to the menu.

    Added dishes to the context so a user can see whats in the menu.

    Models:
        - MenuList
        - DishMenu
    """

    login_url = settings.LOGIN_URL
    model = MenuList
    template_name = "menu/detail.html"
    context_object_name = "menu"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        menu = self.get_object()
        context["dishes"] = DishMenu.objects.filter(menu=menu)
        return context

    def get_queryset(self):
        return MenuList.objects.filter(usermenu__user=self.request.user)


class AddToMenuView(LoginRequiredMixin, View):
    """This view makes it possible to add a dish to a menu.
    We are getting the dish id and the menu id, so we can make the DishMenu object wich makes the relation between Dish and Menu.
    """

    def post(self, request, *args, **kwargs):
        dish_id = request.POST.get("dish_id")
        menu_id = request.POST.get("menu_id")

        dish = get_object_or_404(Dish, pk=dish_id)
        menu = get_object_or_404(MenuList, pk=menu_id)

        DishMenu.objects.create(menu=menu, dish=dish)
        return redirect("dish_list")


class RemoveFromMenuView(LoginRequiredMixin, View):
    """This view makes it possible to delete a dish to a menu.
    We are getting the dish id and the menu id, so we can delete the DishMenu object wich makes the relation between Dish and Menu.
    """

    def post(self, request, *args, **kwargs):
        dish_id = request.POST.get("dish_id")
        menu_id = request.POST.get("menu_id")

        dish = get_object_or_404(Dish, pk=dish_id)
        menu = get_object_or_404(MenuList, pk=menu_id)

        DishMenu.objects.filter(menu=menu, dish=dish).delete()
        return redirect("dish_list")
