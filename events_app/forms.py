from django import forms
from .models import Event, EventRole, EventRegistration


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'lake', 'location', 'date', 'start_time',
                  'end_time', 'required_materials', 'max_volunteers', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'lake': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'required_materials': forms.Textarea(attrs={'class': 'form-control', 'rows': 3,
                                                        'placeholder': 'e.g.\nGloves\nTrash bags\nWater bottle'}),
            'max_volunteers': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class EventRoleForm(forms.ModelForm):
    class Meta:
        model = EventRole
        fields = ['name', 'description', 'max_volunteers']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'max_volunteers': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class EventRegistrationForm(forms.ModelForm):
    class Meta:
        model = EventRegistration
        fields = ['role']
        widgets = {
            'role': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, event, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].queryset = EventRole.objects.filter(event=event)
        self.fields['role'].required = False
        self.fields['role'].empty_label = "No specific role"
