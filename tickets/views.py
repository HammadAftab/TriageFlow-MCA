from django.shortcuts import render, redirect
from .models import Ticket
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def create_ticket(request):
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']

        Ticket.objects.create(
            title=title,
            description=description,
            created_by=request.user
        )

        return redirect('dashboard')

    return render(request, 'create_ticket.html')


def my_tickets(request):
    tickets = Ticket.objects.filter(created_by=request.user).order_by('-created_at')
    return render(request, 'my_tickets.html', {'my_tickets': tickets})