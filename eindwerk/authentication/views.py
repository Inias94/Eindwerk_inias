from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from eindwerk.settings import SOCIAL_AUTH_AUTH0_DOMAIN, SOCIAL_AUTH_AUTH0_KEY


# Auth0 view. This is the only one required. The rest is handled in the settings file of shopMyDish.
@login_required
def logout(request):
    """View function to handle user logout.
    This function logs out the user using Django's built-in logout function.
    It then redirects the user to the Auth0 logout page."""

    # Log out the user using Django's logout function
    django_logout(request)
    # Get the Auth0 domain and client ID from the settings
    domain = SOCIAL_AUTH_AUTH0_DOMAIN
    client_id = SOCIAL_AUTH_AUTH0_KEY
    # Set the return URL to the current domain
    return_to = "http://127.0.0.1:8000"  # this can be current domain
    # Redirect the user to the Auth0 logout page with the client ID and return URL
    return redirect(
        f"https://{domain}/v2/logout?client_id={client_id}&returnTo={return_to}"
    )
