# Imports from django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView, UpdateView

# Project imports
from eindwerk.settings import LOGIN_URL

from .forms import DishForm, ProductDishForm, ProductForm, ShoppingListForm, UnitForm
from .formsets import ProductDishFormSet
from .models import Dish, Product, ProductDish, ProductShoppingList, ShoppingList, Unit, UserDish, UserProduct


# TODO:: Alle templates hun styling moet nog gebeuren.


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

    # A shoppinglist will be created when visiting the endpoint.
    def get(self, request, *args, **kwargs):
        ShoppingList.objects.create(user=self.request.user)
        return redirect(reverse_lazy('shoppinglist'))

    # We are not using the form anymore, only the endpoint for this.
    # def form_valid(self, form):
    #     # Links the created objected to the user.
    #     form.instance.user = self.request.user
    #     return super().form_valid(form)


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
    """This view will show you a list of all the users dishes."""

    login_url = LOGIN_URL
    model = Dish
    template_name = "dish/list.html"

    def get_queryset(self):
        return Dish.objects.filter(userdish__user=self.request.user)


class DishCreateView(LoginRequiredMixin, CreateView):
    """This view creates a new dish object. A Dish containing multiple products.

    Relations established in this CreateView:
        - User with Product: UserProduct model.
        - User with Dish: UserDish model.
        - Product with Dish: ProductDish model.

    Forms used:
        - DishForm: For creating a new Dish object(form inherits from modelForm).
        - ProductDishFormset: For creating multiple products in the Dish creation.
    """

    login_url = LOGIN_URL
    model = Dish
    form_class = DishForm
    template_name = 'dish/create.html'
    success_url = reverse_lazy('dish_list')

    def get_context_data(self, **kwargs):
        # Need to get extra context from the View, except from the DishForm.
        data = super().get_context_data(**kwargs)
        if self.request.method == "POST":
            data['formset'] = ProductDishFormSet(self.request.POST)
        else:
            data['formset'] = ProductDishFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if formset.is_valid():
            # Object is the dish here.
            self.object = form.save()
            # print(formset)

            for formset_form in formset:
                # print(formset_form)
                # Take the product(name, is_favorite) out of the formset (added in the ProductDishForm)
                product_name = formset_form.cleaned_data.get('product_name')
                product_is_favorite = formset_form.cleaned_data.get('product_is_favorite')

                if product_name:
                    product, created = Product.objects.get_or_create(
                        name=product_name,
                        defaults={'is_favorite': product_is_favorite}
                    )

                    # Set the product for each ProductDish instance and save
                    # formsets have instances, the amount is specified in the extra parameter in the creation of the formset.
                    formset_form.instance.product = product
                    formset_form.instance.dish = self.object
                    formset_form.save()
                UserProduct.objects.get_or_create(user=self.request.user, product=product)

            # Create the UserDish instance
            UserDish.objects.create(user=self.request.user, dish=self.object)

            return redirect(reverse_lazy("dish_list"))
        else:
            raise ValidationError(formset.errors)


class UnitCreateView(LoginRequiredMixin, CreateView):
    """This view will make it possible to create a new unit."""

    login_url = LOGIN_URL
    model = Unit
    form_class = UnitForm
    template_name = "unit/create.html"
    success_url = reverse_lazy("unit_list")


class UnitListView(LoginRequiredMixin, ListView):
    """This view will show a list of ALL units."""

    login_url = LOGIN_URL
    model = Unit
    template_name = "unit/list.html"
