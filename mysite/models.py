from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import URLValidator


class CustomUser(AbstractUser):

    def __str__(self):
        return self.username


class Post(models.Model):
    title = models.CharField(max_length=250, null=False)
    user= models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)
    url = models.TextField(validators=[URLValidator()])
    likes_count= models.IntegerField(default = 0)

    def __str__(self):
        return self.title

class Like (models.Model):
    user=models.ForeignKey(CustomUser,  related_name = 'likes',on_delete=models.SET_NULL, null=True)
    post=models.ForeignKey(Post,  related_name = 'likes', on_delete=models.SET_NULL, null=True)


class Comment(models.Model):
    comment= models.CharField(max_length=1000, null=False)
    posted_at= models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(CustomUser,  on_delete=models.SET_NULL, null=True)
    post=models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    