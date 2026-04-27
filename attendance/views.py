from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, date, time as time_type


from .models import AttendanceRecord
from .utils import get_client_ip, is_office_ip, is_within_office_radius, get_device_info


@login_required
def dashboard_view(request):
    """
    Main page after login.
    Shows today's check-in status and last 7 days of attendance.
    
    @login_required means: if user is NOT logged in,
    Django automatically redirects them to the login page.
    """
    today = timezone.localdate()

    # Try to find today's attendance record
    try:
        today_record = AttendanceRecord.objects.get(
            employee=request.user,
            date=today
        )
    except AttendanceRecord.DoesNotExist:
        today_record = None  # No check-in yet today

    # Get last 7 attendance entries
    recent_records = AttendanceRecord.objects.filter(
        employee=request.user
    ).order_by('-date')[:7]

    return render(request, 'attendance/dashboard.html', {
        'today_record': today_record,
        'recent_records': recent_records,
        'today': today,
    })


@login_required
def check_in_view(request):
    """
    Handle the Check In button.
    
    Security checks (in order):
    1. Must be a POST request (not just visiting the URL)
    2. IP must be from the office network
    3. GPS must be within office radius (if provided by browser)
    4. Cannot check in twice in one day
    """
    if request.method != 'POST':
        return redirect('attendance:dashboard')

    today = timezone.localdate()
    now = timezone.localtime().time()
    ip = get_client_ip(request)

    # --- Security Check 1: Office IP ---
    if not is_office_ip(ip):
        messages.error(
            request,
            f'Check-in is only allowed from the office network. '
            f'Your current IP address ({ip}) is not authorised.'
        )
        return redirect('attendance:dashboard')

    # --- Security Check 2: Already checked in today? ---
    existing = AttendanceRecord.objects.filter(
        employee=request.user,
        date=today
    ).first()

    if existing and existing.is_checked_in:
        messages.warning(request, 'You have already checked in today.')
        return redirect('attendance:dashboard')

    # --- Security Check 3: GPS location (optional) ---
    latitude = request.POST.get('latitude')
    longitude = request.POST.get('longitude')

    if latitude and longitude:
        try:
            if not is_within_office_radius(float(latitude), float(longitude)):
                messages.error(
                    request,
                    'Your GPS location is outside the office area. '
                    'Please check in from the office.'
                )
                return redirect('attendance:dashboard')
        except (ValueError, TypeError):
            pass  # Invalid GPS data — skip the GPS check

    # --- All checks passed: save the check-in ---
    record, created = AttendanceRecord.objects.get_or_create(
        employee=request.user,
        date=today
    )
    record.check_in_time = now
    record.ip_address = ip
    record.device_info = get_device_info(request)
    if latitude and longitude:
        record.gps_latitude = latitude
        record.gps_longitude = longitude

    # Mark as late if check-in is after 10:00 AM
    check_in_start = time_type(9, 30)   # office opens 9:30 AM
    late_threshold = time_type(10, 0)   # late after 10:00 AM

    # Block check-in before 9:30 AM
    if now < check_in_start:
        messages.error(request, 'Check-in is not allowed before 9:30 AM.')
        return redirect('attendance:dashboard')

    # Mark as late if after 10:00 AM
    if now > late_threshold:
        record.attendance_status = 'late'
    else:
        record.attendance_status = 'present'

    record.save()
    
    messages.success(
        request,
        f'Checked in successfully at {now.strftime("%H:%M")}.'
    )
    return redirect('attendance:dashboard')


@login_required
def check_out_view(request):
    """
    Handle the Check Out button.
    
    Validation:
    - Must have checked in today first
    - Cannot check out twice
    - Session must be at least 5 minutes long (prevents accidental instant checkout)
    """
    if request.method != 'POST':
        return redirect('attendance:dashboard')

    today = timezone.localdate()
    now = timezone.localtime().time()

    # Find today's record
    try:
        record = AttendanceRecord.objects.get(
            employee=request.user,
            date=today
        )
    except AttendanceRecord.DoesNotExist:
        messages.error(request, 'You have not checked in today. Cannot check out.')
        return redirect('attendance:dashboard')

    # Prevent double checkout
    if record.is_checked_out:
        messages.warning(request, 'You have already checked out today.')
        return redirect('attendance:dashboard')

    # Prevent checkout without check-in
    if not record.is_checked_in:
        messages.error(request, 'You must check in before checking out.')
        return redirect('attendance:dashboard')

    # Prevent unrealistically short sessions (< 5 minutes)
    check_in_dt = datetime.combine(date.today(), record.check_in_time)
    check_out_dt = datetime.combine(date.today(), now)
    session_minutes = (check_out_dt - check_in_dt).total_seconds() / 60

    if session_minutes < 5:
        messages.error(
            request,
            f'Session too short ({int(session_minutes)} minutes). '
            f'Minimum 5 minutes required before checkout.'
        )
        return redirect('attendance:dashboard')

    # Save checkout and calculate hours
    record.check_out_time = now
    record.total_working_hours = record.calculate_working_hours()
    record.save()

    messages.success(
        request,
        f'Checked out at {now.strftime("%H:%M")}. '
        f'Total working time: {record.total_working_hours} hours.'
    )
    return redirect('attendance:dashboard')


@login_required
def attendance_history_view(request):
    """
    Employee's personal attendance history.
    Can be filtered by month using ?month=2024-01 in the URL.
    """
    records = AttendanceRecord.objects.filter(employee=request.user)
    month = request.GET.get('month', '')
    if month:
        try:
            year, m = month.split('-')
            records = records.filter(
                date__year=int(year),
                date__month=int(m)
            )
        except (ValueError, AttributeError):
            pass  # Ignore invalid month format

    records = records.order_by('-date')
    return render(request, 'attendance/history.html', {
        'records': records,
        'month': month,
    })


@login_required
def admin_attendance_view(request):
    """
    Admin-only: see all employees' attendance records.
    Supports search by employee name/ID, date, or month.
    """
    if not request.user.is_admin_role:
        messages.error(request, 'Admin access required.')
        return redirect('attendance:dashboard')

    records = AttendanceRecord.objects.select_related('employee').all()

    # --- Filters ---
    employee_search = request.GET.get('employee', '').strip()
    date_filter = request.GET.get('date', '').strip()
    month_filter = request.GET.get('month', '').strip()

    if employee_search:
        records = records.filter(
            employee__first_name__icontains=employee_search
        ) | records.filter(
            employee__last_name__icontains=employee_search
        ) | records.filter(
            employee__employee_id__icontains=employee_search
        )

    if date_filter:
        records = records.filter(date=date_filter)

    if month_filter:
        try:
            year, month = month_filter.split('-')
            records = records.filter(
                date__year=int(year),
                date__month=int(month)
            )
        except (ValueError, AttributeError):
            pass

    records = records.order_by('-date')

    return render(request, 'attendance/admin_attendance.html', {
        'records': records,
        'employee_search': employee_search,
        'date_filter': date_filter,
        'month_filter': month_filter,
    })