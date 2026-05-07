from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),

    # users
    path('', include('users.urls')),

    # dashboard
    path('', include('dashboard.urls')),

    # tickets 
    path('', include('tickets.urls')),
]