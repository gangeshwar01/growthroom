from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

@login_required
@staff_member_required
def dashboard(request):
    # Only superusers can access this dashboard
    if not request.user.is_superuser:
        return redirect(reverse('employee_portal:dashboard'))
    
    return render(request, 'dashboard.html')
    
