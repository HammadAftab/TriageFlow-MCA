from django.db import models
from django.conf import settings


class Ticket(models.Model):

    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Pending', 'Pending'),
        ('Closed', 'Closed')
    ]

    LEVEL_CHOICES = [
        ('L1', 'L1'),
        ('L2', 'L2'),
        ('L3', 'L3'),
    ]

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_tickets'
    )

    subject = models.CharField(max_length=255, blank=True)

    query = models.TextField()

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Open'
    )

    ticket_level = models.CharField(
        max_length=2,
        choices=LEVEL_CHOICES,
        default='L1'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    # AI fields
    classification = models.CharField(
        max_length=100,
        blank=True
    )

    suggested_resolution = models.TextField(
        blank=True
    )

    confidence_score = models.FloatField(
        default=0
    )

    resolved_by = models.CharField(
        max_length=100,
        blank=True
    )

    escalation_reason = models.TextField(
    blank=True,
    null=True
)

    def __str__(self):
        return self.query[:50]