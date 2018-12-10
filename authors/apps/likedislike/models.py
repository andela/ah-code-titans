from django.db import models
from django.db.models import Sum
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from authors.apps.authentication.models import User


class ArticleLikeDislikeManager(models.Manager):
    """
    Manager class for article like and dislike
    """
    def likes(self):
        """
        Return all likes for a particular article.
        We take the query set with records greater than 0
        """
        return self.get_queryset().filter(vote__gt=0)

    def dislikes(self):
        """
        get all the dislikes for a particular article.
        We take the query set with records less than 0.
        """
        return self.get_queryset().filter(vote__lt=0)

    def sum_rating(self):
        """
        Get aggregate likes and dislikes for an article.
        We take the total ratings.
        """
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0


class ArticleLikeDislike(models.Model):
    """
    Model class for article like and dislike.
    """
    LIKE = 1
    DISLIKE = -1

    VOTES = (
        (LIKE, 'like'),
        (DISLIKE, 'dislike')
    )

    vote = models.SmallIntegerField(verbose_name="likes", choices=VOTES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    objects = ArticleLikeDislikeManager()

    def __str__(self):
        """
        Return a readable representation of class objects
        """
        return "Votes: {}".format(self.vote)

