from django.contrib import admin
from .models import User, Employee

# Register your models here.
admin.site.register(User)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        "employee_id",
        "full_name",
        "position",
        "email",
    )

    list_filter = (
        "position",
    )

    search_fields = (
        "employee_id",
        "full_name",
        "email",
    )