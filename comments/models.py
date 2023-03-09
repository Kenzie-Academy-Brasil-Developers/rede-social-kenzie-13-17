from django.db import models


class Comment(models.Model):
    comment = models.TextField(max_length=400)
<<<<<<< HEAD
    created_at = models.DateField(auto_now=False, auto_now_add=True)
=======
    created_at = models.DateField(auto_now_add=True)
>>>>>>> 8e117fac0543d0e83da57fea06c177c88fd1cd26
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
