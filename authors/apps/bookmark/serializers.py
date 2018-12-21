from rest_framework import serializers

# local imports
from .models import BookmarkArticle


class BookmarkSerializer(serializers.ModelSerializer):
    """
    Bookmarks serializer
    """
    class Meta:
        model = BookmarkArticle

        fields = ('user', 'bookmark')
        read_only = ('created_at', 'updated_at')
