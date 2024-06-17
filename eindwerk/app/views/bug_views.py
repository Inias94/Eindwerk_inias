# Django imports
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

# Project imports
from django.conf import settings
from ..forms import BugReportForm
from ..models import BugReport


class BugReportCreateView(LoginRequiredMixin, CreateView):
    """
    This view allows users to create bug reports. Only the admin can review these reports.
     Superusers must log in to the admin panel to access this functionality.

    Relations:
        - User and BugReport: The BugReport model is associated with the User model.

    Forms:
        - BugReportForm: This form is used to create a new BugReport object. It inherits from ModelForm.

    Overridden functions:
        - form_valid(): This function is overridden to assign the current user to the form.
    """

    login_url = settings.LOGIN_URL
    Model = BugReport
    form_class = BugReportForm
    template_name = "bug/create.html"
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)