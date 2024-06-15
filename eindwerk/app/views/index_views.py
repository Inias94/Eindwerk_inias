# Django imports
from django.views.generic import TemplateView


class IndexView(TemplateView):
    """This view renders the homepage."""

    template_name = "index.html"
