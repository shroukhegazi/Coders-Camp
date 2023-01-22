from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions
from .serializers import PostSerializer,LikeSerializer, CommentSerializer
from .models import Post, CustomUser,Like, Comment
from .helpers import get_post, get_comment



class PostListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def post(self,request, *args, **kwargs):

        serializer = PostSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save(user_id=request.user.id)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
class PostDetailAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, requset, pk, *args, **kwargs):
        post= get_post(self,pk)
        if post is None:
            return Response({'error': 'Post not found'}, status = status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(post)
        return Response(serializer.data, status = status.HTTP_200_OK)


    def put(self, request, pk, *args, **kwargs):
        post= get_post(self,pk)
        if post is None:
            return Response({'error': 'Post not found'}, status = status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(post, data = request.data, partial = True)  
        if serializer.is_valid():
            if post.user.id == request.user.id:
                serializer.save()
                return Response(serializer.data, status = status.HTTP_200_OK)
            return Response({"error": "You are not authorized to edit this post"}, status = status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST) 


    def delete(self, request,pk, *args, **kwargs):
        post= get_post(self,pk)
        if post is None:
            return Response({'error': 'Post not found'}, status = status.HTTP_404_NOT_FOUND)
        if post.user.id == request.user.id:
            # like = Like.objects.filter(post=self.kwargs["pk"])
            # if like:
            #     like.delete()
            post.delete()
            return Response({"msg":"Post has been deleted!"}, status = status.HTTP_200_OK)
        return Response({"error": "You are not authorized to delete this post"}, status = status.HTTP_401_UNAUTHORIZED)
  

class UserPostAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, username, *args, **kwargs):
        user = CustomUser.objects.filter(username = username).first()
        if user is None:
            return Response({'error': 'User not found'}, status = status.HTTP_404_NOT_FOUND)
        posts = Post.objects.filter(user = user)
        serializer = PostSerializer(posts, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

class CommentAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        post = get_post(self, pk)
        if post is None:
            return Response({'error': 'Post not found'}, status = status.HTTP_404_NOT_FOUND)
        comments = Comment.objects.filter(post_id=self.kwargs["pk"])
        serializer= CommentSerializer(comments, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def post(self, request, pk, *args, **kwargs):
        post = get_post(self,pk)
        if post is None:
            return Response({'error': 'Post not found'}, status = status.HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(user_id=request.user.id,post_id=self.kwargs["pk"])
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class CommentDetailAPIView(APIView):
    def get(self, requset, pk,pk2 ,*args, **kwargs):
        comment= get_comment(self,pk2)
        if comment is None:
            return Response({'error': 'comment not found'}, status = status.HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def delete(self, request,pk,pk2, *args, **kwargs):  
        post = get_post(self,pk) 
        comment=get_comment(self, pk2)
        if post is None:
            return Response({'error': 'Post not found'}, status = status.HTTP_404_NOT_FOUND)
  
        if comment.user.id == request.user.id:
            comment.delete()
            return Response({"msg":"Comment has been deleted!"}, status = status.HTTP_200_OK)
        return Response({"error": "You are not authorized to delete this post"}, status = status.HTTP_401_UNAUTHORIZED)    

class LikeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, pk, *args, **kwargs):
        post = get_post(self, pk)
        if post is None:
            return Response({'error': 'Post not found'}, status = status.HTTP_404_NOT_FOUND)

        like = Like.objects.filter(post=post.id, user=request.user).first()
        if like:
            like.delete()
            post.likes_count -=1
            post.save()
            return Response({"Error": "You unliked this post"}, status=status.HTTP_200_OK)

        else:
            like= Like.objects.create(user= request.user, post= post )
            like.save()
            post.likes_count +=1
            post.save()
            return Response({"status": "You liked this post"}, status=status.HTTP_200_OK)

                   
   
                

             