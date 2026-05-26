from django import forms
from .models import Announcement, Message
from events_app.models import Event
from volunteers_app.models import Badge


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'event', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'event': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['event'].queryset = Event.objects.all().order_by('-date')
        self.fields['event'].required = False
        self.fields['event'].empty_label = "Not linked to an event"


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['event', 'subject', 'content']
        widgets = {
            'event': forms.Select(attrs={'class': 'form-select'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['event'].queryset = Event.objects.all().order_by('-date')
        self.fields['event'].required = False
        self.fields['event'].empty_label = "General message (not event-specific)"


class BadgeForm(forms.ModelForm):
    class Meta:
        model = Badge
        fields = ['name', 'description', 'icon', 'min_points']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Silver Guardian'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3,
                                                  'placeholder': 'Short description of this badge'}),
            'icon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. fas fa-star'}),
            'min_points': forms.NumberInput(attrs={'class': 'form-control', 'min': 0,
                                                   'placeholder': 'Leave blank for manual-only'}),
        }
        labels = {
            'min_points': 'Auto-Award Points Threshold',
        }
        help_texts = {
            'icon': 'Font Awesome class, e.g. <code>fas fa-star</code>',
            'min_points': 'Badge is automatically awarded when a volunteer reaches this score. '
                          'Leave blank to award manually only.',
        }
