from django.contrib.auth.models import AbstractUser
from django.db import models

class Employee(AbstractUser):
    """
    Custom user model. Extends Django's built-in AbstractUser so we keep
    all authentication features (login, password hashing, sessions, etc.)
    and add our own employee-specific fields.
    
    When a user logs in, Django will use this model instead of the default User.
    """

    ROLE_CHOICES = [
        ('employee', 'Employee'),
        ('admin', 'Admin'),
    ]

    # Employee-specific fields
    employee_id = models.CharField(
        max_length=20,
        unique=True,
        help_text="Unique employee ID (e.g., EMP001)"
    )
    department = models.CharField(
        max_length=100,
        default='General',
        help_text="Department name (e.g., Engineering, HR, Sales)"
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='employee',
        help_text="Admin can create/manage employees. Employee can only check in/out."
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        help_text="Contact phone number (optional)"
    )

    class Meta:
        ordering = ['first_name', 'last_name']
        verbose_name = "Employee"
        verbose_name_plural = "Employees"

    def __str__(self):
        """Return a readable string representation."""
        return f"{self.get_full_name()} ({self.employee_id})"

    @property
    def is_admin_role(self):
        """
        Helper method to check if this employee has admin role.
        This is different from is_staff/is_superuser.
        Use this to check permissions in views.
        
        Example:
            if employee.is_admin_role:
                # Show admin dashboard
        """
        return self.role == 'admin'