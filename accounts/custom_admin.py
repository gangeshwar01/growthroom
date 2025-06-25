from django.contrib.admin import AdminSite
from accounts.forms import StaffAuthenticationForm
from django.utils.translation import gettext_lazy as _

# Import all models
from accounts.models import ProfileIssue, Profile
from attendance.models import Attendance
from training.models import TrainingSession
from tasks.models import Task, Project
from performance.models import PerformanceReview
from certificates.models import Certificate
from employee_portal.models import EmployeeTask

class MyAdminSite(AdminSite):
    site_header = _("Django administration")
    login_form = StaffAuthenticationForm

custom_admin_site = MyAdminSite(name='custom_admin')

# Register models from accounts app
custom_admin_site.register(ProfileIssue)
custom_admin_site.register(Profile)

# Register models from attendance app
custom_admin_site.register(Attendance)

# Register models from training app
custom_admin_site.register(TrainingSession)

# Register models from tasks app
custom_admin_site.register(Task)
custom_admin_site.register(Project)

# Register models from performance app
custom_admin_site.register(PerformanceReview)

# Register models from certificates app
custom_admin_site.register(Certificate)

# Register models from employee_portal app
custom_admin_site.register(EmployeeTask) 