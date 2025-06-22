from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from .models import PerformanceReview
from .forms import PerformanceReviewForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.utils import timezone
from datetime import timedelta

@staff_member_required
def performance_home(request):
    """
    Displays a list of all performance reviews for admins/staff.
    """
    reviews = PerformanceReview.objects.select_related('task', 'employee', 'reviewer').all()
    context = {
        'reviews': reviews,
    }
    return render(request, 'performance/home.html', context)

@staff_member_required
def performance_review_create(request):
    if request.method == 'POST':
        form = PerformanceReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.employee = review.task.assigned_to
            review.save()
            messages.success(request, f"Review for '{review.task.title}' has been successfully created.")
            return redirect('performance:performance_home')
    else:
        form = PerformanceReviewForm()
    
    context = {
        'form': form,
    }
    return render(request, 'performance/performance_form.html', context)

@staff_member_required
def performance_review_update(request, pk):
    review = get_object_or_404(PerformanceReview, pk=pk)
    if request.method == 'POST':
        form = PerformanceReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save() # Reviewer and employee are already set, no need to change on update
            messages.success(request, 'Performance review has been updated.')
            return redirect('performance:performance_home')
    else:
        form = PerformanceReviewForm(instance=review)
    
    context = {
        'form': form,
        'form_title': 'Edit Performance Review'
    }
    return render(request, 'performance/performance_form.html', context)

@staff_member_required
def performance_review_delete(request, pk):
    review = get_object_or_404(PerformanceReview, pk=pk)
    if request.method == 'POST':
        review.delete()
        messages.success(request, f'The review for "{review.task.title}" has been deleted.')
        return redirect('performance:performance_home')
    
    context = {
        'review': review,
    }
    return render(request, 'performance/performance_review_confirm_delete.html', context)

@login_required
def my_performance(request):
    """
    Displays performance reviews and analytics for the logged-in user.
    """
    user = request.user
    
    # --- Performance Analytics ---
    today = timezone.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    start_of_month = today.replace(day=1)

    reviews = PerformanceReview.objects.filter(employee=user)

    weekly_avg = reviews.filter(review_date__date__gte=start_of_week).aggregate(avg_rating=Avg('rating'))['avg_rating']
    monthly_avg = reviews.filter(review_date__date__gte=start_of_month).aggregate(avg_rating=Avg('rating'))['avg_rating']

    context = {
        'performance_reviews': reviews,
        'weekly_performance': weekly_avg,
        'monthly_performance': monthly_avg,
    }
    return render(request, 'performance/my_performance.html', context)
