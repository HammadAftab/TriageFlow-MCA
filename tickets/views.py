from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from .models import Ticket
from users.models import Employee


@login_required
def my_tickets(request):

    tickets = Ticket.objects.filter(created_by=request.user).order_by("-created_at")

    return render(request, "my_tickets.html", {
            "my_tickets": tickets
        }
    )

@login_required
def raise_ticket(request):
    if request.method == "POST":
        subject = request.POST.get("subject", "")
        body = request.POST.get("body", "")
        Ticket.objects.create(
            created_by=request.user,
            subject=subject,
            body=body
        )
        return redirect("dashboard")
    return render(request, "raise_ticket.html")


@login_required
def ticket_detail(request, ticket_id):

    ticket = get_object_or_404(
        Ticket,
        id=ticket_id
    )

    # Temporary AI simulation
    if not ticket.predicted_queue:

        ticket.predicted_queue = "Technical Issue"

        ticket.resolution = (
            "1. Verify credentials\n"
            "2. Restart service\n"
            "3. Clear cache\n"
            "4. Retry"
        )

        ticket.confidence_score = 0.42

        ticket.save()

    is_employee = False

    try:
        employee = Employee.objects.get(user=request.user)
        is_employee = True
    except Employee.DoesNotExist:
        employee = None
        return redirect("dashboard")

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "resolve":
            ticket.status = "Closed"
            ticket.resolved_by = employee.employee_id
            ticket.resolved_at = timezone.now()
            
        elif action == "escalate":
            if ticket.current_level == "L1":
                ticket.current_level = "L2"
            elif ticket.current_level == "L2":
                ticket.current_level = "L3"

            ticket.status = "Open"
            ticket.save()
            messages.success(request, f"Ticket escalated to {ticket.current_level} successfully.")
            return redirect("dashboard")

    return render(request, "ticket_detail.html", {
            "ticket": ticket,
            "is_employee": is_employee
    })