from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from tasks.models import Task

# Create your models here.

class PerformanceReview(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE, related_name='performance_review')
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='given_reviews')
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='performance_reviews')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    feedback = models.TextField()
    review_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-review_date']
        unique_together = ('task', 'employee')

    def __str__(self):
        return f"Review for {self.task.title} by {self.employee.username}"
