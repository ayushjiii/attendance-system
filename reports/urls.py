from django.urls import path
from django.http import HttpResponse

app_name = 'reports'

def coming_soon(request):
    return HttpResponse("Reports coming soon.")

urlpatterns = [
    path('', coming_soon, name='monthly_report'),
]