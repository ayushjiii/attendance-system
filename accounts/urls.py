from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('employees/', views.employee_list_view, name='employee_list'),
    path('employees/create/', views.create_employee_view, name='create_employee'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/change-password/', views.change_password_view, name='change_password'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
]