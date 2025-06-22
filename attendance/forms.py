from django import forms
from .models import AttendanceRecord
from datetime import datetime, date, time # Import necessary for combining
from django.contrib.auth.models import User

class AttendanceForm(forms.ModelForm):
    # These are form-specific fields for time input
    check_in_time = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}))
    check_out_time = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}))

    class Meta:
        model = AttendanceRecord
        # Only include fields that are directly mapped or will be handled by form.save()
        fields = ['user', 'date', 'status', 'notes']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # Set initial values for time fields from DateTimeField instances
        if self.instance and self.instance.check_in:
            self.fields['check_in_time'].initial = self.instance.check_in.time()
        if self.instance and self.instance.check_out:
            self.fields['check_out_time'].initial = self.instance.check_out.time()
        # Restrict user field for non-admin/staff
        if user and not (user.is_superuser or user.is_staff):
            self.fields['user'].queryset = User.objects.filter(pk=user.pk)
            self.fields['user'].initial = user.pk
            self.fields['user'].empty_label = None
            self.fields['user'].disabled = True

    def clean(self):
        cleaned_data = super().clean()
        # Convert empty strings to None for time fields
        if cleaned_data.get('check_in_time') == '':
            cleaned_data['check_in_time'] = None
        if cleaned_data.get('check_out_time') == '':
            cleaned_data['check_out_time'] = None
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Combine date with time fields from the form
        selected_date = self.cleaned_data.get('date')
        cleaned_check_in_time = self.cleaned_data.get('check_in_time')
        cleaned_check_out_time = self.cleaned_data.get('check_out_time')

        print(f"DEBUG: selected_date: {selected_date}, type: {type(selected_date)}")
        print(f"DEBUG: cleaned_check_in_time: {cleaned_check_in_time}, type: {type(cleaned_check_in_time)}")
        print(f"DEBUG: cleaned_check_out_time: {cleaned_check_out_time}, type: {type(cleaned_check_out_time)}")

        if selected_date and cleaned_check_in_time:
            instance.check_in = datetime.combine(selected_date, cleaned_check_in_time)
        else:
            instance.check_in = None

        if selected_date and cleaned_check_out_time:
            instance.check_out = datetime.combine(selected_date, cleaned_check_out_time)
        else:
            instance.check_out = None

        if commit:
            instance.save()
        return instance 