from django import forms
from .models import Lake, LakePhoto


class LakeForm(forms.ModelForm):
    class Meta:
        model = Lake
        fields = ['name', 'location', 'description', 'ecology_info',
                  'current_status', 'cleanup_needs', 'area_sq_km', 'pollution_level']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'ecology_info': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'current_status': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'cleanup_needs': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'area_sq_km': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'pollution_level': forms.Select(attrs={'class': 'form-select'}),
        }


class LakePhotoForm(forms.ModelForm):
    class Meta:
        model = LakePhoto
        fields = ['image', 'image_url', 'caption', 'photo_type']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control',
                                               'placeholder': 'https://example.com/photo.jpg'}),
            'caption': forms.TextInput(attrs={'class': 'form-control'}),
            'photo_type': forms.Select(attrs={'class': 'form-select'}),
        }
