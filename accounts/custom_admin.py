from django.contrib.admin import AdminSite
from accounts.forms import StaffAuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import ProfileIssue

class MyAdminSite(AdminSite):
    site_header = _("Django administration")
    login_form = StaffAuthenticationForm

custom_admin_site = MyAdminSite(name='custom_admin')

# Register your models here
custom_admin_site.register(ProfileIssue) 