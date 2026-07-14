from django.contrib import admin
from .models import Ticket

# Register your models here.

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "subject",
        "status",
        "current_level",
        "predicted_queue",
        "confidence_score",
        "created_at",
    )

    list_filter = (
        "status",
        "current_level",
    )

    search_fields = (
        "subject",
        "body",
    )