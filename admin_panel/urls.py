from django.urls import include, path
from .views import *

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('inscription/', registration, name='registration'),
    path('login/', signin, name='signin'),
    path('deconnexion/', signout, name='signout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('updateProfile/', UpdateProfileView.as_view(), name='update_profile'),
    path('category/',include([
        path('', CategoryListView.as_view(), name='category_list'),
        path('create/', CategoryCreateView.as_view(), name='category_create'),
        path('<int:pk>/update/', CategoryUpdateView.as_view(), name='category_update'),
        path('<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),
    ])),
    path('article/',include([
        path('', ArticleListView.as_view(), name='article_list'),
        path('create/', ArticleCreateView.as_view(), name='article_create'),
        
        path('<int:pk>/update/', ArticleUpdateView.as_view(), name='article_update'),
        path('<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
    ])),path('<int:pk>/details/', ArticleDetailsView.as_view(), name='article_details'),

    path('commentaire/', include([
        path('', CommentaireListView.as_view(), name='commentaire_list'),
        path('<int:pk>/delete', CommentaireDeleteView.as_view(), name='commentaire_delete'),
        path('<int:id>/approuve', approved_commentaire, name='commentaire_approuve'),
    ])),

    path('message/',include([
        path('', MessageListView.as_view(), name='message_list')
        # path('<int:pk>/delete', MessageDeleteView.as_view(), name='message_delete'),
    ]))
]
