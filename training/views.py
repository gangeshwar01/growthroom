from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models import Count, Q
from .models import TrainingSession, TrainingAttendance
from .forms import TrainingSessionForm

# Create your views here.

def training_home(request):
    # Filter sessions based on user permissions
    if request.user.is_superuser or request.user.is_staff:
        # Admins see all sessions
        upcoming_sessions = TrainingSession.objects.filter(
            date__gte=timezone.now().date()
        ).order_by('date', 'time')[:5]
        
        upcoming_count = TrainingSession.objects.filter(
            date__gte=timezone.now().date()
        ).count()
        
        total_sessions = TrainingSession.objects.count()
        
        recent_activity = TrainingSession.objects.order_by('-created_at')[:5]
    else:
        # Regular users see only assigned sessions
        upcoming_sessions = TrainingSession.objects.filter(
            date__gte=timezone.now().date(),
            assigned_employees=request.user
        ).order_by('date', 'time')[:5]
        
        upcoming_count = TrainingSession.objects.filter(
            date__gte=timezone.now().date(),
            assigned_employees=request.user
        ).count()
        
        total_sessions = TrainingSession.objects.filter(
            assigned_employees=request.user
        ).count()
        
        recent_activity = TrainingSession.objects.filter(
            assigned_employees=request.user
        ).order_by('-created_at')[:5]
    
    total_attendees = TrainingAttendance.objects.filter(
        attended=True
    ).count()
    
    topics_count = TrainingSession.objects.values('topic').distinct().count()

    context = {
        'upcoming_sessions': upcoming_sessions,
        'upcoming_count': upcoming_count,
        'total_sessions': total_sessions,
        'total_attendees': total_attendees,
        'topics_count': topics_count,
        'recent_activity': recent_activity,
    }
    
    return render(request, 'training/home.html', context)

def session_list(request):
    base_query = TrainingSession.objects.annotate(
        attendees_count=Count('assigned_employees', distinct=True),
        attended_count=Count('trainingattendance', filter=Q(trainingattendance__attended=True))
    )
    if request.user.is_superuser or request.user.is_staff:
        sessions = base_query.all().order_by('-date', '-time')
    else:
        sessions = base_query.filter(
            assigned_employees=request.user
        ).order_by('-date', '-time')
    
    context = {
        'sessions': sessions,
        'today': timezone.now().date(),
    }
    return render(request, 'training/session_list.html', context)

def session_detail(request, pk):
    if request.user.is_superuser or request.user.is_staff:
        session = get_object_or_404(TrainingSession, pk=pk)
    else:
        session = get_object_or_404(TrainingSession, pk=pk, assigned_employees=request.user)
    return render(request, 'training/session_detail.html', {'session': session})

def session_create(request):
    if request.method == 'POST':
        form = TrainingSessionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('training:session_list')
    else:
        form = TrainingSessionForm()
    return render(request, 'training/session_form.html', {'form': form})

def session_update(request, pk):
    session = get_object_or_404(TrainingSession, pk=pk)
    if request.method == 'POST':
        form = TrainingSessionForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            return redirect('training:session_list')
    else:
        form = TrainingSessionForm(instance=session)
    return render(request, 'training/session_form.html', {'form': form})

def session_delete(request, pk):
    session = get_object_or_404(TrainingSession, pk=pk)
    if request.method == 'POST':
        session.delete()
        return redirect('training:session_list')
    return render(request, 'training/session_confirm_delete.html', {'session': session})

def mark_attendance(request, pk):
    session = get_object_or_404(TrainingSession, pk=pk)
    
    # Create or update the attendance record for the current user
    attendance, created = TrainingAttendance.objects.get_or_create(
        user=request.user,
        session=session,
        defaults={'attended': True}
    )
    
    # If the record already existed, make sure it's marked as attended
    if not created and not attendance.attended:
        attendance.attended = True
        attendance.save()

    # Redirect to the meeting link
    return redirect(session.meeting_link)
