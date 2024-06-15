# Django imports
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

# Project imports
from eindwerk.eindwerk.settings import LOGIN_URL
from ..models import MenuList
from ..forms import MenuForm


class MenuListView(LoginRequiredMixin, CreateView):
    """This view lists your items in your menu."""

    login_url = LOGIN_URL
    model = MenuList
    template_name = "menu/list.html"


class MenuCreateView(LoginRequiredMixin, CreateView):
    """This view will let you add dishes to your menu."""

    login_url = LOGIN_URL
    model = MenuList
    form_class = MenuForm
    template_name = "menu/create.html"
    success_url = reverse_lazy("menu_list")

    def get_queryset(self):
        return MenuList.objects.filter(user=self.request.user)
