from django.db import models


class Comment(models.Model):
    comment = models.TextField(max_length=400)
    created_at = models.DateField(auto_now=False, auto_now_add=True)
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="comments",
    )
    publication = models.ForeignKey(
        "posts.Post",
        on_delete=models.CASCADE,
        related_name="publications",
    )
