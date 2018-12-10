from rest_framework import serializers
from .models import Article


class ArticlesSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Article
        fields = ("title", "description", "body", "author")
