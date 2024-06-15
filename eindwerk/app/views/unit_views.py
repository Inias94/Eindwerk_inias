# Django imports
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView


# Project imports
from eindwerk.eindwerk.settings import LOGIN_URL
from ..models import Unit
from ..forms import UnitForm


class UnitCreateView(LoginRequiredMixin, CreateView):
    """This view will make it possible to create a new unit."""

    login_url = LOGIN_URL
    model = Unit
    form_class = UnitForm
    template_name = "unit/create.html"
    success_url = reverse_lazy("unit_create")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["unit_list"] = Unit.objects.all()
        return context


class UnitListView(LoginRequiredMixin, ListView):
    """This view will show a list of ALL units."""

    login_url = LOGIN_URL
    model = Unit
    template_name = "unit/list.html"


class UnitUpdateView(LoginRequiredMixin, UpdateView):
    """This view is to make it possible to adjust a Unit model."""

    login_url = LOGIN_URL
    model = Unit
    form_class = UnitForm
    template_name = "unit/update.html"
    success_url = reverse_lazy("unit_list")


class UnitDeleteView(LoginRequiredMixin, DeleteView):
    """This view makes it possible to delete a Unit model."""

    login_url = LOGIN_URL
    model = Unit
    template_name = "unit/delete.html"
    success_url = reverse_lazy("unit_list")
