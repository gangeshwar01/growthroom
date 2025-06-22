from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta, datetime
from .models import AttendanceRecord
from .forms import AttendanceForm
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def attendance_home(request):
    today = timezone.now().date()
    user = request.user
    is_admin = user.is_superuser or user.is_staff

    # Filter by user for non-admin/staff
    user_filter = {} if is_admin else {'user': user}

    # Get today's statistics
    present_today = AttendanceRecord.objects.filter(date=today, status='present', **user_filter).count()
    remote_today = AttendanceRecord.objects.filter(date=today, status='remote', **user_filter).count()
    absent_today = AttendanceRecord.objects.filter(date=today, status='absent', **user_filter).count()
    total_employees = User.objects.count() if is_admin else 1

    # Get today's records
    today_records = AttendanceRecord.objects.filter(date=today, **user_filter).select_related('user')

    # Get monthly statistics
    first_day_of_month = today.replace(day=1)
    monthly_stats = {
        'present': int(AttendanceRecord.objects.filter(date__gte=first_day_of_month, status='present', **user_filter).count()),
        'remote': int(AttendanceRecord.objects.filter(date__gte=first_day_of_month, status='remote', **user_filter).count()),
        'absent': int(AttendanceRecord.objects.filter(date__gte=first_day_of_month, status='absent', **user_filter).count()),
    }
    # Ensure keys are strings and values are always integers
    monthly_stats = {str(k): int(v) for k, v in monthly_stats.items()}

    # Prepare data for the chart
    days_in_month = (today.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
    days = range(1, days_in_month.day + 1)

    monthly_labels = [str(day) for day in days]
    monthly_present = []
    monthly_remote = []
    monthly_absent = []

    for day in days:
        date_obj = today.replace(day=day)
        monthly_present.append(AttendanceRecord.objects.filter(date=date_obj, status='present', **user_filter).count())
        monthly_remote.append(AttendanceRecord.objects.filter(date=date_obj, status='remote', **user_filter).count())
        monthly_absent.append(AttendanceRecord.objects.filter(date=date_obj, status='absent', **user_filter).count())

    # Calculate number of days with at least one present/remote/absent record for the user in the month
    present_days = AttendanceRecord.objects.filter(date__gte=first_day_of_month, status='present', **user_filter).values('date').distinct().count()
    remote_days = AttendanceRecord.objects.filter(date__gte=first_day_of_month, status='remote', **user_filter).values('date').distinct().count()
    absent_days = AttendanceRecord.objects.filter(date__gte=first_day_of_month, status='absent', **user_filter).values('date').distinct().count()

    context = {
        'present_today': present_today,
        'remote_today': remote_today,
        'absent_today': absent_today,
        'total_employees': total_employees,
        'today_records': today_records,
        'monthly_stats': monthly_stats,
        'monthly_labels': monthly_labels,
        'monthly_present': monthly_present,
        'monthly_remote': monthly_remote,
        'monthly_absent': monthly_absent,
        'present_days': present_days,
        'remote_days': remote_days,
        'absent_days': absent_days,
    }
    return render(request, 'attendance/home.html', context)

def attendance_list(request):
    users = User.objects.all().order_by('username')
    selected_user_id = request.GET.get('user_id')
    if request.user.is_superuser or request.user.is_staff:
        if selected_user_id:
            records = AttendanceRecord.objects.filter(user_id=selected_user_id).select_related('user').order_by('-date', '-check_in')
        else:
        records = AttendanceRecord.objects.all().select_related('user').order_by('-date', '-check_in')
    else:
        records = AttendanceRecord.objects.filter(user=request.user).order_by('-date', '-check_in')
    
    # Calculate per-employee present and absent counts (only for admin/staff)
    employee_stats = {}
    if request.user.is_superuser or request.user.is_staff:
        for user in users:
            present_count = AttendanceRecord.objects.filter(user=user, status='present').count()
            absent_count = AttendanceRecord.objects.filter(user=user, status='absent').count()
            employee_stats[user.pk] = {
                'present': present_count,
                'absent': absent_count,
            }

    context = {
        'records': records,
        'employee_stats': employee_stats,
        'users': users,
        'selected_user_id': selected_user_id,
    }
    return render(request, 'attendance/attendance_list.html', context)

def attendance_detail(request, pk):
    record = get_object_or_404(AttendanceRecord.objects.select_related('user'), pk=pk)
    return render(request, 'attendance/attendance_detail.html', {'record': record})

def attendance_create(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('attendance:attendance_list')
    else:
        form = AttendanceForm(user=request.user)
    return render(request, 'attendance/attendance_form.html', {'form': form})

def attendance_update(request, pk):
    record = get_object_or_404(AttendanceRecord, pk=pk)
    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('attendance:attendance_list')
    else:
        form = AttendanceForm(instance=record)
    return render(request, 'attendance/attendance_form.html', {'form': form})

def attendance_delete(request, pk):
    record = get_object_or_404(AttendanceRecord, pk=pk)
    if request.method == 'POST':
        record.delete()
        return redirect('attendance:attendance_list')
    return render(request, 'attendance/attendance_confirm_delete.html', {'record': record})
