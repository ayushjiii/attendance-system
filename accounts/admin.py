from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(BaseUserAdmin):
    """
    Register Employee in Django's built-in admin panel.
    Extends Django's built-in UserAdmin to add our custom fields.
    
    This lets you manage employees at http://127.0.0.1:8000/admin/
    """
    
    # Columns shown in the list view
    list_display = [
        'username',
        'get_full_name',
        'employee_id',
        'department',
        'role',
        'is_active'
    ]
    
    # Filter options on the right sidebar
    list_filter = ['role', 'department', 'is_active', 'date_joined']
    
    # Search bar (what fields to search in)
    search_fields = ['username', 'employee_id', 'first_name', 'last_name', 'email']

    # Define which fields show when editing an employee
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Employee Information', {
            'fields': ('employee_id', 'department', 'role', 'phone')
        }),
    )
    
    # Define which fields show when creating a new employee
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Employee Information', {
            'fields': ('employee_id', 'department', 'role', 'phone')
        }),
    )

    def get_full_name(self, obj):
        """Display the employee's full name in the list."""
        return obj.get_full_name()
    get_full_name.short_description = 'Full Name'