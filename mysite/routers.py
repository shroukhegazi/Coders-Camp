from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_simplejwt import views as jwt_views
from .views import PostListAPIView

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

# router.register("", PostViews, basename="postviews")
# app_name = "mysite"


urlpatterns = router.urls