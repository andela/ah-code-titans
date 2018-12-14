from rest_framework import serializers

from .models import ArticleLikeDislike


class ArticleLikeDislikeSerializer(serializers.Serializer):
    """
    Class representing serializing of likes and dislikes
    """
    class Meta:
        model = ArticleLikeDislike
