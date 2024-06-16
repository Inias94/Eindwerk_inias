# Django imports
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView, DeleteView

# Project imports
from django.conf import settings
from ..models import ShoppingList
from ..forms import ShoppingListForm


# This code snippet is redundant now, should be deleted after testing.
class ShoppingListCreateView(LoginRequiredMixin, CreateView):
    """This view creates a new shopping list object."""

    login_url = settings.LOGIN_URL
    model = ShoppingList
    form_class = ShoppingListForm
    template_name = "shoppinglist/create.html"
    success_url = reverse_lazy("shoppinglist")

    # A shoppinglist will be created when visiting the endpoint.
    def get(self, request, *args, **kwargs):
        ShoppingList.objects.create(user=self.request.user)
        return redirect(reverse("shoppinglist"))


class ShoppingListListView(LoginRequiredMixin, ListView):
    """This view will show you a list of all the users shopping lists."""

    login_url = settings.LOGIN_URL
    model = ShoppingList
    template_name = "shoppinglist/list.html"

    def get_queryset(self):
        return ShoppingList.objects.filter(user=self.request.user)


class ShoppingListDeleteView(LoginRequiredMixin, DeleteView):

    login_url = settings.LOGIN_URL
    model = ShoppingList
    template_name = "shoppinglist/delete.html"
    success_url = reverse_lazy("shoppinglist")

    def get_queryset(self):
        return ShoppingList.objects.filter(user=self.request.user)
