from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile, ProfileIssue
from django.contrib.auth import authenticate

class ProfileForm(forms.ModelForm):
    bio = forms.CharField(label="Name", required=False, widget=forms.TextInput(attrs={'placeholder': 'Full Name'}))
    class Meta:
        model = Profile
        fields = ['user', 'employee_id', 'role', 'bio', 'location', 'birth_date']

class UserProfileCreationForm(UserCreationForm):
    employee_id = forms.CharField(max_length=50, required=True, label='Employee ID')
    role = forms.CharField(max_length=100, required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    location = forms.CharField(max_length=100, required=False)
    birth_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'employee_id', 'role', 'bio', 'location', 'birth_date')

    def save(self, commit=True):
        user = super().save(commit=commit)
        profile = Profile.objects.create(
            user=user,
            employee_id=self.cleaned_data['employee_id'],
            role=self.cleaned_data.get('role', ''),
            bio=self.cleaned_data.get('bio', ''),
            location=self.cleaned_data.get('location', ''),
            birth_date=self.cleaned_data.get('birth_date', None),
        )
        return user

class ProfileIssueForm(forms.ModelForm):
    description = forms.CharField(
        label="Describe the issue",
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe the mistake in your profile...'}),
        required=True
    )
    class Meta:
        model = ProfileIssue
        fields = ['description']

class StaffAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active or not user.is_staff:
            raise forms.ValidationError(
                "Invalid username or password.",
                code='invalid_login',
            ) 