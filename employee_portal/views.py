from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.models import Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from tasks.models import Task, Project
from functools import wraps
from attendance.models import AttendanceRecord
from training.models import TrainingSession
from performance.models import PerformanceReview
from django.db.models import Avg
from django.utils import timezone
from datetime import timedelta

def employee_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if 'employee_id' not in request.session:
            messages.error(request, 'Please login to access this page')
            return redirect('employee_portal:login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def employee_login(request):
    if 'employee_id' in request.session:
        return redirect('employee_portal:emp_dashboard')
        
    if request.method == 'POST':
        employee_id_or_username = request.POST.get('employee_id')
        password = request.POST.get('password')
        print(f"Trying login: employee_id_or_username={employee_id_or_username}, password={password}")

        if not employee_id_or_username or not password:
            messages.error(request, 'Please enter both employee ID/username and password')
            return render(request, 'employee_portal/login.html')
        
        # Try to find by employee_id first
        profile = Profile.objects.filter(employee_id=employee_id_or_username).first()
        user = None
        if profile:
            user = profile.user
        else:
            # Try to find by username
            user = User.objects.filter(username=employee_id_or_username).first()
            if user:

                # Try to get profile for session
                profile = Profile.objects.filter(user=user).first()
        if user:
            user_auth = authenticate(request, username=user.username, password=password)
            if user_auth is not None:
                login(request, user_auth)
                if profile:
                    request.session['employee_id'] = profile.id
                return redirect('employee_portal:emp_dashboard')
        messages.error(request, 'Invalid employee ID/username or password')
    
    return render(request, 'employee_portal/login.html')

@employee_login_required
def employee_dashboard(request):
    try:
        profile = Profile.objects.get(id=request.session.get('employee_id'))
        user = profile.user
        
        # --- Performance Analytics ---
        today = timezone.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        start_of_month = today.replace(day=1)

        # Fetch all reviews for the user
        reviews = PerformanceReview.objects.filter(employee=user)

        # Calculate weekly average
        weekly_avg = reviews.filter(review_date__date__gte=start_of_week).aggregate(avg_rating=Avg('rating'))['avg_rating']
        
        # Calculate monthly average
        monthly_avg = reviews.filter(review_date__date__gte=start_of_month).aggregate(avg_rating=Avg('rating'))['avg_rating']

        # --- Quick Stats ---
        tasks = Task.objects.filter(assigned_to=user)
        pending_tasks_count = tasks.filter(status='pending').count()
        
        projects = Project.objects.filter(task__assigned_to=user).distinct()
        total_projects_count = projects.count()

        attendance_records = AttendanceRecord.objects.filter(user=user).order_by('-date')[:5] # Last 5 records
        training_sessions = TrainingSession.objects.filter(assigned_employees=user).order_by('date', 'time')
        
        context = {
            'profile': profile,
            'tasks': tasks,
            'projects': projects,
            'attendance_records': attendance_records,
            'training_sessions': training_sessions,
            'performance_reviews': reviews.order_by('-review_date')[:3], # Most recent 3 reviews
            'weekly_performance': weekly_avg,
            'monthly_performance': monthly_avg,
            'pending_tasks_count': pending_tasks_count,
            'active_projects_count': total_projects_count,
        }
        return render(request, 'employee_portal/dashboard.html', context)
    except Profile.DoesNotExist:
        messages.error(request, 'Employee profile not found')
        return redirect('employee_portal:login')

# Optional: If you have separate task/project list pages for employees, use similar filtering:
@employee_login_required
def employee_task_list(request):
    profile = Profile.objects.get(id=request.session.get('employee_id'))
    tasks = Task.objects.filter(assigned_to=profile.user)
    return render(request, 'employee_portal/task_list.html', {'tasks': tasks})

@employee_login_required
def employee_project_list(request):
    profile = Profile.objects.get(id=request.session.get('employee_id'))
    projects = Project.objects.filter(task__assigned_to=profile.user).distinct()
    return render(request, 'employee_portal/project_list.html', {'projects': projects})

def employee_logout(request):
    logout(request)
    return redirect('employee_portal:login')
