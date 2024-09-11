
from django.contrib import admin

from .models import Article, Category, Tag, Message, Comment, Profile
from admin_panel.forms import ArticleForm
# Register your models here.
admin.site.site_header = "Dems Blog"
class CategorieAdmin(admin.ModelAdmin):
    pass

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_published'
    list_display = ['title','category', 'image', 'summary', 'date_published', 'user']
    fields = ('category','title',  'summary',  'content', 'image', 'date_published')

    def save_model(self, request, obj ,form, change):
        obj.user = request.user
        return super().save_model(request, obj, form, change)
    
    def has_change_permission(self, request, obj=None):
        if obj  and obj.user != request.user:
            return False
        return super().has_change_permission(request, obj)
    
    def has_delete_permission(self, request, obj=None) -> bool:
        if obj  and obj.user != request.user:
            return False
        return super().has_delete_permission(request, obj)
    


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category, CategorieAdmin)