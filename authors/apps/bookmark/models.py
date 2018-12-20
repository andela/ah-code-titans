from django.db import models

# local imports
from ...apps.authentication.models import User


class BookmarkArticle(models.Model):
    """
    Bookmarks model
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bookmark = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.bookmark
