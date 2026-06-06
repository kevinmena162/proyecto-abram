from django.contrib import admin
from .models import Author, Post, Comment

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'username', 'occupation', 'nationality')
    search_fields = ('name', 'username', 'key_theories')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'created_at', 'likes_count')
    list_filter = ('author', 'created_at')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author_name', 'created_at')
    list_filter = ('created_at',)

