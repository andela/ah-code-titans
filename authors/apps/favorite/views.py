from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

# local imports
from .serializers import FavoritedSerializers
from .renderers import FavoriteJSONRenderer
from ..articles.models import Article
from .models import FavouriteArticle
from authors.response import RESPONSE


class FavoriteView(CreateAPIView, DestroyAPIView):
    """
    favorite and unfavorite an article.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = FavoritedSerializers
    renderer_classes = (FavoriteJSONRenderer,)

    def post(self, request, slug):
        """
        Favorite a specific article
        :param slug
        authenticated users can favorite an article
        """

        article = check_article_exist(slug)

        if isinstance(article, Response):
            return article

        # check if user has favourite an article
        # If user has favourited the article raise a flag
        # otherwise favourite the article
        favorite = FavouriteArticle.objects.filter(user=self.request.user.id, article=article.id).exists()
        if favorite:
            return Response(
                {"message": RESPONSE['favorite']['favorited_twice']},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = {"user": request.user.id, "article": article.id}
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        message = {"message": RESPONSE['favorite']['favorited']}

        return Response(message, status=status.HTTP_200_OK)

    def delete(self, request, slug):
        """
        unfavorite a specific article
        :param slug
        authenticated users can favorite an article
        """

        article = check_article_exist(slug)

        if isinstance(article, Response):
            return article

        # check if user has unfavourite an article
        # If a user tries to favorite an article raise a flag
        # otherwise a user con unfavourite the article
        favorite = FavouriteArticle.objects.filter(user=self.request.user.id, article=article.id).exists()
        if not favorite:
            return Response(
                {"message": RESPONSE['favorite']['unfavorited_twice']},
                status=status.HTTP_400_BAD_REQUEST
            )

        instance = FavouriteArticle.objects.filter(user=request.user.id, article=article.id)
        self.perform_destroy(instance)

        message = {"message": RESPONSE['favorite']['unfavorited']}

        return Response(message, status=status.HTTP_204_NO_CONTENT)


class GetAllFavorites(ListAPIView):
    """
    get all favorited articles by current user 
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = FavoritedSerializers
    renderer_classes = (FavoriteJSONRenderer,)

    def get_queryset(self):
        return FavouriteArticle.objects.filter(user_id=self.request.user.id)

    def get(self, *args, **kwargs):
        """
        get all favorited articles
        :param slug
        authenticated users can view article they have favorited
        """
        get_article = self.get_queryset()

        # if user has not favorited any articles
        # raise a flag to inform the user
        if not get_article:
            message = {"message": RESPONSE['favorite']['no_favorites']}
            return Response(message, status=status.HTTP_200_OK)

        serializer = self.serializer_class(instance=get_article, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


def check_article_exist(slug):
    try:
        get_article = Article.objects.get(slug=slug)
    except Article.DoesNotExist:
        message = {"message": RESPONSE['favorite']['not_found'].format(slug)}
        return Response(message, status=status.HTTP_404_NOT_FOUND)
    return get_article
