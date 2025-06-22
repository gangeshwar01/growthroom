from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models import Count, Q
from .models import Project, Task, Comment
from .forms import ProjectForm, TaskForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.

def tasks_home(request):
    # Get active projects count
    active_projects_count = Project.objects.filter(
        end_date__gte=timezone.now().date()
    ).count()
    
    # Get task counts by status
    completed_tasks_count = Task.objects.filter(status='completed').count()
    pending_tasks_count = Task.objects.filter(status='pending').count()
    in_progress_tasks_count = Task.objects.filter(status='in_progress').count()
    
    # Get help needed count
    help_needed_count = Task.objects.filter(help_needed=True).count()
    
    # Get recent tasks
    recent_tasks = Task.objects.select_related(
        'assigned_to', 'project'
    ).order_by('-created_at')[:5]

    context = {
        'active_projects_count': active_projects_count,
        'completed_tasks_count': completed_tasks_count,
        'pending_tasks_count': pending_tasks_count,
        'in_progress_tasks_count': in_progress_tasks_count,
        'help_needed_count': help_needed_count,
        'recent_tasks': recent_tasks,
    }
    
    return render(request, 'tasks/home.html', context)

@login_required
def project_list(request):
    if request.user.is_superuser or request.user.is_staff:
        projects = Project.objects.annotate(
            total_tasks_count=Count('task'),
            completed_tasks_count=Count('task', filter=Q(task__status='completed')),
            team_members_count=Count('task__assigned_to', distinct=True)
        ).order_by('-created_at')
    else:
        projects = Project.objects.filter(task__assigned_to=request.user).distinct().annotate(
            total_tasks_count=Count('task'),
            completed_tasks_count=Count('task', filter=Q(task__status='completed')),
            team_members_count=Count('task__assigned_to', distinct=True)
        ).order_by('-created_at')

    for project in projects:
        if project.total_tasks_count > 0:
            project.progress_percentage = (project.completed_tasks_count / project.total_tasks_count) * 100
        else:
            project.progress_percentage = 0

    context = {
        'projects': projects,
    }
    return render(request, 'tasks/project_list.html', context)

@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    tasks = Task.objects.filter(project=project).select_related('assigned_to').order_by('-created_at')
    
    # Get task counts by status
    completed_tasks_count = tasks.filter(status='completed').count()
    in_progress_tasks_count = tasks.filter(status='in_progress').count()
    pending_tasks_count = tasks.filter(status='pending').count()
    total_tasks_count = tasks.count()
    
    # Calculate progress percentage
    if total_tasks_count > 0:
        progress_percentage = (completed_tasks_count / total_tasks_count) * 100
    else:
        progress_percentage = 0
    
    # Get team members with task counts
    team_members = User.objects.filter(
        task__project=project
    ).annotate(
        tasks_count=Count('task', filter=Q(task__project=project))
    ).distinct()
    
    context = {
        'project': project,
        'tasks': tasks,
        'completed_tasks_count': completed_tasks_count,
        'in_progress_tasks_count': in_progress_tasks_count,
        'pending_tasks_count': pending_tasks_count,
        'total_tasks_count': total_tasks_count,
        'progress_percentage': progress_percentage,
        'team_members': team_members,
    }
    return render(request, 'tasks/project_detail.html', context)

def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasks:project_list')
    else:
        form = ProjectForm()
    return render(request, 'tasks/project_form.html', {'form': form})

def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('tasks:project_list')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'tasks/project_form.html', {'form': form})

def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('tasks:project_list')
    return render(request, 'tasks/project_confirm_delete.html', {'project': project})

@login_required
def task_list(request):
    if request.user.is_superuser or request.user.is_staff:
        tasks = Task.objects.select_related('project', 'assigned_to').order_by('-created_at')
    else:
        tasks = Task.objects.filter(assigned_to=request.user).select_related('project', 'assigned_to').order_by('-created_at')
    completed_count = tasks.filter(status='completed').count()
    in_progress_count = tasks.filter(status='in_progress').count()
    pending_count = tasks.filter(status='pending').count()
    
    context = {
        'tasks': tasks,
        'completed_count': completed_count,
        'in_progress_count': in_progress_count,
        'pending_count': pending_count,
        'total_count': tasks.count()
    }
    return render(request, 'tasks/task_list.html', context)

@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    comments = task.comments.all().select_related('user').order_by('-created_at')
    return render(request, 'tasks/task_detail.html', {
        'task': task,
        'comments': comments
    })

@login_required
def task_create(request):
    from django.contrib.auth.models import User
    if request.method == 'POST':
        form = TaskForm(request.POST)
        form.fields['assigned_to'].queryset = User.objects.all()
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            messages.success(request, 'Task created successfully.')
            return redirect('tasks:task_detail', pk=task.pk)
    else:
        form = TaskForm()
        form.fields['assigned_to'].queryset = User.objects.all()
    context = {
        'form': form,
        'projects': Project.objects.all(),
        'users': User.objects.all()
    }
    return render(request, 'tasks/task_form.html', context)

@login_required
def task_update(request, pk):
    from django.contrib.auth.models import User
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        form.fields['assigned_to'].queryset = User.objects.all()
        if form.is_valid():
            task = form.save()
            messages.success(request, 'Task updated successfully.')
            return redirect('tasks:task_detail', pk=task.pk)
    else:
        form = TaskForm(instance=task)
        form.fields['assigned_to'].queryset = User.objects.all()
    context = {
        'form': form,
        'task': task,
        'projects': Project.objects.all(),
        'users': User.objects.all()
    }
    return render(request, 'tasks/task_form.html', context)

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully.')
        return redirect('tasks:task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})

@login_required
def task_add_comment(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(
                task=task,
                user=request.user,
                content=content
            )
            messages.success(request, 'Comment added successfully.')
        else:
            messages.error(request, 'Comment cannot be empty.')
    return redirect('tasks:task_detail', pk=task.pk)

@login_required
def task_mark_complete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.status = 'completed'
    task.save()
    messages.success(request, 'Task marked as completed.')
    return redirect('task_detail', pk=task.pk)

@login_required
def task_mark_in_progress(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.status = 'in_progress'
    task.save()
    messages.success(request, 'Task marked as in progress.')
    return redirect('task_detail', pk=task.pk)

@login_required
def task_mark_pending(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.status = 'pending'
    task.save()
    messages.success(request, 'Task marked as pending.')
    return redirect('task_detail', pk=task.pk)
