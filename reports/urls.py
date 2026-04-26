from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.monthly_report_view, name='monthly_report'),
    path('export/csv/', views.export_csv_view, name='export_csv'),
    path('export/excel/', views.export_excel_view, name='export_excel'),
    path('employee/<int:employee_id>/', views.employee_detail_report_view, name='employee_detail')
]