from django.db import models


# local imports
from ...apps.authentication.models import User
from ...apps.articles.models import Article


class FavouriteArticle(models.Model):
    """
    favorite articles model
    """

    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    article = models.ForeignKey(Article, related_name='favorited', on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        return a human readable string
        """
        return '{user} favorited article {favorited}'.format(
            user=self.user, favorited=self.article
        )
