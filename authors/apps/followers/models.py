from django.db import models

from ..authentication.models import User


class Follower(models.Model):
    """
    Store data on following statistics for users.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed')
    followed_at = models.DateTimeField(auto_created=True, auto_now_add=True)

    class Meta:
        unique_together = ('user', 'followed')

    def __str__(self):
        return '{follower} follows {followed}'.format(
            follower=self.user, followed=self.followed
        )
