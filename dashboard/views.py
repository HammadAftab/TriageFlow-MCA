from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from tickets.models import Ticket


@login_required
def dashboard_view(request):

    if request.method == 'POST':
        query = request.POST.get('query')

        if query:
            Ticket.objects.create(
                created_by=request.user,
                query=query
            )

        return redirect('dashboard')

    all_tickets = Ticket.objects.all().order_by('-created_at')

    return render(request, 'dashboard.html', {
        'all_tickets': all_tickets
    })