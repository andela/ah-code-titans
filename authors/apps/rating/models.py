from django.db import models

from ..authentication.models import User
from ..articles.models import Article

# Create your models here.


class RateArticle(models.Model):
    # This is the foreign key that relates a rating to an article
    article = models.ForeignKey(Article, on_delete=models.CASCADE,)

    # This is the foreign key that relates a rating to an specific user
    user = models.ForeignKey(User, on_delete=models.CASCADE,)

    # This is to hold the user rating on the specific article
    user_rating = models.IntegerField(default=0)
