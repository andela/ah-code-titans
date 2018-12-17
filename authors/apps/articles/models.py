from authors.apps.likedislike.models import ArticleLikeDislike
from django.contrib.contenttypes.fields import GenericRelation
from authors.apps.authentication.models import User
from django.db import models
from django.template.defaultfilters import slugify
from taggit.managers import TaggableManager


class Article(models.Model):
    """
    create articles models
    """
    slug = models.SlugField(max_length=50, unique=True)
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

        # This generates a new slug from the title of the article.
        self.slug = slugify(self.title)

        unique_slug = self.slug
        extension = 1

        # This ensures that the slug is unique by running through multiple
        # variations of the slug by adding an integer at the end.
        while Article.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(self.slug, extension)
            extension += 1

        self.slug = unique_slug

        super(Article, self).save(*args, **kwargs)

    def json(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "body": self.body,
            "author": self.author.json(),
            "created_at": self.createdAt.strftime('%Y-%m-%d %H:%M:%S'),
            "updated_at": self.updatedAt.strftime('%Y-%m-%d %H:%M:%S'),
        }


class Comment(models.Model):

    # This is the foreign ket that relates this comment to the article it is commenting on
    article = models.ForeignKey(
        Article, verbose_name="comment_article", on_delete=models.CASCADE)
    # article = models.ForeignKey(Article, on_delete=models.CASCADE)

    # This is the foreign key that relates this comment to the author, which
    # is a user registered to the app.
    user = models.ForeignKey(User, verbose_name="comment_user", on_delete=models.CASCADE)

    # This is the id of the parent comment that this comment replies to.
    # This is optional and set to 0 as the default. This is to create a 
    # threaded comment system.
    parent = models.IntegerField(default=0)

    # This is the comment text.
    text = models.TextField()

    # This is used to save the time at which this comment was created.
    created_at = models.DateTimeField(auto_now_add=True)

    # This is used to save the last time the comment was updated.
    updated_at = models.DateTimeField(auto_now=True)

    def json(self):

        return {
            "article": self.article.id,
            "user": self.user.id,
            "parent": self.parent,
            "text": self.text,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "updated_at": self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
