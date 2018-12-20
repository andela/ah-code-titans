from rest_framework import serializers
from .models import UserReadStat


class UserReadStatSerializer(serializers.ModelSerializer):
    duration = serializers.SerializerMethodField()
    article = serializers.SerializerMethodField()

    class Meta:
        model = UserReadStat
        fields = '__all__'

    def get_duration(self, stat):
        duration = stat.updatedAt - stat.createdAt
        return duration

    def get_article(self, stat):
        return {
            "title": stat.article.title,
            "slug": stat.article.slug
        }
