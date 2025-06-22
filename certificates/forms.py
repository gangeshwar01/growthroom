from django import forms
from .models import CertificateRequest

class CertificateRequestForm(forms.ModelForm):
    class Meta:
        model = CertificateRequest
        fields = ['user', 'type', 'submission_info', 'status', 'criteria_met'] 