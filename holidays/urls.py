from django.urls import path
from . import views

app_name = 'holidays'

urlpatterns = [
    path('', views.holiday_list_view, name='list'),
    path('add/', views.add_holiday_view, name='add'),
    path('<int:holiday_id>/delete/', views.delete_holiday_view, name='delete'),
]