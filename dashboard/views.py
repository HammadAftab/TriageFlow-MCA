from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from tickets.models import Ticket
from users.models import Employee


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

    # Check whether logged-in account is employee
    try:
        employee = Employee.objects.get(user=request.user)

        # Employee Dashboard
        if employee.position == 'L1':
            tickets = Ticket.objects.all().order_by('-created_at')

        else:
            tickets = []

        return render(request, 'dashboard.html', {
            'all_tickets': tickets,
            'is_employee': True,
            'position': employee.position
        })

    except Employee.DoesNotExist:

        # Normal User Dashboard
        user_tickets = Ticket.objects.filter(
            created_by=request.user
        ).order_by('-created_at')

        return render(request, 'dashboard.html', {
            'all_tickets': user_tickets,
            'is_employee': False
        })