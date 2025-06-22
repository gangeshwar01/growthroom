from django.urls import path
from . import views

app_name = 'employee_portal'

urlpatterns = [
    path('login/', views.employee_login, name='login'),
    path('dashboard/', views.employee_dashboard, name='emp_dashboard'),
    path('logout/', views.employee_logout, name='logout'),
] 