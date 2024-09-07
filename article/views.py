from typing import Any
from django.forms.models import BaseModelForm
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, CreateView 
from django.contrib import messages
from article.forms import CommentForm, MessageForm
from article.models import Article, Category, Comment, Message
from django.db.models import Prefetch
from django.db.models.query import QuerySet


class IndexView(ListView):
    model = Article
    template_name = 'article/index.html'
    context_object_name = 'articles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtenir toutes les catégories
        categories = Category.objects.all()
        # Créer un dictionnaire pour stocker les articles par catégorie
        categorized_articles = {}
        for category in categories:
            # Limiter à 6 articles par catégorie
            categorized_articles[category] = Article.objects.filter(category=category)[:6]

        context['categorized_articles'] = categorized_articles
        return context

class ArticleDetailsView(DetailView):
    model = Article
    template_name = 'article/singlePost.html'
    context_object_name = 'article' 

    
    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset()
        return queryset.prefetch_related(
            Prefetch(
                'comment_set',
                queryset=Comment.objects.filter(is_approved=True)
            )
        )

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = self.object
            comment.save()
            messages.success(request, "Votre commentaire a été ajouté et sera visible une fois approuvé par le rédacteur.")
            return redirect('detail_article_public', pk=self.object.pk)
        return self.render_to_response(self.get_context_data(form=form))
    

class ContactCreateView(CreateView):
    model = Message
    success_url = reverse_lazy('contact')
    form_class = MessageForm
    template_name = 'article/contact.html'

    def form_valid(self, form):
        messages.success(self.request, 'Votre message a ete envoyer avec success')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Votre message n\'a pas pu etre envoyer')
        return super().form_invalid(form)


class ListArticleCategory(ListView):
    model = Article
    template_name = 'article/category.html'
    context_object_name = 'articles'

    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset()
        category_id = self.kwargs.get('id')
        return queryset.filter(category=category_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('id')
        context['category'] = Category.objects.get(id=category_id)
        return context
    
    