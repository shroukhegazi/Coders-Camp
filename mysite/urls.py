from django.urls import path, include
from .views import PostListAPIView, PostDetailAPIView, UserPostAPIView, LikeAPIView, CommentAPIView, CommentDetailAPIView
urlpatterns = [
    #auth endpoints
    path("auth/", include('djoser.urls')),
    path("auth/", include('djoser.urls.jwt')),
    #posts endpoints
    path('post/', PostListAPIView.as_view()),
    path('post/<int:pk>/', PostDetailAPIView.as_view()),
    path('<username>/posts/', UserPostAPIView.as_view()),
    #like, unlike endpoints
    path('<int:pk>/like/', LikeAPIView.as_view()),
    #comments endpoints
    path('<int:pk>/comment/', CommentAPIView.as_view()),
    path('<int:pk>/comment/<int:pk2>', CommentDetailAPIView.as_view())




    

    ]
