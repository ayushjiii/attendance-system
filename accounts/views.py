
# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Employee
from .forms import EmployeeCreationForm

def login_view(request):
    """
    Display and handle the login form.
    
    GET: Show empty login form
    POST: Validate username/password and log user in
    
    If user is already logged in, redirect to dashboard.
    """
    # Redirect if already logged in
    if request.user.is_authenticated:
        return redirect('attendance:dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Django's authenticate() checks the password against the hashed version
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Login was successful
            login(request, user)  # This creates a session
            messages.success(request, f'Welcome back, {user.first_name}!')
            return redirect('attendance:dashboard')
        else:
            # Login failed
            messages.error(request, 'Invalid username or password.')

    return render(request, 'accounts/login.html')

def logout_view(request):
    """
    Log the user out and clear their session.
    Redirect to login page.
    """
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('accounts:login')

@login_required
def create_employee_view(request):
    """
    Admin-only view to create a new employee account.
    
    @login_required: Redirects unauthenticated users to login page
    We also manually check is_admin_role for extra safety.
    
    GET: Show the form
    POST: Create the employee
    """
    # Check that user is admin
    if not request.user.is_admin_role:
        messages.error(request, 'Only admins can create employee accounts.')
        return redirect('attendance:dashboard')

    if request.method == 'POST':
        form = EmployeeCreationForm(request.POST)
        if form.is_valid():
            employee = form.save(commit=False)
            # Password is already hashed by the form
            employee.save()
            messages.success(
                request,
                f'Account created for {employee.get_full_name()} ({employee.employee_id}).'
            )
            return redirect('accounts:employee_list')
    else:
        form = EmployeeCreationForm()

    return render(request, 'accounts/create_employee.html', {'form': form})

@login_required
def employee_list_view(request):
    """
    Admin-only view to list all employees.
    Shows name, ID, department, role, and active status.
    """
    if not request.user.is_admin_role:
        return redirect('attendance:dashboard')

    employees = Employee.objects.all().order_by('department', 'first_name')
    return render(request, 'accounts/employee_list.html', {'employees': employees})