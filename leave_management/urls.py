from django.urls import path
from . import views

app_name = 'leave_management'

urlpatterns = [
    path('submit/', views.submit_leave_view, name='submit'),
    path('my-leaves/', views.my_leaves_view, name='my_leaves'),
    path('admin/leaves/', views.admin_leaves_view, name='admin_leaves'),
    path('admin/leaves/<int:leave_id>/approve/', views.approve_leave_view, name='approve'),
    path('admin/leaves/<int:leave_id>/reject/', views.reject_leave_view, name='reject'),
]