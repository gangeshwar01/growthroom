from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    # Project URLs
    path('projects/', views.project_list, name='project_list'),
    path('projects/create/', views.project_create, name='project_create'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('projects/<int:pk>/update/', views.project_update, name='project_update'),
    path('projects/<int:pk>/delete/', views.project_delete, name='project_delete'),
    
    # Task URLs
    path('', views.task_list, name='task_list'),
    path('create/', views.task_create, name='task_create'),
    path('<int:pk>/', views.task_detail, name='task_detail'),
    path('<int:pk>/update/', views.task_update, name='task_update'),
    path('<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('<int:pk>/comment/', views.task_add_comment, name='task_add_comment'),
    path('<int:pk>/complete/', views.task_mark_complete, name='task_mark_complete'),
    path('<int:pk>/in-progress/', views.task_mark_in_progress, name='task_mark_in_progress'),
    path('<int:pk>/pending/', views.task_mark_pending, name='task_mark_pending'),
] 