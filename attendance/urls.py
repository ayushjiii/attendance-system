from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('check-in/', views.check_in_view, name='check_in'),
    path('check-out/', views.check_out_view, name='check_out'),
    path('history/', views.attendance_history_view, name='history'),
    path('all-attendance/', views.admin_attendance_view, name='admin_attendance')
]