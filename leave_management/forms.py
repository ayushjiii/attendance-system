from django import forms
from .models import LeaveRequest
from django.utils import timezone

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
            'leave_date': forms.DateInput(attrs={
                'type': 'date',
                'min': timezone.localdate().strftime('%Y-%m-%d')
            }),
            'reason': forms.TextInput(attrs={'placeholder': 'Brief reason'}),
            'note': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Optional details'}),
        }

    labels = {
        'leave_date': 'Leave Date',
        'leave_type': 'Leave Type',
        'reason': 'Reason',
        'note': 'Additional Note (optional)',
    }