from django.contrib import admin
from .models import AttendanceRecord, BreakRecord, CompanyPolicy, EmployeeShift

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ['employee', 'date', 'check_in_time', 'check_out_time', 'total_working_hours', 'attendance_status']
    list_filter = ['attendance_status', 'date']
    search_fields = ['employee__first_name', 'employee__last_name', 'employee__employee_id']


@admin.register(BreakRecord)
class BreakRecordAdmin(admin.ModelAdmin):
    list_display = ['attendance', 'break_start', 'break_end', 'duration_hours']
    list_filter = ['attendance__date']
    search_fields = [
        'attendance__employee__first_name',
        'attendance__employee__last_name',
        'attendance__employee__employee_id',
    ]


@admin.register(CompanyPolicy)
class CompanyPolicyAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'office_start_time',
        'late_threshold_time',
        'default_break_enabled',
        'default_break_start_time',
        'default_break_end_time',
        'daily_working_hours',
        'is_active',
    ]
    list_filter = ['is_active', 'default_break_enabled']


@admin.register(EmployeeShift)
class EmployeeShiftAdmin(admin.ModelAdmin):
    list_display = [
        'employee',
        'name',
        'start_time',
        'end_time',
        'required_working_hours',
        'grace_minutes',
        'late_threshold_time',
        'is_active',
    ]
    list_filter = ['is_active', 'start_time']
    search_fields = ['employee__first_name', 'employee__last_name', 'employee__employee_id', 'name']
