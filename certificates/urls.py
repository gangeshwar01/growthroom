from django.urls import path
from . import views

app_name = 'certificates'

urlpatterns = [
    path('', views.certificates_home, name='certificates_home'),
    path('certificates/', views.certificate_list, name='certificate_list'),
    path('certificates/<int:pk>/', views.certificate_detail, name='certificate_detail'),
    path('certificates/create/', views.certificate_create, name='certificate_create'),
    path('certificates/<int:pk>/update/', views.certificate_update, name='certificate_update'),
    path('certificates/<int:pk>/delete/', views.certificate_delete, name='certificate_delete'),
] 