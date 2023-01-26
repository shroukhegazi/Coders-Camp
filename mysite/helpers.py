from .models import Post, Comment, CustomUser
def get_post(self, pk):
        try:
            return Post.objects.get(pk = pk)
        except Post.DoesNotExist:
            return None

def get_comment(self, pk):
        try:
            return Comment.objects.get(pk = pk)
        except Comment.DoesNotExist:
            return None


def number_of_likes(self):
    return self.likes.count()


def user(self):
    user=CustomUser.objects.create_user("testing1", "134679//t")

