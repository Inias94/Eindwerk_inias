from django.conf import settings
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView

from .forms import ProductForm, AddProductToShoppingListForm
from .models import Dish, Product, ProductInShoppingList, ShoppingList


# ---- Auth0 code block START ---- #
@login_required
def logout(request):
    """View function to handle user logout.
    This function logs out the user using Django's built-in logout function.
    It then redirects the user to the Auth0 logout page.
    Args:
        request: The HTTP request object.
    Returns:
        A redirect response to the Auth0 logout page.
    """
    # Log out the user using Django's logout function
    django_logout(request)
    # Get the Auth0 domain and client ID from the settings
    domain = settings.SOCIAL_AUTH_AUTH0_DOMAIN
    client_id = settings.SOCIAL_AUTH_AUTH0_KEY
    # Set the return URL to the current domain
    return_to = "http://127.0.0.1:8000"  # this can be current domain
    # Redirect the user to the Auth0 logout page with the client ID and return URL
    return redirect(
        f"https://{domain}/v2/logout?client_id={client_id}&returnTo={return_to}"
    )


# ---- Auth0 code block END ---- #

# ---- Homepage START ---- #


class IndexView(TemplateView):
    """View class to display the index page of the shop.

    This view inherits from Django's TemplateView, which renders a given template.
    """
    template_name = "shop_app/index.html"


# ---- Homepage END ---- #

# ---- Products database code block START ---- #


class ProductListView(ListView):
    """View class to display a list of products.

    This view inherits from Django's ListView, which automatically
    retrieves a list of objects (in this case, products) from the database
    and renders them using a specified template.
    """
    template_name = "shop_app/product/product_list.html"
    model = Product


# class AddProductView(CreateView):
#     """View class to add a new product.

#     This view inherits from Django's CreateView, which allows
#     users to create new objects (in this case, products) in the database.
#     """

#     template_name = "shop_app/product/product_add.html"
#     model = Product
#     form_class = ProductForm
#     success_url = reverse_lazy('shop_app:product-list')
    


# def create_product(request):
#     """View function to handle creation of a new product. It can handle multiple product creations in a single request.

#     This function handles both GET and POST requests.
#     On a GET request, it renders the product form.
#     On a POST request, it validates the form data and saves the product if valid.
#     """

#     if request.method == "POST":
#         form = ProductForm(request.POST or None)

#         # Check if the form is valid
#         if form.is_valid():
#             # Save the form data to create a new product
#             product = form.save()
#             # Prepare the context for rendering the product partial template
#             context = {'product': product}
#             # Render the product partial template with the context
#             return render(request, 'shop_app/product/partial/product.html', context)

#     # If the request method is not POST or the form is not valid, render the product form template
#     return render(request, 'shop_app/product/partial/product_form.html', {'form': ProductForm})

class AddProductView(CreateView):
    """View class to add a new product."""

    template_name = "shop_app/product/product_add.html"  # Assuming you have a form template
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('shop_app:product-list')

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        # Prepare the context for rendering the product partial template
        context = {'product': self.object}
        # Return the response, rendering the product partial template with the context
        return render(self.request, 'shop_app/product/partial/product.html', context)

# ---- Products database code block END ---- #

# ---- Products ShoppingList code block start ---- #

class ProductInShoppingListView(ListView):
    """View class to display a list of products in a shopping list."""
    template_name = "shop_app/product_shoppinglist/product_shoppinglist_list.html"
    model = ProductInShoppingList

class AddProductToShoppingListView(CreateView):
    """View class to add a product to a shopping list and to the the general database."""
    
    template_name = 'shop_app/product_shoppinglist/product_shoppinglist_add.html'
    model = ProductInShoppingList
    form_class = AddProductToShoppingListForm
    success_url = reverse_lazy('shop_app:shopping-list')
    


# ---- Products ShopppingList code block END ---- #

# ---- Dish views START ---- #


# ---- Dish views END ---- #
