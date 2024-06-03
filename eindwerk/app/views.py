# Imports from django
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView, UpdateView

# Project imports
from eindwerk.settings import LOGIN_URL

from .forms import DishForm, ProductDishForm, ProductForm, ShoppingListForm, UnitForm
from .formsets import ProductDishFormSet
from .models import (
    Dish,
    Product,
    ProductDish,
    ProductShoppingList,
    ShoppingList,
    Unit,
    UserDish,
    UserProduct
)

# TODO:: Alle templates hun styling moet nog gebeuren.


def add_productform_to_create_dish(request):
    """This function is used to render partials in the create_dish view using the HTMX package."""

    form = ProductDishForm()
    form_html = render_to_string("dish/partials/product_dish_form.html", {"form": form})
    return HttpResponse(form_html)


@login_required
def create_dish(request):
    """This function creates a new dish. A product can be created if it does not exist yet.
    We are using a formset here so we can add multiple products to the dish. This makes it possible to use multiple forms.
    """

    if request.method == "POST":
        dish_form = DishForm(request.POST)
        formset = ProductDishFormSet(request.POST)
        if dish_form.is_valid() and formset.is_valid():
            dish = dish_form.save()
            formset.instance = dish
            formset.save()
            UserDish.objects.create(user=request.user, dish=dish)
            return redirect(reverse_lazy("dish_list"))
    else:
        dish_form = DishForm()
        formset = ProductDishFormSet()
    return render(
        request, "dish/create.html", {"dish_form": dish_form, "formset": formset}
    )

# class DishCreateView(LoginRequiredMixin, CreateView):
#     model = Dish
#     form_class = DishForm
#     template_name = 'dish/create.html'
#     success_url = reverse_lazy('your_success_url_name')

#     def get_context_data(self, **kwargs):
#         data = super().get_context_data(**kwargs)
#         if self.request == 'POST':
#             data['productdish_formset'] = ProductDishFormSet(self.request.POST)
#         else:
#             data['productdish_formset'] = ProductDishFormSet()
#         return data

#     def form_valid(self, form):
#         data = self.get_context_data()
#         productdish_formset = data['productdish_formset']

#         if form.is_valid() and productdish_formset.is_valid():
#             self.object = form.save()

#             # Save each product form in the formset
#             for productdish_form in productdish_formset:
#                 if productdish_form.has_changed() and productdish_form.is_valid():
#                     productdish = productdish_form.save(commit=False)
#                     productdish.dish = self.object
#                     productdish.save()

#             # Create UserDish entry
#             UserDish.objects.create(user=self.request.user, dish=self.object)

#             # Create UserProduct entries
#             for productdish_form in productdish_formset:
#                 if productdish_form.instance.pk:
#                     UserProduct.objects.get_or_create(user=self.request.user, product=productdish_form.instance.product)

#             return redirect(reverse_lazy('dish_list'))

#         return self.render_to_response(self.get_context_data(form=form))


class IndexView(TemplateView):
    """This view renders the homepage."""

    template_name = "index.html"


class ShoppingListCreateView(LoginRequiredMixin, CreateView):
    """This view creates a new shopping list object."""

    login_url = LOGIN_URL
    model = ShoppingList
    form_class = ShoppingListForm
    template_name = "shoppinglist/create.html"
    success_url = reverse_lazy("shoppinglist")

    def form_valid(self, form):
        # Links the created objected to the user.
        form.instance.user = self.request.user
        return super().form_valid(form)


class ShoppingListUpdateView(LoginRequiredMixin, UpdateView):
    """This view is to make adjustments to the items in the shopping list."""

    login_url = LOGIN_URL
    model = ShoppingList
    form_class = ShoppingListForm
    template_name = "shoppinglist/create.html"
    success_url = reverse_lazy("shoppinglist")


class ShoppingListListView(LoginRequiredMixin, ListView):
    """This view will show you a list of all the users shopping lists."""

    login_url = LOGIN_URL
    model = ShoppingList
    template_name = "shoppinglist/list.html"

    def get_queryset(self):
        return ShoppingList.objects.filter(user=self.request.user)


class ProductListView(LoginRequiredMixin, ListView):
    """This view will show you a list of all the users products."""

    login_url = LOGIN_URL
    model = Product
    template_name = "shoppinglist/list.html"

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)


class DishListView(LoginRequiredMixin, ListView):
    login_url = LOGIN_URL
    model = Dish
    template_name = "dish/list.html"


class UnitCreateView(LoginRequiredMixin, CreateView):
    """This view will make it possible to create a new unit."""

    login_url = LOGIN_URL
    model = Unit
    form_class = UnitForm
    template_name = "unit/create.html"
    success_url = reverse_lazy("unit_list")


class UnitListView(LoginRequiredMixin, ListView):
    login_url = LOGIN_URL
    model = Unit
    template_name = "unit/list.html"
