from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('', views.attendance_home, name='attendance_home'),
    path('records/', views.attendance_list, name='attendance_list'),
    path('records/<int:pk>/', views.attendance_detail, name='attendance_detail'),
    path('records/create/', views.attendance_create, name='attendance_create'),
    path('records/<int:pk>/update/', views.attendance_update, name='attendance_update'),
    path('records/<int:pk>/delete/', views.attendance_delete, name='attendance_delete'),
] 