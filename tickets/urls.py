from django.urls import path
from . import views

urlpatterns = [

path(
    'my-tickets/',
    views.my_tickets,
    name='my_tickets'
),

path(
    'ticket/<int:ticket_id>/',
    views.ticket_detail,
    name='ticket_detail'
),

]