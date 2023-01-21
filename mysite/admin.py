from django.contrib import admin
from .models import Comment, Post, CustomUser, Like


# Register your models here.

@admin.register(CustomUser)
class UserAdmin (admin.ModelAdmin):
    list_display = ["username", "email"]

@admin.register(Post)
class PostAdmin (admin.ModelAdmin):
    list_display = ["title","user", "posted_at", "url", "likes_count"]

    

@admin.register(Comment)
class CommentAdmin (admin.ModelAdmin):
    list_display = ["post", "comment", "user", "posted_at"]

@admin.register(Like)
class LikeAdmin (admin.ModelAdmin):
    list_display = ["post", "user"]