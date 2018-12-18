from authors.apps.authentication.models import User
from authors.response import RESPONSE
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers

from .models import Article, Comment
from ..favorite.models import FavouriteArticle


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Article
        fields = ("title", "description", "body", "author")

    def validate_user_permissions(self, request, data):
        """
        :param request and data
        """
        if request.user.id != data.author_id:

            return Response({
                "message": "you are not allowed to perform this action"
            },
                status=status.HTTP_403_FORBIDDEN
            )


class GetArticlesSerializer(serializers.ModelSerializer):

    author = serializers.SerializerMethodField()
    favorite = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = '__all__'

    def get_author(self, article):
        author_data = article.author
        profile = author_data.profile
        author = {
            'username': author_data.username,
            'bio': profile.bio,
            'image': profile.image,
        }

        return author

    def get_favorite(self, slug):
        user = self.context.get('request').user.id
        article = slug.id
        favorite = FavouriteArticle.objects.filter(user=user, article=article).exists()

        return favorite


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
