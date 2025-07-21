from django import forms
from .models import ProgressLog

class ProgressLogForm(forms.ModelForm):
    class Meta:
        model = ProgressLog
        fields = [
            'title',
            'summary',
            'details',
            'reflection',
            'next_action',
            # Omit creation_date if it's non-editable
        ]
