from django.db import models
from django.conf import settings
from django.utils import timezone


class LeaveRequest(models.Model):
    """
    Stores an employee's leave request.

    Key business rule:
        Leave must be requested at least 36 hours in advance.
        If not, it is automatically rejected when submitted.

    Fields:
    - employee: who is requesting leave
    - leave_date: the day they want off
    - leave_type: sick / casual / annual / etc.
    - reason: short description
    - note: optional extra details
    - submitted_at: auto-filled when created
    - status: pending → approved / rejected / auto_rejected
    - admin_comment: admin's note when approving or rejecting
    """

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('auto_rejected', 'Auto-Rejected (less than 36 hrs notice)'),
    ]

    LEAVE_TYPE_CHOICES = [
        ('sick', 'Sick Leave'),
        ('casual', 'Casual Leave'),
        ('annual', 'Annual Leave'),
        ('emergency', 'Emergency Leave'),
        ('other', 'Other'),
    ]

    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='leave_requests'
    )
    leave_date = models.DateField()
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPE_CHOICES)
    reason = models.CharField(max_length=200)
    note = models.TextField(blank=True)

    # auto_now_add=True means Django fills this in automatically when created
    submitted_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    admin_comment = models.TextField(blank=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.employee} - {self.leave_date} ({self.status})"

    def hours_until_leave(self):
        """
        How many hours remain between now and the leave date?
        
        We calculate from now until midnight of the leave date.
        Example: if leave_date is tomorrow and it's 8 PM now,
        there are only ~4 hours left — which is less than 36.
        """
        from datetime import datetime, time
        # Set leave start to midnight of the leave date
        leave_start = timezone.make_aware(
            datetime.combine(self.leave_date, time.min)
        )
        delta = leave_start - timezone.now()
        return delta.total_seconds() / 3600

    def passes_36_hour_rule(self):
        """
        Returns True if the request was submitted at least
        36 hours before the leave date. Otherwise False.
        
        This is called before saving the request.
        If False, the status is set to 'auto_rejected'.
        """
        return self.hours_until_leave() >= 36