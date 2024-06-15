# Django imports
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import UpdateView, DeleteView

# Project imports
from django.conf import settings
from ..custom_mixins import UserDishAccessMixin
from ..models import ProductDish, Product
from ..forms import ProductDishForm


class ProductDishUpdateView(LoginRequiredMixin, UserDishAccessMixin, UpdateView):
    # TODO: DOCSTRING!
    login_url = settings.LOGIN_URL
    model = ProductDish
    form_class = ProductDishForm
    template_name = "product_dish/update.html"

    def get_queryset(self):
        # We need to make sure that the user can only edit hos own objects.
        queryset = super().get_queryset()
        return queryset.filter(dish__userdish__user=self.request.user)

    def get_initial(self):
        """Add product_name and product_is_favorite to initial values.
        Need to explicit do this because they do not inherit from the ModelForm."""

        initial = super().get_initial()
        product_dish = self.get_object()
        initial["product_name"] = product_dish.product.name
        initial["product_is_favorite"] = product_dish.product.is_favorite
        return initial

    def form_valid(self, form):
        product_name = form.cleaned_data.get("product_name")
        product_is_favorite = form.cleaned_data.get("product_is_favorite")

        product, created = Product.objects.update_or_create(
            name=product_name, defaults={"is_favorite": product_is_favorite}
        )

        if not created:
            # Update product if it already exists.
            product.is_favorite = product_is_favorite
            product.save()

        form.instance.product = product
        return super().form_valid(form)


class ProductDishDeleteView(LoginRequiredMixin, UserDishAccessMixin, DeleteView):
    login_url = settings.LOGIN_URL
    model = ProductDish
    template_name = "product_dish/delete.html"

    def get_success_url(self):
        obj = self.get_object()
        return reverse("dish_detail", kwargs={"pk": obj.dish.pk})
