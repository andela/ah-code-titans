from django.db import models
from authors.apps.articles.models import Article
from authors.apps.authentication.models import User


class UserReadStat(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             null=False, blank=False,)

    article = models.ForeignKey(Article,
                                on_delete=models.CASCADE,
                                null=False, blank=False,)
    read = models.BooleanField(default=False)

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Print out as title."""
        return self.article.title
