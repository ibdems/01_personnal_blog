from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

class Profile(models.Model):
    choice_role = [
        ('Editeur', 'Editeur'),
        ('Admin', 'Administrateur'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    role= models.CharField(max_length=10, choices=choice_role, default='Editeur')
    photo = models.ImageField(blank=True, null=True, upload_to='photos_user', max_length=255)
    tel = models.IntegerField(null=True, blank=True)
    link_facebook = models.URLField(null=True, blank=True, max_length=255)
    link_instagram = models.URLField(null=True, blank=True, max_length=255)
    link_linkedin = models.URLField(null=True, blank=True, max_length=255)
    adresse = models.CharField(max_length=100,blank=True, null=True)


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    user = models.ForeignKey(User, related_name='tags',blank=True, null=True, default=1, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Article(models.Model):
    user = models.ForeignKey(User, related_name='articles',blank=True, null=True, default=1, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    summary = models.CharField(max_length=200)
    content = RichTextField()
    date_published = models.DateTimeField(blank=True, default=timezone.now)
    image = models.ImageField(upload_to='images_article/', max_length=255, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)

class Comment(models.Model):
    name = models.CharField(max_length=100)
    comment = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

class Message(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True,blank=True)



    

