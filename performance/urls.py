from django.urls import path
from . import views

app_name = 'performance'

urlpatterns = [
    path('', views.performance_home, name='performance_home'),
    path('my-performance/', views.my_performance, name='my_performance'),
    path('review/add/', views.performance_review_create, name='performance_review_create'),
    path('review/<int:pk>/update/', views.performance_review_update, name='performance_review_update'),
    path('review/<int:pk>/delete/', views.performance_review_delete, name='performance_review_delete'),
] 