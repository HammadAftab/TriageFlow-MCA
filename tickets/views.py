from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Ticket
from users.models import Employee


@login_required
def my_tickets(request):

    tickets = Ticket.objects.filter(
        created_by=request.user
    ).order_by("-created_at")

    return render(
        request,
        "my_tickets.html",
        {
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
            query=body
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
    if not ticket.classification:

        ticket.classification = "Technical Issue"

        ticket.suggested_resolution = (
            "1. Verify credentials\n"
            "2. Restart service\n"
            "3. Clear cache\n"
            "4. Retry"
        )

        ticket.confidence_score = 0.42


        if ticket.confidence_score < 0.50:

            ticket.escalation_reason = (
                "Low confidence detected. "
                "Escalation to higher support level is recommended."
            )

        else:

            ticket.escalation_reason = ""

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

        elif action == "escalate":
            if ticket.ticket_level == "L1":
                ticket.ticket_level = "L2"
            elif ticket.ticket_level == "L2":
                ticket.ticket_level = "L3"

            ticket.status = "Open"
            ticket.save()
            messages.success(request, f"Ticket escalated to {ticket.ticket_level} successfully.")
            return redirect("dashboard")

    return render(request, "ticket_detail.html", {
            "ticket": ticket,
            "is_employee": is_employee
        })