from django.db import models
from django.conf import settings
from datetime import datetime


class AttendanceRecord(models.Model):
    """
    Stores one attendance record per employee per day.
    
    Fields:
    - employee: who this record belongs to
    - date: which day
    - check_in_time / check_out_time: when they arrived/left
    - total_working_hours: auto-calculated on checkout
    - ip_address: for anti-fake verification
    - device_info: browser + OS (audit trail)
    - gps_latitude/longitude: location at time of check-in
    - attendance_status: present / absent / late / etc.
    """

    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('half_day', 'Half Day'),
        ('late', 'Late'),
        ('on_leave', 'On Leave'),
    ]

    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,       # delete records if employee is deleted
        related_name='attendance_records'
    )
    date = models.DateField()
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    total_working_hours = models.DecimalField(
        max_digits=5, decimal_places=2,
        null=True, blank=True
    )

    # Security / audit fields
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    device_info = models.TextField(blank=True)
    gps_latitude = models.DecimalField(
        max_digits=9, decimal_places=6,
        null=True, blank=True
    )
    gps_longitude = models.DecimalField(
        max_digits=9, decimal_places=6,
        null=True, blank=True
    )

    attendance_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='present'
    )
    notes = models.TextField(blank=True)

    class Meta:
        # Database-level constraint: only ONE record per employee per day
        unique_together = ['employee', 'date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.employee} - {self.date} ({self.attendance_status})"

    def calculate_working_hours(self):
        """
        Calculate total hours worked.
        Called automatically when the employee checks out.
        
        Returns hours as a float rounded to 2 decimal places.
        Example: 8.5 means 8 hours 30 minutes.
        """
        if self.check_in_time and self.check_out_time:
            check_in_dt = datetime.combine(self.date, self.check_in_time)
            check_out_dt = datetime.combine(self.date, self.check_out_time)
            delta = check_out_dt - check_in_dt
            hours = round(delta.total_seconds() / 3600, 2)
            return hours
        return None

    @property
    def is_checked_in(self):
        """True if employee has checked in today."""
        return self.check_in_time is not None

    @property
    def is_checked_out(self):
        """True if employee has checked out today."""
        return self.check_out_time is not None