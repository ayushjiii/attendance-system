from django.db import models
from django.conf import settings
from datetime import datetime, time, timedelta
from decimal import Decimal


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
        Calculate net hours worked. 
        - Caps duration at 10 hours total.
        - If exceeded, defaults to 8.0 working hours (as per user requirement).
        """
        if self.check_in_time and self.check_out_time:
            check_in_dt = datetime.combine(self.date, self.check_in_time)
            check_out_dt = datetime.combine(self.date, self.check_out_time)
            
            if check_out_dt < check_in_dt:
                check_out_dt += timedelta(days=1)
                
            delta = check_out_dt - check_in_dt
            total_seconds = delta.total_seconds()
            
            # 10-Hour Rule: If shift duration exceeds 10 hours, 
            # assume they forgot to check out and cap at 8 working hours.
            if total_seconds > (10 * 3600):
                return Decimal('8.00')

            worked_seconds = max(total_seconds - self.total_break_seconds, 0)
            hours = round(worked_seconds / 3600, 2)
            return Decimal(str(hours))
        return None

    @property
    def total_break_seconds(self):
        intervals = self._break_intervals()
        if not intervals:
            return 0

        intervals.sort()
        merged = []
        for start_dt, end_dt in intervals:
            if not merged or start_dt > merged[-1][1]:
                merged.append([start_dt, end_dt])
            elif end_dt > merged[-1][1]:
                merged[-1][1] = end_dt

        return sum((end_dt - start_dt).total_seconds() for start_dt, end_dt in merged)

    @property
    def total_break_hours(self):
        return round(self.total_break_seconds / 3600, 2)

    @property
    def active_break(self):
        return self.break_records.filter(break_end__isnull=True).first()

    @property
    def is_on_break(self):
        return self.active_break is not None

    @property
    def is_checked_in(self):
        """True if employee has checked in today."""
        return self.check_in_time is not None

    @property
    def is_checked_out(self):
        """True if employee has checked out today."""
        return self.check_out_time is not None

    @property
    def expected_working_hours(self):
        shift = EmployeeShift.get_active_for(self.employee)
        if shift:
            return shift.required_working_hours
        return CompanyPolicy.get_active().daily_working_hours

    def _break_intervals(self):
        if not self.check_in_time or not self.check_out_time:
            return []

        check_in_dt = datetime.combine(self.date, self.check_in_time)
        check_out_dt = datetime.combine(self.date, self.check_out_time)
        intervals = []

        policy = CompanyPolicy.get_active()
        if policy.default_break_enabled:
            default_start_dt = datetime.combine(self.date, policy.default_break_start_time)
            default_end_dt = datetime.combine(self.date, policy.default_break_end_time)
            overlap_start = max(check_in_dt, default_start_dt)
            overlap_end = min(check_out_dt, default_end_dt)
            if overlap_start < overlap_end:
                intervals.append((overlap_start, overlap_end))

        for break_record in self.break_records.all():
            if break_record.break_start and break_record.break_end:
                start_dt = datetime.combine(self.date, break_record.break_start)
                end_dt = datetime.combine(self.date, break_record.break_end)
                overlap_start = max(check_in_dt, start_dt)
                overlap_end = min(check_out_dt, end_dt)
                if overlap_start < overlap_end:
                    intervals.append((overlap_start, overlap_end))

        return intervals


class BreakRecord(models.Model):
    attendance = models.ForeignKey(
        AttendanceRecord,
        on_delete=models.CASCADE,
        related_name='break_records'
    )
    break_start = models.TimeField()
    break_end = models.TimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['break_start']

    def __str__(self):
        return f"{self.attendance.employee} - {self.attendance.date} ({self.break_start})"

    @property
    def is_active(self):
        return self.break_end is None

    @property
    def duration_seconds(self):
        if not self.break_start or not self.break_end:
            return Decimal('0')
        start_dt = datetime.combine(self.attendance.date, self.break_start)
        end_dt = datetime.combine(self.attendance.date, self.break_end)
        
        if end_dt < start_dt:
            end_dt += timedelta(days=1)
            
        return Decimal(max((end_dt - start_dt).total_seconds(), 0))

    @property
    def duration_hours(self):
        return round(float(self.duration_seconds) / 3600, 2)


class CompanyPolicy(models.Model):
    name = models.CharField(max_length=100, default='Default Policy')
    office_start_time = models.TimeField(default=time(9, 30))
    late_threshold_time = models.TimeField(default=time(10, 0))
    default_break_enabled = models.BooleanField(default=True)
    default_break_start_time = models.TimeField(default=time(13, 0))
    default_break_end_time = models.TimeField(default=time(14, 0))
    minimum_session_minutes = models.PositiveIntegerField(default=5)
    daily_working_hours = models.DecimalField(max_digits=4, decimal_places=2, default=8)
    half_day_hours = models.DecimalField(max_digits=4, decimal_places=2, default=4)
    leave_notice_hours = models.PositiveIntegerField(default=36)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Company Policy'
        verbose_name_plural = 'Company Policies'

    def __str__(self):
        return self.name

    @classmethod
    def get_active(cls):
        policy = cls.objects.filter(is_active=True).order_by('-updated_at').first()
        if policy:
            return policy

        return cls(
            office_start_time=_setting_time('OFFICE_START_TIME', time(9, 30)),
            late_threshold_time=_setting_time('LATE_THRESHOLD_TIME', time(10, 0)),
            default_break_start_time=_setting_time('DEFAULT_BREAK_START_TIME', time(13, 0)),
            default_break_end_time=_setting_time('DEFAULT_BREAK_END_TIME', time(14, 0)),
        )


def _setting_time(name, default):
    value = getattr(settings, name, None)
    if not value:
        return default

    try:
        hour, minute = value.split(':')
        return time(int(hour), int(minute))
    except (AttributeError, TypeError, ValueError):
        return default


class EmployeeShift(models.Model):
    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='shifts'
    )
    name = models.CharField(max_length=100, default='Regular Shift')
    start_time = models.TimeField()
    end_time = models.TimeField()
    required_working_hours = models.DecimalField(max_digits=4, decimal_places=2, default=8)
    grace_minutes = models.PositiveIntegerField(default=30)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['employee__first_name', 'employee__last_name', 'start_time']

    def __str__(self):
        return f"{self.employee} - {self.name}"

    @property
    def late_threshold_time(self):
        # Use a dummy date for time calculation to avoid timezone/day rollover issues
        dummy_date = date(2000, 1, 1)
        start_dt = datetime.combine(dummy_date, self.start_time)
        return (start_dt + timedelta(minutes=self.grace_minutes)).time()

    @classmethod
    def get_active_for(cls, employee):
        return cls.objects.filter(employee=employee, is_active=True).order_by('-updated_at').first()
