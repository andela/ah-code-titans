from rest_framework import serializers


# local imports
from .models import FavouriteArticle


class FavoritedSerializers(serializers.ModelSerializer):
    """
    favorite article serializer
    """
    user = serializers.CurrentUserDefault

    class Meta:
        model = FavouriteArticle
        fields = ('user', 'article',)

    def create(self, validated_data):
        """
        Creates a record that depicts one user favoriting an article
        :param validated_data:
        :return:
        """
        return FavouriteArticle.objects.create(**validated_data)
