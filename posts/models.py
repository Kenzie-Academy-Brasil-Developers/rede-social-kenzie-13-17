from django.db import models


class Post(models.Model):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="posts")
    title = models.CharField(max_length=45)
    content = models.TextField(null=True, max_length=400)
    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    users_likes = models.ManyToManyField("users.User", related_name="likes")
