from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    full_name = models.CharField(max_length=150, blank=True, null=True)    
    email = models.EmailField(unique=True)
    dob = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username