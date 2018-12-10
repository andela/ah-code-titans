from django.db import models
from taggit.managers import TaggableManager
from django.template.defaultfilters import slugify
from django.contrib.contenttypes.fields import GenericRelation

from ..authentication.models import User
from authors.apps.likedislike.models import ArticleLikeDislike


class Article(models.Model):
    """
    create articles models
    """
    slug = models.SlugField(max_length=50)
    title = models.CharField(max_length=50)
    description = models.TextField()
    body = models.TextField()
    tag_list = TaggableManager(blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    votes = GenericRelation(ArticleLikeDislike, related_query_name='articles')

    def __str__(self):
        return f"{self.title}, {self.body}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)
