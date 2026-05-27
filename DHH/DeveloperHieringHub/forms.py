from django import forms

from .models import BetaJoiner, JobPost, PlatformUser


class BetaJoinerForm(forms.ModelForm):
    class Meta:
        model = BetaJoiner
        fields = ['full_name', 'email', 'role', 'company_name', 'github_username', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email Address'}),
            'company_name': forms.TextInput(attrs={'placeholder': 'Company Name'}),
            'github_username': forms.TextInput(attrs={'placeholder': 'GitHub Username'}),
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'What do you want from DHH?'}),
        }


class DeveloperSignupForm(forms.Form):
    full_name = forms.CharField(max_length=160)
    email = forms.EmailField()
    github_username = forms.CharField(max_length=120)
    headline = forms.CharField(max_length=180)
    primary_stack = forms.CharField(max_length=180)
    years_experience = forms.IntegerField(min_value=0, max_value=60)
    portfolio_url = forms.URLField(required=False)
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False)

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if PlatformUser.objects.filter(email=email).exists():
            raise forms.ValidationError('A user with this email already exists.')
        return email


class HirerSignupForm(forms.Form):
    full_name = forms.CharField(max_length=160)
    email = forms.EmailField()
    company_name = forms.CharField(max_length=180)
    company_website = forms.URLField(required=False)
    company_size = forms.CharField(max_length=20, required=False)
    hiring_needs = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False)

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if PlatformUser.objects.filter(email=email).exists():
            raise forms.ValidationError('A user with this email already exists.')
        return email


class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = [
            'title',
            'company_name',
            'location',
            'job_type',
            'salary_range',
            'required_skills',
            'description',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }


class GitHubConnectionForm(forms.Form):
    full_name = forms.CharField(max_length=160)
    email = forms.EmailField()
    github_username = forms.CharField(max_length=120)
    headline = forms.CharField(max_length=180, required=False)

    def clean_email(self):
        return self.cleaned_data['email'].lower()
