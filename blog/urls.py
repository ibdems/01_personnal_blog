from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from blog import settings

urlpatterns = [
    path('',include('article.urls')),
    path('panel/', include('admin_panel.urls')),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)