from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

# local imports
from .serializers import BookmarkSerializer
from ..articles.models import Article
from .models import BookmarkArticle
from authors.response import RESPONSE


class BookmarkArticleView(CreateAPIView, DestroyAPIView):
    """
    Bookmarking articles.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = BookmarkSerializer

    def post(self, request, slug):
        """
        Bookmark a specific article
        :param slug
        authenticated users can bookmark an article
        """

        to_bookmark = check_article(slug)

        if isinstance(to_bookmark, Response):
            return to_bookmark

        bookmarked = BookmarkArticle.objects.filter(user=self.request.user.id, bookmark=slug).exists()
        if bookmarked is True:
            return Response(
                {"message": RESPONSE['bookmark']['repeat_bookmarking']},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = {"user": request.user.id, "bookmark": slug}
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

        bookmarked = BookmarkArticle.objects.filter(user=self.request.user.id, bookmark=slug).exists()
        if bookmarked is False:
            message = {"message": RESPONSE['bookmark']['repeat_unbookmarking']}
            return Response(
                message,
                status=status.HTTP_400_BAD_REQUEST
            )

        instance = BookmarkArticle.objects.filter(user=self.request.user.id, bookmark=slug)
        self.perform_destroy(instance)

        message = {"message": RESPONSE['bookmark']['unbookmarked'].format(data=slug)}

        return Response(message, status=status.HTTP_204_NO_CONTENT)


class GetAllBoookmarksView(ListAPIView):
    """
    get all bookmarked articles by current user 
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = BookmarkSerializer

    def get(self, request):
        """
        only authenticated users can view bookmarks
        """
        article_to_bookmark = BookmarkArticle.objects.filter(user_id=self.request.user.id)

        if len(article_to_bookmark) == 0:
            return Response(
                {"message": RESPONSE['bookmark']['no_bookmarks']},
                status=status.HTTP_200_OK
            )

        serializer = self.serializer_class(instance=article_to_bookmark, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


def check_article(slug):
    try:
        article_to_bookmark = Article.objects.get(slug=slug)
    except Article.DoesNotExist:
        message = {"message": RESPONSE['article_not_found'].format(data=slug)}
        return Response(message, status=status.HTTP_404_NOT_FOUND)
    return article_to_bookmark
