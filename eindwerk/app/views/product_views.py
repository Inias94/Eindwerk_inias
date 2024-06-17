# Django imports
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

# Project imports
from ..models import Product
from django.conf import settings

# This code is currently not used.
class ProductListView(LoginRequiredMixin, ListView):
    """This view will show you a list of all the users products."""

    login_url = settings.LOGIN_URL
    model = Product
    template_name = "shoppinglist/list.html"

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)
