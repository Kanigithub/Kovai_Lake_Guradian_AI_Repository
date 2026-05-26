from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile


class VolunteerRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class NGORegistrationForm(UserCreationForm):
    # Contact person
    first_name = forms.CharField(max_length=30, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact person first name'}))
    last_name = forms.CharField(max_length=30, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact person last name'}))
    email = forms.EmailField(required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Official email address'}))
    # Organization
    organization_name = forms.CharField(max_length=200, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Green Earth Foundation'}))
    organization_type = forms.ChoiceField(choices=[], required=True,
        widget=forms.Select(attrs={'class': 'form-select'}))
    organization_size = forms.IntegerField(required=True, min_value=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Number of members (min. 2)'}))
    organization_website = forms.URLField(required=False,
        widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://yourorg.org (optional)'}))
    organization_description = forms.CharField(required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3,
                                     'placeholder': 'Brief description of your NGO / group mission'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        from .models import UserProfile
        super().__init__(*args, **kwargs)
        self.fields['organization_type'].choices = UserProfile.ORG_TYPES
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data.get('last_name', '')
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'bio', 'availability_weekdays', 'availability_weekends', 'skills', 'profile_picture']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+91 98765 43210'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'skills': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Swimming, First Aid, Photography'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
