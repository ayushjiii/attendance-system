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
            last = Employee.objects.order_by('-id').first()
            if last and last.employee_id.startswith('EMP'):
                try:
                    last_number = int(last.employee_id[3:])
                    self.employee_id = f'EMP{(last_number + 1):03d}'
                except ValueError:
                    self.employee_id = 'EMP001'
            else:
                self.employee_id = 'EMP001'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_full_name()} ({self.employee_id})"

    @property
    def is_admin_role(self):
        return self.role == 'admin'