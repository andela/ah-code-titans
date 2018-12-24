from rest_framework import serializers

# local imports
from authors.apps.bookmark.models import Bookmark


class BookmarkSerializer(serializers.ModelSerializer):
    """
    Bookmarks serializer
    """

    class Meta:
        model = Bookmark

        fields = ('user', 'slug')
        read_only = ('created_at',)
