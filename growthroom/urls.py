"""
URL configuration for growthroom project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from accounts.custom_admin import custom_admin_site

urlpatterns = [
    path('admin/', custom_admin_site.urls),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('attendance/', include('attendance.urls', namespace='attendance')),
    path('training/', include('training.urls', namespace='training')),
    path('tasks/', include('tasks.urls', namespace='tasks')),
    path('performance/', include('performance.urls', namespace='performance')),
    path('certificates/', include('certificates.urls', namespace='certificates')),
    path('employee-portal/', include('employee_portal.urls', namespace='employee_portal')),
]
