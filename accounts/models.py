from django.db import models
from django.contrib.auth.models import AbstractUser


class Employee(AbstractUser):
    ROLE_CHOICES = [
        ('employee', 'Employee'),
        ('admin', 'Admin'),
    ]

    employee_id = models.CharField(max_length=20, unique=True, blank=True)
    department = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='employee')
    phone = models.CharField(max_length=20, blank=True)

    def save(self, *args, **kwargs):
        # Auto-generate employee ID only if not already set
        if not self.employee_id:
            # Find the highest existing EMP ID
            last_emp = Employee.objects.filter(employee_id__startswith='EMP').order_by('employee_id').last()
            if last_emp:
                try:
                    # Extract the number and increment it
                    last_number = int(last_emp.employee_id[3:])
                    self.employee_id = f'EMP{(last_number + 1):03d}'
                except (ValueError, IndexError):
                    self.employee_id = 'EMP001'
            else:
                self.employee_id = 'EMP001'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_full_name()} ({self.employee_id})"

    @property
    def is_admin_role(self):
        return self.role == 'admin'