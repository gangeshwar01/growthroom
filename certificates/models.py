from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class CertificateRequest(models.Model):
    TYPE_CHOICES = (
        ('welcome', 'Welcome Certificate'),
        ('final', 'Final Internship Certificate'),
    )
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    submission_info = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    criteria_met = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.type} - {self.status}"
