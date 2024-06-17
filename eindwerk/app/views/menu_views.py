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


class MenuUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        menu = get_object_or_404(MenuList, pk=pk)
        form = MenuForm(instance=menu)
        formset = DishMenuFormSet(queryset=DishMenu.objects.filter(menu=menu))

        context = {
            "form": form,
            "formset": formset,
        }
        return render(request, "menu/update.html", context)

    def post(self, request, pk):
        menu = get_object_or_404(MenuList, pk=pk)
        form = MenuForm(request.POST, instance=menu)
        formset = DishMenuFormSet(
            request.POST, queryset=DishMenu.objects.filter(menu=menu)
        )
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()

            # Handle deletion of forms marked for deletion
            for form in formset.deleted_forms:
                if form.instance.pk:
                    form.instance.delete()

            return redirect("menu_list")


class MenuDeleteView(LoginRequiredMixin, DeleteView):

    login_url = settings.LOGIN_URL
    model = MenuList
    success_url = reverse_lazy("menu_list")
    template_name = "menu/delete.html"

    def get_queryset(self, **kwargs):
        return MenuList.objects.filter(usermenu__user=self.request.user)


class MenuDetailView(LoginRequiredMixin, DetailView):

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
    def post(self, request, *args, **kwargs):
        dish_id = request.POST.get("dish_id")
        menu_id = request.POST.get("menu_id")

        dish = get_object_or_404(Dish, pk=dish_id, userdish__user=self.request.user)
        menu = get_object_or_404(MenuList, pk=menu_id, usermenu__user=self.request.user)

        DishMenu.objects.create(menu=menu, dish=dish)
        return redirect("dish_list")


class RemoveFromMenuView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        dish_id = request.POST.get("dish_id")
        menu_id = request.POST.get("menu_id")
        dish = get_object_or_404(Dish, pk=dish_id)
        menu = get_object_or_404(MenuList, pk=menu_id)
        DishMenu.objects.filter(menu=menu, dish=dish).delete()
