from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('employee-login/', views.employee_login_view, name='employee_login'),
    path('employee-signup/', views.employee_signup_view, name='employee_signup'),
]