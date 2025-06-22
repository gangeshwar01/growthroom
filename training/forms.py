from django import forms
from .models import TrainingSession

class TrainingSessionForm(forms.ModelForm):
    class Meta:
        model = TrainingSession
        fields = ['title', 'description', 'date', 'time', 'meeting_link', 'topic', 'resources', 'assigned_employees'] 