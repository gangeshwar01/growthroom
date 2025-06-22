from django.urls import path
from . import views

app_name = 'training'

urlpatterns = [
    path('', views.training_home, name='training_home'),
    path('sessions/', views.session_list, name='session_list'),
    path('sessions/<int:pk>/', views.session_detail, name='session_detail'),
    path('sessions/create/', views.session_create, name='session_create'),
    path('sessions/<int:pk>/update/', views.session_update, name='session_update'),
    path('sessions/<int:pk>/delete/', views.session_delete, name='session_delete'),
    path('sessions/<int:pk>/mark-attendance/', views.mark_attendance, name='mark_attendance'),
] 