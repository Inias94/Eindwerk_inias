from django.http import HttpResponse
from django.contrib.auth.mixins import AccessMixin

class LoginRequired401Mixin(AccessMixin):
    """Verify that the current user is authenticated and return a 401 error if not."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse('Unauthorized', status=401)
        return super().dispatch(request, *args, **kwargs)
