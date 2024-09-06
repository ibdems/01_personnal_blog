from django import forms
from article.models import Article, Category, Profile, Tag
from django.contrib.auth.models import User

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'description')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

class ArticleForm(forms.ModelForm):

    new_tags = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Sport, messi, ronaldo'}),
        label='Tags (Separes par des virgules)'
    )
    class Meta:
        model = Article
        fields = ('category', 'title', 'summary', 'content', 'date_published', 'image', 'new_tags')
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'summary': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'date_published': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',
                attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', }),
        }


class UpdateUser(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = ''

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, min_length=3, required=True)
    password = forms.CharField(max_length=50, min_length=3, required=True)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio',  'photo', 'tel', 'link_facebook', 'link_instagram', 'link_linkedin', 'adresse')
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'tel': forms.TextInput(attrs={'class': 'form-control'}),
            'link_facebook': forms.URLInput(attrs={'class': 'form-control'}),
            'link_instagram': forms.URLInput(attrs={'class': 'form-control'}),
            'link_linkedin': forms.URLInput(attrs={'class': 'form-control'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control'}),
        }
