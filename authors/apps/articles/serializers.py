import numpy
import re

from authors.apps.authentication.models import User
from authors.response import RESPONSE
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers

from .models import Article, Comment
from ..favorite.models import FavouriteArticle


class TagListSerializer(serializers.Field):
    """
    implementing taglist serializers
    :param serializer.Writablefield
    """

    def to_internal_value(self, data):
        """
        :param data get list from the client
        """
        tag_data = ArticleSerializer().validate_tag_list(data)
        return tag_data

    def to_representation(self, obj):
        """
        :param obj get is a TaggableManager instance
        converts TaggableManager instance to a list
        """
        if type(obj) is not list:
            return [tag for tag in obj.all()]
        return obj


class ArticleSerializer(serializers.ModelSerializer):
    tag_list = TagListSerializer(default=[])
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Article
        fields = ("title", "description", "body",
                  "author", "tag_list", "time_to_read")

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

    def validate_tag_list(self, validated_data):
        if type(validated_data) is not list:
            raise serializers.ValidationError(
                RESPONSE['invalid_field'].format("tag_list")
            )

        for tag in validated_data:
            if not isinstance(tag, str):
                raise serializers.ValidationError(
                    RESPONSE['invalid_field'].format("tag")
                )

        return validated_data

    def create(self, validated_data, *args):
        """
        perform a post save to save tags to database
        :param validated_data
        """
        article = Article(**validated_data)
        article.save()
        tags_to = Article.objects.get(pk=article.pk)
        for tag in article.tag_list:
            tags_to.tag_list.add(tag)
        return article

    def update(self, instance, validated_data):
        """
        post update method that updates the tag_list field.
        """

        if 'tag_list' not in validated_data:
            return instance
        instance.tag_list = validated_data.get('tag_list')
        article = Article.objects.get(pk=instance.pk)
        """
        The set method updates the current stored article taglist with a new taglist.
        *instance.tag_list splits the list elements into parameters that are now passed as a new list during updating.
        """
        article.tag_list.set(*instance.tag_list, clear=True)
        return instance

    def article_time_to_read(self, data):
        """Method to calculate the total time to read an article
        """
        # Find all text that has < and > and on that replace with empty string
        clear_body = re.compile('<.*?>')
        clean_body = re.sub(clear_body, '', data.get('body'))
        total_words = data.get('description') + ' ' + clean_body

        time_to_read = len(total_words.split()) / 180

        return (numpy.rint(time_to_read))


class GetArticlesSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    favorite = serializers.SerializerMethodField()
    tag_list = serializers.SerializerMethodField()

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
        favorite = FavouriteArticle.objects.filter(
            user=user, article=article).exists()

        return favorite

    def get_tag_list(self, article):
        return list(article.tag_list.names())


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
