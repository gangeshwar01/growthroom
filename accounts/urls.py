from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.accounts_home, name='accounts_home'),
    path('profiles/', views.profile_list, name='profile_list'),
    path('profiles/<int:pk>/', views.profile_detail, name='profile_detail'),
    path('profiles/create/', views.profile_create, name='profile_create'),
    path('profiles/<int:pk>/update/', views.profile_update, name='profile_update'),
    path('profiles/<int:pk>/delete/', views.profile_delete, name='profile_delete'),
    path('login/', views.login_view, name='accounts_login'),
    path('logout/', views.logout_view, name='accounts_logout'),
    path('register/', views.register_employee, name='register_employee'),
] 