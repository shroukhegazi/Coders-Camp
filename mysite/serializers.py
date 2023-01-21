from rest_framework import serializers
from django.core.validators import URLValidator

from .models import Post, Like, Comment

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('__all__')
        read_only_fields = ['user']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('__all__')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('__all__')
        read_only_fields = ['user']
       