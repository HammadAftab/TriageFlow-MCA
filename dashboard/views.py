from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from tickets.models import Ticket
from users.models import Employee


@login_required
def dashboard_view(request):

    if request.method == 'POST':
        body = request.POST.get('body')

        if body:
            Ticket.objects.create(
                created_by=request.user,
                body=body
            )

        return redirect('dashboard')

    # Check whether logged-in account is employee
    try:
        employee = Employee.objects.get(user=request.user)

        # Employee Dashboard
        tickets = Ticket.objects.filter(
            current_level=employee.position,
            status='Open'
        ).order_by('-created_at')

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