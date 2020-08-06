from django.contrib import admin
from article.models import Article, Comment
# Register your models here.

class CommentAdmin(admin.ModelAdmin):
    list_display = ['article', 'content', 'pubDateTime']
    
    class Meta:
        model = Comment

admin.site.register(Article)
admin.site.register(Comment, CommentAdmin)
