# Django imports
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from django.urls import reverse
from django.shortcuts import redirect

# Project imports
from django.conf import settings
from ..models import MenuList, UserMenu, DishMenu
from ..forms import MenuForm
from ..formsets import DishMenuFormSet


class MenuListView(LoginRequiredMixin, ListView):
    """This view lists your items in your menu."""

    login_url = settings.LOGIN_URL
    model = MenuList
    template_name = "menu/list.html"


class MenuCreateView(CreateView):
    model = MenuList
    form_class = MenuForm
    template_name = "menu/create.html"
    success_url = reverse_lazy("menu_list")

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.method == "POST":
            data["dishes_formset"] = DishMenuFormSet(self.request.POST)
        else:
            data["dishes_formset"] = DishMenuFormSet(queryset=DishMenu.objects.none())

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        user = self.request.user
        dishes_formset = context["dishes_formset"]

        if all([form.is_valid(), dishes_formset.is_valid()]):
            self.object = form.save()

            for dish_form in dishes_formset:
                if dish_form.cleaned_data and not dish_form.cleaned_data.get("DELETE"):
                    DishMenu.objects.create(
                        menu=self.object, dish=dish_form.cleaned_data["dish"]
                    )
            UserMenu.objects.create(user=user, menu=self.object)

            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


class MenuUpdateView(LoginRequiredMixin, UpdateView):

    login_url = settings.LOGIN_URL
    model = MenuList
    form_class = MenuForm
    template_name = "menu/create.html"
    success_url = reverse_lazy("menu_list")

    def get_context_data(self, **kwargs):
        data = super().get_context_data()
        if self.request.method == "POST":
            data["dishes_formset"] = DishMenuFormSet(self.request.POST)
        else:
            data["dishes_formset"] = DishMenuFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        user = self.request.user
        dishes_formset = context["dishes_formset"]

        if all([form.is_valid(), dishes_formset.is_valid()]):
            self.object = form.save()

            for dish_form in dishes_formset:
                DishMenu.objects.update_or_create(
                    menu=self.object, dish=dish_form.cleaned_data["dish"]
                )
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))
