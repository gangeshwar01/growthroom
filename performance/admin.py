from django.contrib import admin
from .models import PerformanceReview

@admin.register(PerformanceReview)
class PerformanceReviewAdmin(admin.ModelAdmin):
    list_display = ('task', 'employee', 'rating', 'review_date', 'reviewer')
    list_filter = ('rating', 'employee')
    search_fields = ('task__title', 'employee__username')
    autocomplete_fields = ('task',)
    readonly_fields = ('employee', 'review_date')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.reviewer = request.user
        if obj.task:
            obj.employee = obj.task.assigned_to
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj is None:
            # For new reviews, limit task choices to those without a review yet
            form.base_fields['task'].queryset = form.base_fields['task'].queryset.filter(performance_review__isnull=True)
        return form
