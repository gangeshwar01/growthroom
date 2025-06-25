from django.contrib import admin
from .models import ProfileIssue
from accounts.forms import StaffAuthenticationForm
from django.contrib.admin import AdminSite

class MyAdminSite(AdminSite):
    login_form = StaffAuthenticationForm

admin.site.__class__ = MyAdminSite

# Register your models here.
admin.site.register(ProfileIssue)
