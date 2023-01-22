from django.urls import reverse 
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from mysite.models import Post, CustomUser, Comment, Like

class TestPostViews(APITestCase):
#Creating Post Tests
    
    def test_post_by_unauthenicated_user(self):
        client = APIClient()
        data = {
            "title": "CodeCamp",
            "url":"https://www.django-rest-framework.org/"
        }
        response = client.post("/post/",data)
        res_data = response.data
        assert response.status_code == 401

    def test_post_by_authenicated_user(self):
        client = APIClient()

        user=CustomUser.objects.create_user("testing1", "134679//t")
        client.force_authenticate(user=user)
        data = {
            "title": "CodeCamp",
            "url":"https://www.django-rest-framework.org/"
        }

        response = client.post("/post/",data)
        res_data = response.data["data"]
        assert response.status_code == 200
        assert res_data["title"] == data["title"]
        assert res_data["url"] == data["url"]
        post = Post.objects.filter(title="CodeCamp").first()
        assert post is not None
        assert post.url == "https://www.django-rest-framework.org/"

    def test_post_by_authenicated_user_missing_url(self):
        client = APIClient()
        user=CustomUser.objects.create_user("testing1", "134679//t")
        client.force_authenticate(user=user)

        data = {
            "title": "CodeCamp"
        }

        response = client.post("/post/",data)
        res_data = response.data["data"]
        assert response.status_code == 400

    def test_post_by_authenicated_user_missing_title(self):
        client = APIClient()

        user=CustomUser.objects.create_user("testing1", "134679//t")
        client.force_authenticate(user=user)
        data = {
           "url":"https://www.django-rest-framework.org/"
        }

        response = client.post("/post/",data)
        res_data = response.data["data"]
        assert response.status_code == 400

    def test_post_by_authenicated_user_without_data(self):
        client = APIClient()

        user=CustomUser.objects.create_user("testing1", "134679//t")
        client.force_authenticate(user=user)

        response = client.post("/post/",{})
        res_data = response.data["data"]
        assert response.status_code == 400        

    def test_partial_update_post(self):
        client = APIClient()

        user=CustomUser.objects.create_user("testing1", "134679//t")
        client.force_authenticate(user=user)
        post= Post(title="CodeCamp",url="https://www.django-rest-framework.org/", user=user)
        post.save()
        response = client.put("/post/"+str(post.pk)+"/" , {"title":"coding"})
        #Hard Refresh The Object From The DB
        post = Post.objects.get(id=post.pk)
        assert response.status_code == 200
        assert post.title == "coding"  

    def test_update_unexist_post(self):
        client = APIClient()
        user=CustomUser.objects.create_user("testing1", "134679//t")
        client.force_authenticate(user=user)
        response = client.delete("/post/60/",{"title":"dosent exist"})
        assert response.status_code == 404      
#Get Posts Tests
    def test_get_by_unauthenicated_user(self):
        client = APIClient()
        post= Post(title="CodeCamp",url="https://www.django-rest-framework.org/")
        post.save()
        response = client.get("/post/"+str(post.pk)+"/")
        assert response.status_code == 401       

    def test_get_post(self):
        client = APIClient()

        user=CustomUser.objects.create_user("testing1", "134679//t")
        client.force_authenticate(user=user)

        post= Post(title="CodeCamp",url="https://www.django-rest-framework.org/", user=user)
        post.save()
        response = client.get("/post/"+str(post.pk)+"/")
        assert response.status_code == 200
        assert post.title == response.data["title"]  

    def test_get_unexist_post(self):
        client = APIClient()
        user=CustomUser.objects.create_user("testing1", "134679//t")
        client.force_authenticate(user=user)
        response = client.get("/post/60/")
        assert response.status_code == 404    

#Delete Post Tests
    def test_delete_by_unauthenicated_user(self):
        client = APIClient()
        post= Post(title="CodeCamp",url="https://www.django-rest-framework.org/")
        post.save()
        response = client.delete("/post/"+str(post.pk)+"/")
        assert response.status_code == 401        

    def test_delete_post(self):
        client = APIClient()
        user=CustomUser.objects.create_user("testing1", "134679//t")
        client.force_authenticate(user=user)

        post= Post(title="CodeCamp",url="https://www.django-rest-framework.org/", user=user)
        post.save()
        response = client.delete("/post/"+str(post.pk)+"/")
        assert response.status_code == 200

    def test_delete_unexist_post(self):
        client = APIClient()
        user=CustomUser.objects.create_user("testing1", "134679//t")
        client.force_authenticate(user=user)
        response = client.delete("/post/60/")
        assert response.status_code == 404

class TestCommentViews(APITestCase):
#Creating comments tests
    def test_comment_by_authenicated_user(self):
        client = APIClient()
        user=CustomUser.objects.create_user("testing1", "134679//t")
        client.force_authenticate(user=user)
        post= Post(title="CodeCamp",url="https://www.django-rest-framework.org/", user=user)
        post.save()
        data= {
            "comment":"My Comment"
        }
        response = client.post("/"+str(post.pk)+"/comment/",data)
        res_data = response.data
        assert response.status_code == 201
        assert res_data["comment"] == data["comment"]
        comment = Comment.objects.filter(comment="My Comment").first()
        assert comment is not None


    def test_comment_by_unauthenicated_user(self):
        client = APIClient()
        user=CustomUser.objects.create_user("testing1", "134679//t")
        post= Post(title="CodeCamp",url="https://www.django-rest-framework.org/", user=user)
        post.save()
        data= {
            "comment":"My Comment"
        }
        response = client.post("/"+str(post.pk)+"/comment/",data)
        assert response.status_code == 401
      
#Getting comments tests 
    def test_get_exist_comment(self):
        client = APIClient()
        user=CustomUser.objects.create_user("testing1", "134679//t")
        client.force_authenticate(user=user)

        post= Post(title="CodeCamp",url="https://www.django-rest-framework.org/", user=user)
        post.save()
        comment= Comment(comment="My Comment", user=user, post=post)
        comment.save()
    
        response = client.get("/"+str(post.pk)+"/comment/"+str(comment.pk))
        res_data = response.data
        assert response.status_code == 200
        assert res_data["comment"] == comment.comment


    def test_get_unexist_comment(self):
        client = APIClient()
        user=CustomUser.objects.create_user("testing1", "134679//t")
        client.force_authenticate(user=user)

        post= Post(title="CodeCamp",url="https://www.django-rest-framework.org/", user=user)
        post.save()
        response = client.get("/"+str(post.pk)+"/comment/70/")
        assert response.status_code == 404

#Deleting comments tests
    def test_delete_exist_comment(self):
        client = APIClient()
        user=CustomUser.objects.create_user("testing1", "134679//t")
        client.force_authenticate(user=user)

        post= Post(title="CodeCamp",url="https://www.django-rest-framework.org/", user=user)
        post.save()
        comment= Comment(comment="My Comment", user=user, post=post)
        comment.save()
    
        response = client.delete("/"+str(post.pk)+"/comment/"+str(comment.pk))
        assert response.status_code == 200
  
    def test_delete_unexist_comment(self):
        client = APIClient()
        user=CustomUser.objects.create_user("testing1", "134679//t")
        client.force_authenticate(user=user)

        post= Post(title="CodeCamp",url="https://www.django-rest-framework.org/", user=user)
        post.save()
        response = client.delete("/"+str(post.pk)+"/comment/70/")
        assert response.status_code == 404


class TestLikeViews(APITestCase):
    def test_like_by_unauthenticated_user(self):
        client = APIClient()
        user=CustomUser.objects.create_user("testing1", "134679//t")

        post= Post(title="CodeCamp",url="https://www.django-rest-framework.org/", user=user)
        post.save() 
        response = client.post("/"+str(post.pk)+"/like/",{})
        assert response.status_code == 401

    def test_like_post(self):
        client = APIClient()
        user=CustomUser.objects.create_user("testing1", "134679//t")
        client.force_authenticate(user=user)    

        post= Post(title="CodeCamp",url="https://www.django-rest-framework.org/", user=user)
        post.save() 
        response = client.post("/"+str(post.pk)+"/like/",{})
        post = Post.objects.get(id=post.pk)
        assert response.status_code == 200
        assert post.likes_count ==1

    def test_unlike_post(self):
        client = APIClient()
        user=CustomUser.objects.create_user("testing1", "134679//t")
        client.force_authenticate(user=user)    

        post= Post(title="CodeCamp",url="https://www.django-rest-framework.org/", user=user, likes_count=1)
        post.save() 
        like= Like(user=user, post=post)
        like.save()
        response = client.post("/"+str(post.pk)+"/like/",{})
        post = Post.objects.get(id=post.pk)
        assert response.status_code == 200
        assert post.likes_count ==0   

    def test_like_unexist_post(self):
        client = APIClient()
        user=CustomUser.objects.create_user("testing1", "134679//t")
        client.force_authenticate(user=user)    
        response = client.post("/90/like/",{})
        assert response.status_code == 404

