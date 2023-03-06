from django.db import models


class Friendship(models.Model):
    class Meta:
        ordering = ["id"]

    friendship_status = models.BooleanField(default=False)

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="friends",
    )

    user_relation = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="friends",
    )
