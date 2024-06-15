from django.core.exceptions import PermissionDenied
from .models import UserDish, Dish, UserProduct


class UserDishAccessMixin:
    """This mixins checks if the dish/products in dish are from the user.
    If not manipulation of the objects is declined."""

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        user = self.request.user
        if isinstance(obj, Dish):
            if not UserDish.objects.filter(user=user, dish=obj).exists():
                raise PermissionDenied
        else:
            if not UserDish.objects.filter(user=user, dish=obj.dish).exists():
                raise PermissionDenied
        return obj


class UserProductAccessMixin:

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        user = self.request.user
        if not UserProduct.objects.filter(user=user, product=obj).exists():
            raise PermissionDenied
        return obj
