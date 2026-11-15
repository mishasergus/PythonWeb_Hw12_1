from django import forms
from Shared_models.models import Measure

class MeasureForm(forms.ModelForm):
    class Meta:
        model = Measure
        fields = [
            'name',
            'description',
            'price',
            'start_time',
            'end_time',
            'img_url',
            'is_active'
        ]
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'img_url': forms.TextInput(attrs={'class': 'form-control'}),
        }