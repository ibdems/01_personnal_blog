from django.urls import path
from .views import *
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('detail_article/<int:pk>', ArticleDetailsView.as_view(), name='detail_article_public'),
    path('contact/', ContactCreateView.as_view(), name='contact'),
]
