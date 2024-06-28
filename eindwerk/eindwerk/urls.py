from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),

    # Main application
    path('', include('authentication.urls')),
    path('', include('app.urls')),
    # auth0
    path('', include('social_django.urls'))
]
