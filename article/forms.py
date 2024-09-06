from django import forms
from .models import Comment, Message

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'comment')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom*'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Votre commentaire*'}),
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('name', 'email', 'subject', 'content',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Votre email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Le sujet'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Le contenue de votre message', 'rows': 4}),
        }
        