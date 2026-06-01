from django.db import models
from django.conf import settings

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Pending', 'Pending'),
        ('Closed', 'Closed')
    ]

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_tickets'
    )

    query = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Open')
    created_at = models.DateTimeField(auto_now_add=True)

    ticket_level = models.CharField(max_length=2,
    choices=[
        ('L3', 'L3'),
        ('L2', 'L2'),
        ('L1', 'L1'),
    ],
    default='L3'
    )

    def __str__(self):
        return self.query[:50]