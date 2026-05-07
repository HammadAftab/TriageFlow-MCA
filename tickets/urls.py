from django.urls import path
from . import views

urlpatterns = [
    path('my-tickets/', views.my_tickets, name='my_tickets'),
]