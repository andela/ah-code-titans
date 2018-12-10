from authors.apps.authentication.models import User
from authors.response import RESPONSE
from rest_framework import serializers

from .models import Article, Comment


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Article
        fields = ("title", "description", "body", "author")


class CommentSerializer(serializers.ModelSerializer):
    """
    This serializer class is response for serializing comment
    data provided by the user.
    """
    # This relates the comment to the article it is commenting on.
    article = serializers.PrimaryKeyRelatedField(
        queryset=Article.objects.all()
    )

    # This relates the comment to the author of the comment
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )

    # This is the parent comment id this comment may potentially be replying
    # to. This is optional.
    parent = serializers.IntegerField()

    # This is the comment body
    text = serializers.CharField(max_length=None, required=True)

    class Meta:
        model = Comment
        fields = ['parent', 'text', 'article', 'user']

    def validate_text(self, validated_data):

        if validated_data == "":
            raise serializers.ValidationError(
                RESPONSE['empty_field'].format("text")
            )

        return validated_data

    def update(self, instance, validated_data):

        for (key, value) in validated_data.items():
            # For the keys remaining in `validated_data`, we will set them on
            # the current `Comment` instance one at a time.
            setattr(instance, key, value)

        # This saves all the changes specified in the validated data, into the
        # database
        instance.save()
