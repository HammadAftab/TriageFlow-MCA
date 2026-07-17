from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from .models import Ticket
from users.models import Employee

from ai.scripts.classifier import predict_queue
from ai.scripts.ticket_retriever import retrieve_similar_tickets
from ai.scripts.llm_helper import generate_resolution

import statistics


@login_required
def raise_ticket(request):
    if request.method == "POST":
        subject = request.POST.get("subject", "")
        body = request.POST.get("body", "")

        predicted_queue, confidence = predict_queue(subject, body)
        
        print("=" * 50)
        print("Classifier Confidence:", confidence)
        print("=" * 50)

        Ticket.objects.create(
            created_by=request.user,
            subject=subject,
            body=body,
            predicted_queue=predicted_queue,
            classifier_confidence=confidence   
        )
        return redirect("dashboard")
    return render(request, "raise_ticket.html")


@login_required
def ticket_detail(request, ticket_id):

    ticket = get_object_or_404(Ticket, id=ticket_id)
    results = retrieve_similar_tickets(ticket.subject, ticket.body, top_k=3)

    print("=" * 50)
    print(results)
    print("=" * 50)
    
    # AI Confidence Score
    #if results:
    #    top_similarity = results[0]["similarity"]
    #    avg_similarity = sum(r["similarity"] for r in results) / len(results)
    #    confidence = (
    #        0.7 * top_similarity +
    #        0.3 * avg_similarity
    #    )
    #    ticket.confidence_score = round(confidence * 100, 1)
    #    ticket.save(update_fields=["confidence_score"])

    if results:

        similarities = [r["similarity"] for r in results]

        top_similarity = similarities[0]

        average_similarity = sum(similarities) / len(similarities)

        if len(similarities) > 1:
            std_deviation = statistics.stdev(similarities)
        else:
            std_deviation = 0

        consistency_score = max(0, 1 - std_deviation)

        retrieval_confidence = (
            0.5 * top_similarity +
            0.3 * average_similarity +
            0.2 * consistency_score
        )

        classifier_confidence = ticket.classifier_confidence


        classifier_confidence = max(
            classifier_confidence,
            retrieval_confidence * 0.85
        )

        # Weighted ensemble
        final_confidence = (
            0.35 * classifier_confidence +
            0.65 * retrieval_confidence
        )

        # Boost confidence for very strong retrieval evidence
        if retrieval_confidence >= 0.85:
            final_confidence += 0.10
        elif retrieval_confidence >= 0.75:
            final_confidence += 0.07
        elif retrieval_confidence >= 0.65:
            final_confidence += 0.05
        elif retrieval_confidence >= 0.55:
            final_confidence += 0.03

        # Keep the score within 0-98%
        final_confidence = min(final_confidence, 0.98)

        ticket.confidence_score = round(final_confidence * 100, 1)

        ticket.save(update_fields=["confidence_score"])

        print("=" * 60)
        print("Top Similarity       :", round(top_similarity, 4))
        print("Average Similarity   :", round(average_similarity, 4))
        print("Std Deviation        :", round(std_deviation, 4))
        print("Consistency Score    :", round(consistency_score, 4))
        print("Retrieval Confidence :", round(retrieval_confidence, 4))
        print("Classifier Confidence:", round(classifier_confidence, 4))
        print("Final Confidence     :", ticket.confidence_score)
        print("=" * 60)


    if ticket.created_by == request.user:
        return render(request, "customer_ticket_detail.html",
            {
                "ticket": ticket
            }
        )

    # Temporary AI simulation
#   if not ticket.predicted_queue:
#
#     ticket.predicted_queue = "Technical Support"
#
#     ticket.resolution = (
#         "1. Verify credentials\n"
#         "2. Restart service\n"
#         "3. Clear cache\n"
#         "4. Retry"
#     )
#
#     ticket.confidence_score = 0.42
#
#     ticket.save()
    


    #if not ticket.resolution:
    #    if results:
    #        ticket.resolution = generate_resolution(
    #            f"Subject: {ticket.subject}\n\nBody:\n{ticket.body}",
    #            results
    #        )
    #        ticket.save()

    
    if not ticket.resolution and results:
        ticket.resolution = generate_resolution(
        f"Subject: {ticket.subject}\n\nBody:\n{ticket.body}",
        results
        )
        ticket.save(update_fields=["resolution"])


    is_employee = False
    try:
        employee = Employee.objects.get(user=request.user)
        is_employee = True
    except Employee.DoesNotExist:
        employee = None
        return redirect("dashboard")

    if request.method == "POST":
        edited_resolution = request.POST.get("resolution", ticket.resolution)
        action = request.POST.get("action")

        if action == "resolve":
            
            ticket.resolution = edited_resolution
            ticket.resolved_by = employee.employee_id
            ticket.resolved_at = timezone.now()
            ticket.status = "Closed"
            print("=" * 50)
            print("Edited Resolution:")
            print(edited_resolution)
            print("=" * 50)
            ticket.save()

            messages.success(request, "Ticket resolved successfully.")
            return redirect("dashboard")

            
        elif action == "escalate":
            ticket.resolution = edited_resolution

            if employee.position == "L1":
                ticket.current_level = "L2"
            elif employee.position == "L2":
                ticket.current_level = "L3"
            else:
                messages.error(request, "L3 tickets cannot be escalated.")
                return redirect("ticket_detail", ticket_id=ticket.id)

            ticket.status = "Open"
            ticket.save()

            messages.success(request, f"Ticket escalated to {ticket.current_level} successfully.")

            return redirect("dashboard")


    similar_tickets = retrieve_similar_tickets(ticket.subject, ticket.body, top_k=3)

    return render(request, "ticket_detail.html", {
            "ticket": ticket,
            "employee": employee,
            "is_employee": is_employee,
            "similar_tickets": similar_tickets,
    })


@login_required
def customer_ticket_detail(request, ticket_id):

    ticket = get_object_or_404(
        Ticket,
        id=ticket_id,
        created_by=request.user
    )

    return render(
        request,
        "customer_ticket_detail.html",
        {
            "ticket": ticket
        }
    )