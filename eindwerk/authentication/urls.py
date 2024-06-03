from django.urls import path

from . import views

urlpatterns = [
    # logout
    path("logout", views.logout),
]
