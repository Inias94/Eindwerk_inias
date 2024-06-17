# Django imports
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

# Project imports
from django.conf import settings
from ..forms import BugReportForm
from ..models import BugReport


class BugReportCreateView(LoginRequiredMixin, CreateView):

    login_url = settings.LOGIN_URL
    Model = BugReport
    form_class = BugReportForm
    template_name = "bug/create.html"
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)