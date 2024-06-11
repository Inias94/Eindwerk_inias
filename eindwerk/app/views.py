# Imports from django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
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
    login_url = LOGIN_URL
    model = Dish
    template_name = 'dish/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        # Get the current user.
        user = self.request.user
        # Query all dishes belonging to the user
        dishes = Dish.objects.filter(userdish__user=user)

        dish_products = {
            dish: ProductDish.objects.filter(dish=dish).select_related('product', 'unit') for dish in dishes
        }
        print(dish_products)
        context['dish_products'] = dish_products
        # print("Dish Products:", dish_products)
        return context


class DishCreateView(LoginRequiredMixin, CreateView):
    model = Dish
    template_name = 'dish/create.html'
    success_url = reverse_lazy("dish_list")
    form_class = DishForm

    def get_context_data(self, **kwargs):
        data = super().get_context_data()
        if self.request.method == "POST":
            data['product_form'] = ProductForm(self.request.POST)
            data['product_dish_form'] = ProductDishForm(self.request.POST)
        else:
            data['product_form'] = ProductForm()
            data['product_dish_form'] = ProductDishForm()
        return data

    def form_valid(self, form):
        response = super().form_valid(form)
        dish = self.object
        context = self.get_context_data()
        product_form = context['product_form']
        product_dish_form = context['product_dish_form']

        if all([form.is_valid(), product_form.is_valid(), product_dish_form.is_valid()]):
            product = product_form.save()

            product_dish = product_dish_form.save(commit=False)
            product_dish.product = product
            product_dish.dish = dish
            product_dish.save()

        return response




# class DishCreateView(LoginRequiredMixin, CreateView):
#     """This view creates a new dish object. A Dish containing multiple products.
#
#     Relations established in this CreateView:
#         - User with Product: UserProduct model.
#         - User with Dish: UserDish model.
#         - Product with Dish: ProductDish model.
#
#     Forms used:
#         - DishForm: For creating a new Dish object(form inherits from modelForm).
#         - ProductDishFormset: For creating multiple products in the Dish creation.
#     """
#
#     login_url = LOGIN_URL
#     model = Dish
#     form_class = DishForm
#     template_name = 'dish/create.html'
#     success_url = reverse_lazy('dish_list')
#
#     def get_context_data(self, **kwargs):
#         # Need to get extra context from the View, except from the DishForm.
#         data = super().get_context_data(**kwargs)
#         if self.request.method == "POST":
#             data['formset'] = ProductDishFormSet(self.request.POST)
#         else:
#             data['formset'] = ProductDishFormSet()
#         return data
#
#     def form_valid(self, form):
#         context = self.get_context_data()
#         formset = context['formset']
#
#         if formset.is_valid():
#             # Object is the dish here.
#             self.object = form.save()
#             # print(formset)
#
#             for formset_form in formset:
#                 # print(formset_form)
#                 # Take the product(name, is_favorite) out of the formset (added in the ProductDishForm)
#                 product_name = formset_form.cleaned_data.get('product_name')
#                 product_is_favorite = formset_form.cleaned_data.get('product_is_favorite')
#
#                 if product_name:
#                     product, created = Product.objects.get_or_create(
#                         name=product_name,
#                         defaults={'is_favorite': product_is_favorite}
#                     )
#
#                     # Set the product for each ProductDish instance and save
#                     # formsets have instances, the amount is specified in the extra parameter in the creation of the formset.
#                     formset_form.instance.product = product
#                     formset_form.instance.dish = self.object
#                     formset_form.save()
#                     ProductDish.objects.create(dish=self.object, product=product)
#                 UserProduct.objects.get_or_create(user=self.request.user, product=product)
#
#             # Create the UserDish instance
#             UserDish.objects.create(user=self.request.user, dish=self.object)
#
#         return redirect(reverse_lazy("dish_list"))


class DishUpdateView(LoginRequiredMixin, UpdateView):
    """This view updates an existing dish object and its related products.

    Relations managed in this UpdateView:
        - User with Product: UserProduct model.
        - User with Dish: UserDish model.
        - Product with Dish: ProductDish model.

    Forms used:
        - DishForm: For updating an existing Dish object.
        - ProductDishFormset: For updating multiple products in the Dish update.
    """

    login_url = LOGIN_URL
    model = Dish
    form_class = DishForm
    template_name = 'dish/update.html'
    success_url = reverse_lazy('dish_list')

    def get_initial(self):
        initial = super().get_initial()
        dish = self.get_object()
        initial['name'] = dish.name
        initial['recipe'] = dish.recipe
        initial['is_favorite'] = dish.is_favorite

        # Pre-fill product details in the formset
        product_initial = []
        for product_dish in dish.productdish_set.all():
            product_initial.append({
                'product_name': product_dish.product.name,
                'product_is_favorite': product_dish.product.is_favorite,
                'quantity': product_dish.quantity,
                'unit': product_dish.unit,
            })
        initial['product_dish_formset'] = product_initial
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = ProductDishFormSet(self.request.POST)
        else:
            context['formset'] = ProductDishFormSet(initial=self.get_initial().get('product_dish_formset', []))
        return context

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
                    ProductDish.objects.create(dish=self.object, product=product)
                UserProduct.objects.get_or_create(user=self.request.user, product=product)

            # Create the UserDish instance
            UserDish.objects.create(user=self.request.user, dish=self.object)

        return redirect(reverse_lazy("dish_list"))


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
