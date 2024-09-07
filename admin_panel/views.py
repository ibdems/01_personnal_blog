from collections.abc import Sequence
from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView, DetailView
from django.db.models import Prefetch
from django.contrib import messages
from admin_panel.forms import ArticleForm, CategoryForm, LoginForm, ProfileForm, RegistrationForm, UpdateUser
from article.forms import CommentForm
from article.models import Article, Category, Comment, Message, Profile, Tag
# Create your views here.
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['number_article'] = Article.objects.filter(user = self.request.user).count()
        context['number_comment_dont_approved'] = Comment.objects.filter(is_approved=False, article__user = self.request.user).count()
        context['number_message'] = Message.objects.all().count()
        context['number_category'] = Category.objects.all().count()
        return context
    

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/add_categorie.html'
    success_url = reverse_lazy('category_list')

class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'category/list_categorie.html'
    context_object_name = 'categories'  

class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/add_categorie.html'
    success_url = reverse_lazy('category_list')

class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('category_list')

class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'article/list_article.html'
    context_object_name = 'articles'
    paginate_by = 5

    def get_ordering(self) -> Sequence[str]:
        response = super().get_ordering()
        return ['-date_published']
    
    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset()
        return queryset.filter(user = self.request.user)

class ArticleDetailsView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = 'article/detail_article.html'
    context_object_name = 'article' 

    # def get_template_names(self) -> list[str]:
    #     url_previews_page = self.request.META.get('HTTP_REFERER', '')
    #     if 'panel' in url_previews_page and url_previews_page:
    #         return 'article/detail_article.html'
    #     return 'article/singlePost.html'
    
    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset()
        return queryset.prefetch_related(
            Prefetch(
                'comment_set',
                queryset=Comment.objects.filter(is_approved=True)
            )
        )

    
    
class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'article/add_article.html'
    success_url = reverse_lazy('article_list')

    def form_valid(self, form):
        response = super().form_valid(form)

        tags = form.instance.tag.all()
        new_tags = form.cleaned_data['new_tags']

        if new_tags:
            tag_names = [tag.strip() for tag in new_tags.split(',')]
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                tags |= Tag.objects.filter(name=tag_name)

        self.object.tag.set(tags)
        return response

class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'article/add_article.html'

    def get_success_url(self) -> str:
        return reverse_lazy('article_details', kwargs={'pk': self.object.pk})

class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('article_list')

class CommentaireListView(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'commentaire/list_commentaire.html'
    context_object_name = 'commentaires'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_approved=False, article__user = self.request.user)
    
    def get_ordering(self) -> Sequence[str]:
        return ['-created_at']


def approved_commentaire(request, id):
    if request.method == 'POST':
        commentaire = get_object_or_404(Comment, id=id)
        commentaire.is_approved = True
        commentaire.save()
        messages.success(request, "Commentaire approuvé avec succès.")
        return redirect('commentaire_list')
    else:
        messages.error(request, "Méthode non autorisée.")
        return redirect('commentaire_list')


class CommentaireDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    success_url = reverse_lazy('commentaire_list')

class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'message/list_message.html'
    context_object_name ='messages'

    def get_ordering(self) -> Sequence[str]:
        return ['-created_at']


def signin (request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('dashboard'))
            else:
                messages.error(request, "L'utilisateur saisi n'existe pas")
                return redirect(reverse('signin'))
        else:
            print(form.errors)
            return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def signout(request):
    logout(request)
    return redirect(reverse('index'))

def registration (request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user = User.objects.create_user(
                username=cleaned_data.get('username'),
                email=cleaned_data.get('email'),
                password=cleaned_data.get('password'),
                last_name=cleaned_data.get('last_name'),
                first_name=cleaned_data.get('first_name')
            )
            user.save()
            return redirect(reverse('signin'))
        else :
            print(form.errors)
            return render(request, 'register.html', {'form': form})
    else:
        form = RegistrationForm()
     
    return render(request, 'register.html', {'form': form})

class ProfileView(LoginRequiredMixin,DetailView):
    model = Profile
    template_name = 'profile.html'
    context_object_name = 'profile'

    def get_object(self):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'profile_update.html'
    success_url = reverse_lazy('profile')

    def get(self, request, *args,):
        user_form = UpdateUser(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        return render(request, self.template_name, {'user_form': user_form, 'profile_form': profile_form})
    
    def post(self, request):
        user_form = UpdateUser(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and  profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Votre profil a été mis à jour avec succès.")
            return redirect(self.success_url)
        else:
            print(user_form.errors, profile_form.errors)
        return render(request, self.template_name, {'user_form': user_form, 'profile_form': profile_form})
