from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect


# Homepage redirect
def home_redirect(request):
    return redirect('login')

urlpatterns = [
    path('', home_redirect),  
    path('admin/', admin.site.urls),

    # users
    path('', include('users.urls')),

    # dashboard
    path('', include('dashboard.urls')),

    # tickets
    path('', include('tickets.urls')),
]