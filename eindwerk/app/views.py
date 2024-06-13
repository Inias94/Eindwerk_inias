# Imports from django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError, PermissionDenied
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView, UpdateView, DetailView, detail, DeleteView

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


# TODO: De view hieronder moet zijn functionaliteit nog krijgen.
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


class ProductDishUpdateView(LoginRequiredMixin, UpdateView):
    login_url = LOGIN_URL
    model = ProductDish
    form_class = ProductDishForm
    template_name = 'product_dish/update.html'

    def get_queryset(self):
        # We need to make sure that the user can only edit hos own objects.
        queryset = super().get_queryset()
        return queryset.filter(dish__userdish__user=self.request.user)

    def get_initial(self):
        # Add product_name and product_is_favorite to initial values.
        initial = super().get_initial()
        product_dish = self.get_object()
        initial['product_name'] = product_dish.product.name
        initial['product_is_favorite'] = product_dish.product.is_favorite
        return initial

    def form_valid(self, form):
        product_name = form.cleaned_data.get('product_name')
        product_is_favorite = form.cleaned_data.get('product_is_favorite')

        product, created = Product.objects.get_or_create(
            name=product_name,
            defaults={'is_favorite': product_is_favorite}
        )

        if not created:
            # Update product if it already exists.
            product.is_favorite = product_is_favorite
            product.save()

        form.instance.product = product
        return super().form_valid(form)

    def get_success_url(self):
        # After saving go back to the detailview of the dish.
        return reverse_lazy('dish_detail', kwargs={'pk': self.object.dish.pk})


class ProductDishDeleteView(LoginRequiredMixin, DeleteView):
    login_url = LOGIN_URL
    model = ProductDish
    template_name = 'product_dish/delete.html'
    success_url = reverse_lazy('dish_list')


class DishListView(LoginRequiredMixin, ListView):
    """This view will show you a list of all the users dishes. Including the recipe and the products in it."""

    login_url = LOGIN_URL
    model = Dish
    template_name = "dish/list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        # Get the current user.
        user = self.request.user
        # Query all dishes belonging to the current user.
        dishes = Dish.objects.filter(userdish__user=user)
        context = super().get_context_data(object_list=object_list, **kwargs)

        # Create a dictionary to store dishes and their associated products.
        dish_products = {}
        for dish in dishes:
            # Query all products associated with the current dish.
            products = ProductDish.objects.filter(dish=dish).select_related('product', 'unit')
            dish_products[dish] = products

        # Add the dish-products dictionary and the current user to the context.
        context['dish_products'] = dish_products
        return context


class DishDetailView(LoginRequiredMixin, DetailView):
    """This view makes it possible to look to a dish in detail.
    It will only show dishes that are related to the user."""

    login_url = LOGIN_URL
    model = Dish
    template_name = 'dish/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        # Get the current user.
        user = self.request.user
        # Query the dish for the user
        dishes = Dish.objects.filter(pk=self.kwargs['pk'])

        dish_products = {}
        for dish in dishes:
            dish_products[dish] = ProductDish.objects.filter(dish=dish).select_related('product', 'unit')
        print(dish_products)
        context['dish_products'] = dish_products
        # print("Dish Products:", dish_products)
        return context

    def get_object(self, queryset=None):
        # Get the current user.
        user = self.request.user
        # Get the dish object.
        obj = super().get_object(queryset=queryset)
        # Check if the dish belongs to the current user.
        if not Dish.objects.filter(id=obj.id, userdish__user=user).exists():
            raise PermissionDenied
        return obj


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

    model = Dish
    form_class = DishForm
    template_name = 'dish/create.html'
    success_url = reverse_lazy('dish_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request == "POST":
            data['productdish_formset'] = ProductDishFormSet(self.request.POST)
        else:
            data['productdish_formset'] = ProductDishFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        user = self.request.user
        productdish_formset = context['productdish_formset']
        if form.is_valid() and productdish_formset.is_valid():
            self.object = form.save()

            # Save the Dish first
            dish = form.save()

            # Iterate over the productdish_formset and save each ProductDish object
            for productdish_form in productdish_formset:

                # These fields are manually added to the ProductDishForm, therefor we have to extract the data out of the form fields.
                product_name = productdish_form.cleaned_data.get('product_name')
                product_is_favorite = productdish_form.cleaned_data.get('product_is_favorite')

                # Create or get the Product with the data from above.
                product, created = Product.objects.get_or_create(
                    name=product_name,
                    defaults={'is_favorite': product_is_favorite}
                )

                # Create the ProductDish object
                ProductDish.objects.create(
                    dish=dish,
                    product=product,
                    quantity=productdish_form.cleaned_data.get('quantity'),
                    unit=productdish_form.cleaned_data.get('unit')
                )
                # Create the UserProduct object
                UserProduct.objects.create(user=user, product=product)
            # Create the UserDish object for establishing the relation between the user and the dish.
            UserDish.objects.create(user=user, dish=dish)

            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form)


class DishUpdateView(LoginRequiredMixin, UpdateView):
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
    template_name = 'dish/update.html'
    success_url = reverse_lazy('dish_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['productdish_formset'] = ProductDishFormSet(self.request.POST, instance=self.object)
        else:
            data['productdish_formset'] = ProductDishFormSet(instance=self.object)
            for form in data['productdish_formset']:
                product_dish = form.instance
                product = product_dish.product
                form.fields['product_name'].initial = product.name
                form.fields['product_is_favorite'].initial = product.is_favorite
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        user = self.request.user
        productdish_formset = context['productdish_formset']
        if form.is_valid() and productdish_formset.is_valid():
            self.object = form.save()
            dish = form.save()

            for productdish_form in productdish_formset:
                if productdish_form.cleaned_data.get('DELETE'):
                    productdish_form.instance.delete()
                    continue

                product_name = productdish_form.cleaned_data.get('product_name')
                product_is_favorite = productdish_form.cleaned_data.get('product_is_favorite')
                quantity = productdish_form.cleaned_data.get('quantity')
                unit = productdish_form.cleaned_data.get('unit')

                product, created = Product.objects.get_or_create(
                    name=product_name,
                    defaults={'is_favorite': product_is_favorite}
                )

                ProductDish.objects.update_or_create(
                    id=productdish_form.instance.id,
                    defaults={'dish': dish, 'product': product, 'quantity': quantity, 'unit': unit}
                )

                UserProduct.objects.update_or_create(user=user, product=product)

            UserDish.objects.update_or_create(user=user, dish=dish)

            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form)


class DishDeleteView(LoginRequiredMixin, DeleteView):
    login_url = LOGIN_URL
    model = Dish
    success_url = reverse_lazy('dish_list')


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
