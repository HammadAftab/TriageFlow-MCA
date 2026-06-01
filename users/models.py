from django.contrib.auth.models import AbstractUser
from django.db import models
import random
import string


# Create your models here.

class User(AbstractUser):
    full_name = models.CharField(max_length=150, blank=True, null=True)    
    email = models.EmailField(unique=True)
    dob = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username



def generate_employee_id():
    while True:
        letters = ''.join(random.choices(string.ascii_uppercase, k=2))
        numbers = ''.join(random.choices(string.digits, k=3))
        emp_id = f"{letters}{numbers}"

        if not Employee.objects.filter(employee_id=emp_id).exists():
            return emp_id


class Employee(models.Model):
    ROLE_CHOICES = [
        ('L1', 'L1 Support'),
        ('L2', 'L2 Support'),
        ('L3', 'L3 Support'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    employee_id = models.CharField(max_length=6, unique=True, default=generate_employee_id)
    full_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    dob = models.DateField()
    position = models.CharField(max_length=2, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee_id} - {self.position}"