from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Employee


class EmployeeCreationForm(UserCreationForm):
    class Meta:
        model = Employee
        fields = [
            'username', 'first_name', 'last_name', 'email',
            'department', 'role', 'phone',
            'password1', 'password2'
        ]
        # employee_id removed — auto-generated on save

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all fields
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'