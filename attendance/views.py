from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, date


from .models import AttendanceRecord, BreakRecord, CompanyPolicy, EmployeeShift
from .templatetags.attendance_filters import format_hours_value
from .utils import get_client_ip, is_office_ip, is_within_office_radius, get_device_info


@login_required
def dashboard_view(request):
    """
    Main page after login.
    Shows today's check-in status and last 7 days of attendance.
    """
    today = timezone.localdate()

    # 1. Look for an active (not yet checked out) session
    # This could be from yesterday if it's a night shift
    active_record = AttendanceRecord.objects.filter(
        employee=request.user,
        check_out_time__isnull=True
    ).order_by('-date', '-check_in_time').first()

    # 2. If no active session, check if they already COMPLETED a shift today
    # (Prevents the UNIQUE constraint error)
    if not active_record:
        active_record = AttendanceRecord.objects.filter(
            employee=request.user,
            date=today,
            check_out_time__isnull=False
        ).first()

    # Get last 7 attendance entries
    recent_records = AttendanceRecord.objects.filter(
        employee=request.user
    ).order_by('-date')[:7]

    return render(request, 'attendance/dashboard.html', {
        'today_record': active_record,
        'recent_records': recent_records,
        'today': today,
    })


@login_required
def check_in_view(request):
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

    # --- Security Check 2: Already have an active session? ---
    active_session = AttendanceRecord.objects.filter(
        employee=request.user,
        check_out_time__isnull=True
    ).exists()

    if active_session:
        messages.warning(request, 'You already have an active session. Please check out first.')
        return redirect('attendance:dashboard')

    # --- Security Check 3: Already completed a shift on this calendar date? ---
    # This prevents the IntegrityError (UNIQUE constraint)
    if AttendanceRecord.objects.filter(employee=request.user, date=today).exists():
        messages.warning(request, 'Your attendance for today is already complete.')
        return redirect('attendance:dashboard')

    # --- Security Check 4: GPS location ---
    latitude = request.POST.get('latitude')
    longitude = request.POST.get('longitude')

    if latitude and longitude:
        try:
            if not is_within_office_radius(float(latitude), float(longitude)):
                messages.error(
                    request,
                    'Your GPS location is outside the office area.'
                )
                return redirect('attendance:dashboard')
        except (ValueError, TypeError):
            pass

    # --- All checks passed: create the record ---
    record = AttendanceRecord.objects.create(
        employee=request.user,
        date=today,
        check_in_time=now,
        ip_address=ip,
        device_info=get_device_info(request)
    )
    if latitude and longitude:
        record.gps_latitude = latitude
        record.gps_longitude = longitude

    # --- Determine Late Threshold and Start Time ---
    shift = EmployeeShift.get_active_for(request.user)
    policy = CompanyPolicy.get_active()
    
    if shift:
        check_in_start = shift.start_time
        late_threshold = shift.late_threshold_time
    else:
        check_in_start = policy.office_start_time
        late_threshold = policy.late_threshold_time

    # Block check-in before the configured office start time.
    if now < check_in_start:
        messages.error(
            request,
            f'Check-in is not allowed before {check_in_start.strftime("%I:%M %p")}.'
        )
        return redirect('attendance:dashboard')

    # Mark as late if after the threshold.
    if now > late_threshold:
        record.attendance_status = 'late'
    else:
        record.attendance_status = 'present'

    record.save()
    messages.success(request, f'Checked in successfully at {now.strftime("%I:%M %p")}.')
    return redirect('attendance:dashboard')


@login_required
def start_break_view(request):
    if request.method != 'POST':
        return redirect('attendance:dashboard')

    now = timezone.localtime().time()
    record = AttendanceRecord.objects.filter(
        employee=request.user,
        check_out_time__isnull=True
    ).order_by('-date', '-check_in_time').first()

    if not record:
        messages.error(request, 'You must check in before starting a break.')
        return redirect('attendance:dashboard')

    if record.is_on_break:
        messages.warning(request, 'You are already on a break.')
        return redirect('attendance:dashboard')

    BreakRecord.objects.create(attendance=record, break_start=now)
    messages.success(request, f'Break started at {now.strftime("%I:%M %p")}.')
    return redirect('attendance:dashboard')


@login_required
def end_break_view(request):
    if request.method != 'POST':
        return redirect('attendance:dashboard')

    now = timezone.localtime().time()
    record = AttendanceRecord.objects.filter(
        employee=request.user,
        check_out_time__isnull=True
    ).order_by('-date', '-check_in_time').first()

    if not record:
        messages.error(request, 'You do not have an active session.')
        return redirect('attendance:dashboard')

    active_break = record.active_break
    if not active_break:
        messages.warning(request, 'You are not currently on a break.')
        return redirect('attendance:dashboard')

    active_break.break_end = now
    active_break.save()
    messages.success(request, f'Break ended at {now.strftime("%I:%M %p")}.')
    return redirect('attendance:dashboard')


@login_required
def check_out_view(request):
    if request.method != 'POST':
        return redirect('attendance:dashboard')

    now_dt = timezone.localtime()
    now_time = now_dt.time()

    record = AttendanceRecord.objects.filter(
        employee=request.user,
        check_out_time__isnull=True
    ).order_by('-date', '-check_in_time').first()

    if not record:
        messages.error(request, 'You have no active attendance record to check out from.')
        return redirect('attendance:dashboard')

    if record.is_on_break:
        messages.error(request, 'Please end your active break before checking out.')
        return redirect('attendance:dashboard')

    check_in_dt = datetime.combine(record.date, record.check_in_time)
    if timezone.is_aware(now_dt):
        from django.utils.timezone import get_current_timezone
        check_in_dt = timezone.make_aware(check_in_dt, get_current_timezone())

    session_minutes = (now_dt - check_in_dt).total_seconds() / 60
    policy = CompanyPolicy.get_active()
    
    if session_minutes < policy.minimum_session_minutes:
        messages.error(
            request,
            f'Session too short ({int(session_minutes)} minutes). '
            f'Minimum {policy.minimum_session_minutes} minutes required.'
        )
        return redirect('attendance:dashboard')

    record.check_out_time = now_time
    record.total_working_hours = record.calculate_working_hours()
    record.save()

    messages.success(
        request,
        f'Checked out at {now_time.strftime("%I:%M %p")}. '
        f'Total working time: {format_hours_value(record.total_working_hours)}.'
    )
    return redirect('attendance:dashboard')


@login_required
def attendance_history_view(request):
    records = AttendanceRecord.objects.filter(employee=request.user)
    month = request.GET.get('month', '')
    if month:
        try:
            year, m = month.split('-')
            records = records.filter(date__year=int(year), date__month=int(m))
        except (ValueError, AttributeError, Exception):
            pass

    records = records.order_by('-date')
    return render(request, 'attendance/history.html', {
        'records': records,
        'month': month,
    })


@login_required
def admin_attendance_view(request):
    if not request.user.is_admin_role:
        messages.error(request, 'Admin access required.')
        return redirect('attendance:dashboard')

    records = AttendanceRecord.objects.select_related('employee').all()
    employee_search = request.GET.get('employee', '').strip()
    date_filter = request.GET.get('date', '').strip()

    if employee_search:
        records = records.filter(
            employee__first_name__icontains=employee_search
        ) | records.filter(
            employee__last_name__icontains=employee_search
        ) | records.filter(
            employee__employee_id__icontains=employee_search
        )

    if date_filter:
        try:
            records = records.filter(date=date_filter)
        except Exception:
            pass

    records = records.order_by('-date')
    return render(request, 'attendance/admin_attendance.html', {
        'records': records,
        'employee_search': employee_search,
        'date_filter': date_filter,
    })
