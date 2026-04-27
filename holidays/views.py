from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Holiday
from .forms import HolidayForm


@login_required
def holiday_list_view(request):
    holidays = Holiday.objects.all()
    return render(request, 'holidays/holiday_list.html', {'holidays': holidays})


@login_required
def add_holiday_view(request):
    if not request.user.is_admin_role:
        return redirect('attendance:dashboard')

    if request.method == 'POST':
        form = HolidayForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Holiday added successfully.')
            return redirect('holidays:list')
    else:
        form = HolidayForm()
    return render(request, 'holidays/add_holiday.html', {'form': form})


@login_required
def delete_holiday_view(request, holiday_id):
    if not request.user.is_admin_role:
        return redirect('attendance:dashboard')

    holiday = get_object_or_404(Holiday, id=holiday_id)
    if request.method == 'POST':
        holiday.delete()
        messages.success(request, 'Holiday deleted.')
    return redirect('holidays:list')