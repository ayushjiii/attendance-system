from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Employee

class EmployeeCreationForm(UserCreationForm):
    """
    Form for creating a new employee account.
    Inherits from Django's UserCreationForm which handles:
    - Checking that passwords match
    - Password hashing (we never store plain passwords)
    - Field validation
    
    Usage:
        form = EmployeeCreationForm(request.POST)
        if form.is_valid():
            employee = form.save()
    """
    
    class Meta:
        model = Employee
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'employee_id',
            'department',
            'role',
            'phone',
            'password1',
            'password2'
        ]
        labels = {
            'username': 'Username (for login)',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email Address',
            'employee_id': 'Employee ID',
            'department': 'Department',
            'role': 'Role (Admin or Employee)',
            'phone': 'Phone (optional)',
            'password1': 'Password',
            'password2': 'Confirm Password',
        }