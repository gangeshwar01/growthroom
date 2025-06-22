from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class TrainingSession(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    meeting_link = models.URLField()
    topic = models.CharField(max_length=200)
    resources = models.TextField(blank=True)
    assigned_employees = models.ManyToManyField(User, blank=True, related_name='assigned_training_sessions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class TrainingAttendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(TrainingSession, on_delete=models.CASCADE)
    attended = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.session.title} - {'Attended' if self.attended else 'Not Attended'}"
