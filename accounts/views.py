from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import Profile, ProfileIssue
from .forms import ProfileForm, UserProfileCreationForm, ProfileIssueForm

# Create your views here.

def accounts_home(request):
    # Get total number of employees
    total_employees = User.objects.count()
    
    # Get active profiles (profiles updated in the last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    active_profiles = Profile.objects.filter(updated_at__gte=thirty_days_ago).count()
    
    # Get new profiles this month
    new_this_month = Profile.objects.filter(created_at__month=timezone.now().month).count()
    
    # Get recent activities (profile updates)
    recent_activities = Profile.objects.order_by('-updated_at')[:5]
    
    context = {
        'total_employees': total_employees,
        'active_profiles': active_profiles,
        'new_this_month': new_this_month,
        'recent_activities': recent_activities,
    }
    return render(request, 'accounts/home.html', context)

def profile_list(request):
    profiles = Profile.objects.all()
    return render(request, 'accounts/profile_list.html', {'profiles': profiles})

@login_required
def profile_detail(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    issue_form = None
    issue_submitted = False
    profile_issues = None
    open_issues_count = 0
    if request.user.is_superuser or request.user.is_staff:
        profile_issues = profile.issues.all().order_by('-created_at')
        open_issues_count = profile.issues.filter(status='open').count()
        # Handle resolving an issue
        if request.method == 'POST' and request.POST.get('resolve_issue_id'):
            issue_id = request.POST.get('resolve_issue_id')
            issue = profile.issues.filter(id=issue_id).first()
            if issue and issue.status == 'open':
                issue.status = 'resolved'
                issue.save()
        # Handle deleting an issue
        if request.method == 'POST' and request.POST.get('delete_issue_id'):
            issue_id = request.POST.get('delete_issue_id')
            issue = profile.issues.filter(id=issue_id).first()
            if issue:
                issue.delete()
    if request.user == profile.user:
        if request.method == 'POST' and 'raise_issue' in request.POST:
            issue_form = ProfileIssueForm(request.POST)
            if issue_form.is_valid():
                issue = issue_form.save(commit=False)
                issue.profile = profile
                issue.save()
                issue_submitted = True
        else:
            issue_form = ProfileIssueForm()
    return render(request, 'accounts/profile_detail.html', {
        'profile': profile,
        'issue_form': issue_form,
        'issue_submitted': issue_submitted,
        'profile_issues': profile_issues,
        'open_issues_count': open_issues_count,
    })

def profile_create(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile_list')
    else:
        form = ProfileForm()
    return render(request, 'accounts/profile_form.html', {'form': form})

def profile_update(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile_list')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'accounts/profile_form.html', {'form': form})

def profile_delete(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    if request.method == 'POST':
        profile.delete()
        return redirect('accounts:profile_list')
    return render(request, 'accounts/profile_confirm_delete.html', {'profile': profile})

def login_view(request):
    # Clear any existing messages when first loading the login page
    if request.method == 'GET':
        storage = messages.get_messages(request)
        storage.used = True
        return render(request, 'accounts/login.html')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html')

def logout_view(request):
    # Clear all session data
    request.session.flush()
    # Clear the session cookie
    if request.session.session_key:
        request.session.delete()
    # Logout the user
    logout(request)
    # Clear all messages before adding the logout message
    storage = messages.get_messages(request)
    for _ in storage:
        pass  # This iterates and clears all messages
    messages.success(request, 'Successfully logged out.')
    return redirect('accounts:accounts_login')

def register_employee(request):
    if request.method == 'POST':
        form = UserProfileCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee created successfully!')
            return redirect('accounts:profile_list')
    else:
        form = UserProfileCreationForm()
    return render(request, 'accounts/register_employee.html', {'form': form})
