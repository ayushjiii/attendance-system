from django import forms
from .models import LeaveRequest


class LeaveRequestForm(forms.ModelForm):
    """
    Form for submitting a leave request.
    
    The employee fills in:
    - leave_date: which day they want off
    - leave_type: dropdown (sick, casual, annual, etc.)
    - reason: short text
    - note: optional longer explanation
    
    We do NOT include 'employee' or 'status' here because those
    are set by the view, not chosen by the user.
    """

    class Meta:
        model = LeaveRequest
        fields = ['leave_date', 'leave_type', 'reason', 'note']
        widgets = {
            # type="date" gives a date picker in the browser
            'leave_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'leave_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'reason': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Brief reason for leave'
            }),
            'note': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Optional: additional details'
            }),
        }
        labels = {
            'leave_date': 'Leave Date',
            'leave_type': 'Leave Type',
            'reason': 'Reason',
            'note': 'Additional Note (optional)',
        }