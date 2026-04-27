from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(UserAdmin):
    list_display = ['username', 'employee_id', 'get_full_name', 'department', 'role', 'is_active']
    list_filter = ['role', 'department', 'is_active']
    search_fields = ['username', 'employee_id', 'first_name', 'last_name', 'email']

    # employee_id is visible but cannot be edited
    readonly_fields = ['employee_id']

    fieldsets = UserAdmin.fieldsets + (
        ('Employee Info', {'fields': ('employee_id', 'department', 'role', 'phone')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Employee Info', {'fields': ('department', 'role', 'phone')}),
        # employee_id not shown on add — auto generated
    )