from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authors.apps.articles.models import Article
from authors.apps.articles.serializers import GetArticlesSerializer
from authors.apps.bookmark.models import Bookmark
from authors.apps.bookmark.renderers import BookmarksJSONRenderer
from authors.apps.bookmark.serializers import BookmarkSerializer
from authors.response import RESPONSE


class BookmarkArticleCreateDestroyAPIView(CreateAPIView, DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BookmarkSerializer
    renderer_classes = (BookmarksJSONRenderer,)

    class Meta:
        model = Bookmark
        fields = ('user', 'article',)

    def post(self, request, slug):
        """
        Bookmark a specific article
        :param slug
        authenticated users can bookmark an article
        """

        to_bookmark = check_article(slug)

        if isinstance(to_bookmark, Response):
            return to_bookmark

        bookmarked = Bookmark.objects.filter(user=self.request.user.id, slug=slug).exists()
        if bookmarked is True:
            return Response(
                {"message": RESPONSE['bookmark']['repeat_bookmarking']},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = {"user": request.user.id, "slug": slug}
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        message = {"message": RESPONSE['bookmark']['bookmarked'].format(data=slug)}

        return Response(message, status=status.HTTP_200_OK)

    def delete(self, request, slug):
        """
        unbookmark a specific article
        :param slug
        authenticated users can unbookmark an article
        """

        to_unbookmark = check_article(slug)

        if isinstance(to_unbookmark, Response):
            return to_unbookmark

        bookmarked = Bookmark.objects.filter(user=self.request.user.id, slug=slug).exists()
        if bookmarked is False:
            message = {"message": RESPONSE['bookmark']['repeat_unbookmarking']}
            return Response(
                message,
                status=status.HTTP_400_BAD_REQUEST
            )

        instance = Bookmark.objects.filter(user=self.request.user.id, slug=slug)
        self.perform_destroy(instance)

        message = {"message": RESPONSE['bookmark']['unbookmarked'].format(data=slug)}

        return Response(message, status=status.HTTP_204_NO_CONTENT)


class BookmarkListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = GetArticlesSerializer
    renderer_classes = (BookmarksJSONRenderer,)

    def get_queryset(self):
        article_to_bookmark = Bookmark.objects.filter(user_id=self.request.user.pk)

        if not article_to_bookmark:
            return []

        slugs = Bookmark.objects.filter(user_id=self.request.user.id).values_list('slug', flat=True)
        articles = Article.objects.filter(slug__in=slugs)
        return articles


def check_article(slug):
    try:
        article_to_bookmark = Article.objects.get(slug=slug)
    except Article.DoesNotExist:
        message = {"message": RESPONSE['article_not_found'].format(data=slug)}
        return Response(message, status=status.HTTP_404_NOT_FOUND)
    return article_to_bookmark
