from django import forms
from .models import Note, Tag


class NoteForm(forms.ModelForm):

    class Meta:
        model = Note
        fields = ['title', 'body']

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Note Title'}),
            'body': forms.Textarea( attrs={'placeholder': 'Write stuff here'}),
        }


class TagForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = ['name']
