from django.contrib import admin
from .models import AttendanceRecord

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ['employee', 'date', 'check_in_time', 'check_out_time', 'attendance_status']
    list_filter = ['attendance_status', 'date']
    search_fields = ['employee__first_name', 'employee__last_name', 'employee__employee_id']