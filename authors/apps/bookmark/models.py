from django.db import models

# local imports
from authors.apps.authentication.models import User


class Bookmark(models.Model):
    """
    Bookmarks model
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
