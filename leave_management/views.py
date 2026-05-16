from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import LeaveRequest
from .forms import LeaveRequestForm


@login_required
def submit_leave_view(request):
    """
    Employee submits a new leave request.

    What happens:
    1. Employee fills out the form and clicks Submit
    2. We check the 36-hour rule:
       - If less than 36 hours until leave date → auto-reject immediately
       - If 36+ hours → save as 'pending' and notify admin by email
    3. Redirect to the employee's leave list
    """
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            # Save form data but don't commit to database yet
            # We need to add the employee field first
            leave_request = form.save(commit=False)
            leave_request.employee = request.user

            # Check the 36-hour rule (exception for sick and emergency leave)
            exempt_types = ['sick', 'emergency']
            if leave_request.leave_type not in exempt_types and not leave_request.passes_36_hour_rule():
                # Automatically reject — not enough notice
                leave_request.status = 'auto_rejected'
                leave_request.admin_comment = (
                    'Automatically rejected: request was submitted less than '
                    '36 hours before the leave date.'
                )
                leave_request.save()
                messages.error(
                    request,
                    f'Your leave request for {leave_request.leave_date} was '
                    f'automatically rejected. Leave must be requested at least '
                    f'36 hours in advance.'
                )
            else:
                # Valid request — save and notify admin
                leave_request.save()
                _send_leave_email_to_admin(leave_request)
                messages.success(
                    request,
                    f'Leave request for {leave_request.leave_date} submitted '
                    f'successfully. You will be notified once it is reviewed.'
                )

            return redirect('leave_management:my_leaves')
    else:
        form = LeaveRequestForm()

    return render(request, 'leave_management/submit_leave.html', {
    'form': form,
    'today_date': timezone.localdate()
    })

def _send_leave_email_to_admin(leave_request):
    """
    Send an email to the admin when a leave request is submitted.

    The underscore prefix (_) is a Python convention meaning
    this is a private helper function — not a view.

    In development, emails print to the terminal because
    EMAIL_BACKEND = console in settings.py.
    In production, swap to real SMTP settings.
    """
    employee = leave_request.employee

    subject = (
        f'Leave Request: {employee.get_full_name()} '
        f'on {leave_request.leave_date}'
    )

    message = f"""
A new leave request has been submitted.

Employee:     {employee.get_full_name()}
Employee ID:  {employee.employee_id}
Department:   {employee.department}
Leave Date:   {leave_request.leave_date}
Leave Type:   {leave_request.get_leave_type_display()}
Reason:       {leave_request.reason}
Note:         {leave_request.note or 'None'}
Submitted At: {leave_request.submitted_at.strftime('%Y-%m-%d %I:%M %p')}

Please log in to the admin dashboard to approve or reject this request.
http://127.0.0.1:8000/leave/admin/leaves/
    """

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@company.com'),
            recipient_list=[getattr(settings, 'ADMIN_EMAIL', 'admin@company.com')],
            fail_silently=True,  # Don't crash the app if email fails
        )
    except Exception:
        pass  # In production, log this properly


def _send_status_notification_email(leave_request):
    """
    Send email to employee when their leave is approved or rejected.
    """
    employee = leave_request.employee
    status = leave_request.get_status_display()
    
    subject = f'Leave Request {status} - {leave_request.leave_date}'
    
    message = f"""
Dear {employee.get_full_name()},

Your leave request has been {status.lower()}.

Details:
  Leave Date   : {leave_request.leave_date}
  Leave Type   : {leave_request.get_leave_type_display()}
  Reason       : {leave_request.reason}
  Status       : {status}
  Admin Comment: {leave_request.admin_comment or 'No comment provided'}

{"You are approved for leave on this date." if leave_request.status == 'approved' else "Please contact your manager if you have questions."}

Regards,
HR / Admin Team
    """

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[employee.email],
            fail_silently=True,
        )
    except Exception:
        pass

@login_required
def my_leaves_view(request):
    """
    Employee sees their own leave request history.
    Shows all requests sorted by most recent first.
    """
    leaves = LeaveRequest.objects.filter(employee=request.user)
    return render(request, 'leave_management/my_leaves.html', {'leaves': leaves})


@login_required
def admin_leaves_view(request):
    """
    Admin-only: see all leave requests from all employees.
    Can filter by status: pending / approved / rejected.
    """
    if not request.user.is_admin_role:
        messages.error(request, 'Admin access required.')
        return redirect('attendance:dashboard')

    leaves = LeaveRequest.objects.select_related('employee').all()

    # Optional filter by status
    status_filter = request.GET.get('status', '').strip()
    if status_filter:
        try:
            leaves = leaves.filter(status=status_filter)
        except Exception:
            pass

    return render(request, 'leave_management/admin_leaves.html', {
        'leaves': leaves,
        'status_filter': status_filter,
        'status_choices': LeaveRequest.STATUS_CHOICES,
    })


@login_required
def approve_leave_view(request, leave_id):
    """
    Admin approves a specific leave request.
    
    GET: Show confirmation page
    POST: Save approval and redirect back to leave list
    """
    if not request.user.is_admin_role:
        return redirect('attendance:dashboard')

    leave = get_object_or_404(LeaveRequest, id=leave_id)

    if request.method == 'POST':
        comment = request.POST.get('comment', '').strip()
        leave.status = 'approved'
        leave.admin_comment = comment
        leave.save()
        _send_status_notification_email(leave)
        messages.success(
            request,
            f'Leave approved for {leave.employee.get_full_name()} on {leave.leave_date}.'
        )
        return redirect('leave_management:admin_leaves')

    return render(request, 'leave_management/approve_reject.html', {
        'leave': leave,
        'action': 'approve',
    })


@login_required
def reject_leave_view(request, leave_id):
    """
    Admin rejects a specific leave request.
    
    GET: Show confirmation page
    POST: Save rejection and redirect back to leave list
    """
    if not request.user.is_admin_role:
        return redirect('attendance:dashboard')

    leave = get_object_or_404(LeaveRequest, id=leave_id)

    if request.method == 'POST':
        comment = request.POST.get('comment', '').strip()
        leave.status = 'rejected'
        leave.admin_comment = comment
        leave.save()
        _send_status_notification_email(leave)
        messages.warning(
            request,
            f'Leave rejected for {leave.employee.get_full_name()} on {leave.leave_date}.'
        )
        return redirect('leave_management:admin_leaves')

    return render(request, 'leave_management/approve_reject.html', {
        'leave': leave,
        'action': 'reject',
    })

@login_required
def delete_leave_view(request, leave_id):
    if not request.user.is_admin_role:
        return redirect('attendance:dashboard')

    leave = get_object_or_404(LeaveRequest, id=leave_id)
    if request.method == 'POST':
        leave.delete()
        messages.success(request, 'Leave request deleted.')
    return redirect('leave_management:admin_leaves')


@login_required
def leave_balance_view(request):
    from .models import LeaveBalance
    balance, created = LeaveBalance.objects.get_or_create(employee=request.user)
    summary = balance.get_summary()
    return render(request, 'leave_management/leave_balance.html', {
        'balance': balance,
        'summary': summary,
    })


@login_required
def admin_leave_balance_view(request):
    if not request.user.is_admin_role:
        return redirect('attendance:dashboard')

    from .models import LeaveBalance
    from accounts.models import Employee
    # Optimized query with prefetch_related to avoid N+1 queries
    employees = Employee.objects.filter(role='employee').prefetch_related('leave_balance')
    data = []
    for emp in employees:
        # Check if leave balance exists, otherwise create it (try to avoid creating in loops in production)
        try:
            balance = emp.leave_balance
        except LeaveBalance.DoesNotExist:
            balance, _ = LeaveBalance.objects.get_or_create(employee=emp)
            
        data.append({
            'employee': emp,
            'summary': balance.get_summary(),
        })
    return render(request, 'leave_management/admin_leave_balance.html', {'data': data})
