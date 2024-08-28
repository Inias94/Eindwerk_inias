# Django imports
from django.views.generic import TemplateView


class IndexView(TemplateView):
    """This view renders the homepage."""

    template_name = "index.html"

# In een bestand genaamd `views.py` of een andere geschikte locatie
from django.http import HttpResponse
from django.core.management import call_command

def run_migrations(request):
    call_command('migrate')
    return HttpResponse('Migrations completed successfully.')
