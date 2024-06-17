# Django imports
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy

# Project imports

from django.conf import settings
from ..models import Dish, ProductDish, Product, UserDish, UserProduct, MenuList
from ..custom_mixins import UserDishAccessMixin
from ..forms import DishForm
from ..formsets import ProductDishFormSet


class DishListView(LoginRequiredMixin, ListView):
    """
    This view displays a list of all the user's dishes along with their corresponding recipes and products.

    The view requires the user to be logged in. Only the dishes belonging to the current user are displayed.

    The context data for the view includes:
        - dish_products: A dictionary mapping each dish to its associated products.
        - menus: A queryset of all menus belonging to the current user.
        - user: The current user.
    """

    login_url = settings.LOGIN_URL
    model = Dish
    template_name = "dish/list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        """Here we are making sure the view knows about the extra context variables. to be handeld in the view."""

        user = self.request.user
        # Query all dishes belonging to the current user.
        dishes = Dish.objects.filter(userdish__user=user)
        # Get the context data from the parent view.
        context = super().get_context_data(object_list=object_list, **kwargs)

        # Create a dictionary to store dishes and their associated products.
        dish_products = {}
        for dish in dishes:
            # Query all products associated with the current dish.
            products = ProductDish.objects.filter(dish=dish).select_related(
                "product", "unit"
            )
            dish_products[dish] = products

        # Query all menus belonging to the current user.
        menus = MenuList.objects.filter(usermenu__user=user)

        # Add the dish-products dictionary, the current user, and the user's menus to the context.
        context["dish_products"] = dish_products
        context["menus"] = menus
        context["user"] = user
        return context


class DishDetailView(LoginRequiredMixin, UserDishAccessMixin, DetailView):
    """This view makes it possible to look to a dish in detail.
    It will only show dishes that are related to the user."""

    login_url = settings.LOGIN_URL
    model = Dish
    template_name = "dish/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        # Get the current dish.
        dish = self.get_object()

        # Get the related product dishes.
        dish_products = ProductDish.objects.filter(dish=dish).select_related(
            "product", "unit"
        )
        context["dish_products"] = dish_products
        return context


class DishCreateView(LoginRequiredMixin, UserDishAccessMixin, CreateView):
    """This view creates a new dish object. A Dish containing multiple products.

    Relations established in this CreateView:
        - User with Product: UserProduct model.
        - User with Dish: UserDish model.
        - Product with Dish: ProductDish model.

    Forms used:
        - DishForm: For creating a new Dish object(form inherits from modelForm).
        - ProductDishFormset: For creating multiple products in the Dish creation.
    """

    model = Dish
    form_class = DishForm
    template_name = "dish/create.html"
    success_url = reverse_lazy("dish_list")

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.method == "POST":
            data["productdish_formset"] = ProductDishFormSet(self.request.POST)
        else:
            data["productdish_formset"] = ProductDishFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        user = self.request.user
        productdish_formset = context["productdish_formset"]
        if form.is_valid() and productdish_formset.is_valid():
            self.object = form.save()

            # Save the Dish first
            dish = form.save()

            # Iterate over the productdish_formset and save each ProductDish object
            for productdish_form in productdish_formset:
                # These fields are manually added to the ProductDishForm, therefore we have to extract the data out of the form fields.
                product_name = productdish_form.cleaned_data.get("product_name")
                product_is_favorite = productdish_form.cleaned_data.get(
                    "product_is_favorite"
                )

                # Create or get the Product with the data from above.
                product, created = Product.objects.get_or_create(
                    name=product_name, defaults={"is_favorite": product_is_favorite}
                )

                # Create the ProductDish object
                ProductDish.objects.get_or_create(
                    dish=dish,
                    product=product,
                    quantity=productdish_form.cleaned_data.get("quantity"),
                    unit=productdish_form.cleaned_data.get("unit"),
                )
                # Create the UserProduct object
                UserProduct.objects.get_or_create(user=user, product=product)
            # Create the UserDish object for establishing the relation between the user and the dish.
            UserDish.objects.get_or_create(user=user, dish=dish)

            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form)


class DishUpdateView(LoginRequiredMixin, UserDishAccessMixin, UpdateView):
    """This view updates an existing dish object. A Dish containing multiple products.

    Relations established in this UpdateView:
        - User with Product: UserProduct model.
        - User with Dish: UserDish model.
        - Product with Dish: ProductDish model.

    Forms used:
        - DishForm: For updating a Dish object (form inherits from modelForm).
        - ProductDishFormset: For managing multiple products in the Dish update.
    """

    model = Dish
    form_class = DishForm
    template_name = "dish/update.html"
    success_url = reverse_lazy("dish_list")

    def get_context_data(self, **kwargs):
        """Here we are making sure the view knows about the extra context variables. to be handeld in the view.
        Because of the ProductDishForm inherits from django modelForm, we need to add 2 extra form.fields to the view.
        for the creation of the product."""

        data = super().get_context_data(**kwargs)
        if self.request.method == "POST":
            data["productdish_formset"] = ProductDishFormSet(
                self.request.POST, instance=self.object
            )
        else:
            data["productdish_formset"] = ProductDishFormSet(instance=self.object)
            for form in data["productdish_formset"]:
                product_dish = form.instance
                product = product_dish.product
                form.fields["product_name"].initial = product.name
                form.fields["product_is_favorite"].initial = product.is_favorite
        return data

    def form_valid(self, form):
        # TODO: Add a docstring with info
        context = self.get_context_data()
        user = self.request.user
        productdish_formset = context["productdish_formset"]

        if form.is_valid() and productdish_formset.is_valid():
            self.object = form.save()
            dish = form.save()

            for productdish_form in productdish_formset:
                if productdish_form.cleaned_data.get("DELETE"):
                    productdish_form.instance.delete()
                    continue

                product_name = productdish_form.cleaned_data.get("product_name")
                product_is_favorite = productdish_form.cleaned_data.get(
                    "product_is_favorite"
                )
                quantity = productdish_form.cleaned_data.get("quantity")
                unit = productdish_form.cleaned_data.get("unit")

                product, created = Product.objects.get_or_create(
                    name=product_name, defaults={"is_favorite": product_is_favorite}
                )

                ProductDish.objects.update_or_create(
                    id=productdish_form.instance.id,
                    defaults={
                        "dish": dish,
                        "product": product,
                        "quantity": quantity,
                        "unit": unit,
                    },
                )

                UserProduct.objects.get_or_create(user=user, product=product)

            UserDish.objects.get_or_create(user=user, dish=dish)

            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form)


class DishDeleteView(LoginRequiredMixin, UserDishAccessMixin, DeleteView):
    login_url = settings.LOGIN_URL
    template_name = "dish/delete.html"
    model = Dish
    success_url = reverse_lazy("dish_list")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        UserDish.objects.filter(dish=self.object).delete()
        ProductDish.objects.filter(dish=self.object).delete()
        self.object.delete()
        return redirect(self.get_success_url())
