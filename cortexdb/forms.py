# cortexdb/forms.py

from django import forms
from cortexdb.models import Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
        labels = {
            'title': 'Note Title',
            'content': 'Note Content',
        }
        help_texts = {
            'title': 'Enter a title that is descriptive and concise',
            'content': 'Enter the content of your note. Think about capturing the essence of the idea and adhering to the principles of atomicity and clarity.',
        }