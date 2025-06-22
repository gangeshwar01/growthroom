from django import forms
from .models import PerformanceReview
from tasks.models import Task
from django.db.models import Q

class PerformanceReviewForm(forms.ModelForm):
    task = forms.ModelChoiceField(
        queryset=Task.objects.filter(performance_review__isnull=True),
        help_text="Select a task that has not been reviewed yet."
    )

    class Meta:
        model = PerformanceReview
        fields = ['task', 'rating', 'feedback']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 10}),
            'feedback': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # For an existing review, ensure its current task is in the queryset
        if self.instance and self.instance.pk:
            self.fields['task'].queryset = Task.objects.filter(
                Q(performance_review__isnull=True) | Q(pk=self.instance.task.pk)
            ).order_by('title')
        else:
            self.fields['task'].queryset = Task.objects.filter(performance_review__isnull=True).order_by('title')
            
        self.fields['task'].label_from_instance = lambda obj: f"{obj.title} (Assigned to: {obj.assigned_to.username})" 