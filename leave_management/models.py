from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


class LeaveRequest(models.Model):
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
        from datetime import datetime, time
        leave_start = timezone.make_aware(
            datetime.combine(self.leave_date, time.min)
        )
        delta = leave_start - timezone.now()
        return delta.total_seconds() / 3600

    def passes_36_hour_rule(self):
        return self.hours_until_leave() >= 36


class LeaveBalance(models.Model):
    employee = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='leave_balance'
    )
    year = models.IntegerField(default=2026)
    sick_leave = models.IntegerField(default=12)
    casual_leave = models.IntegerField(default=12)
    annual_leave = models.IntegerField(default=15)
    emergency_leave = models.IntegerField(default=5)
    other_leave = models.IntegerField(default=3)

    def __str__(self):
        return f"{self.employee.get_full_name()} - {self.year}"

    def get_used(self, leave_type):
        return LeaveRequest.objects.filter(
            employee=self.employee,
            leave_type=leave_type,
            status='approved',
            leave_date__year=self.year
        ).count()

    def get_remaining(self, leave_type):
        total = getattr(self, f'{leave_type}_leave')
        return total - self.get_used(leave_type)

    def get_summary(self):
        types = ['sick', 'casual', 'annual', 'emergency', 'other']
        summary = []
        for t in types:
            total = getattr(self, f'{t}_leave')
            used = self.get_used(t)
            remaining = total - used
            summary.append({
                'type': t,
                'label': t.title(),
                'total': total,
                'used': used,
                'remaining': remaining,
            })
        return summary


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_leave_balance(sender, instance, created, **kwargs):
    """Automatically create a LeaveBalance when a new employee is created."""
    if created:
        LeaveBalance.objects.get_or_create(employee=instance)