from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status, exceptions
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404

from ..serializers import ArticleSerializer, GetArticlesSerializer
from ..renderers import ArticlesJSONRenderer
from ..models import Article


class ArticlesViews(CreateAPIView):
    """
    create a new article
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        post a new article
        :param request
        we are creating a  new request context then passing the context in our
        case the user that is creating an article along
        with the data in our serializer class
        """
        data = request.data.get("article", {})
        context = {'request': request}

        time_to_read = ArticleSerializer().article_time_to_read(data)
        data['time_to_read'] = time_to_read

        serializer = ArticleSerializer(data=data, context=context)
        if serializer.is_valid():
            article_data = serializer.save()
            message = {
                "message": "article created successfully",
                "slug": article_data.slug
            }
            return Response(message, status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleView(RetrieveUpdateDestroyAPIView):
    """
    get, update, delete a specific article view
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = [ArticlesJSONRenderer]

    def get(self, request, slug):
        """
        Retrieve a specific article
        :param slug
        any user should view details of an article
        """
        # Get the article user searched
        # When article is not found, Give the user a description
        # of what happened. If the article is found return it back to user
        try:
            article = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise exceptions.NotFound({
                "message": "Article was not found"})
        serializer = GetArticlesSerializer(instance=article, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request, slug):
        """
        update a specific article
        :param slug
        an author can only update his/her article
        """
        article = get_object_or_404(Article.objects.all(), slug=slug)
        ArticleSerializer().validate_user_permissions(request, article)
        data = request.data.get("article")

        time_to_read = ArticleSerializer().article_time_to_read(data)
        data['time_to_read'] = time_to_read

        serializer = ArticleSerializer(
            instance=article, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "article updated successfully",
                "article": serializer.data
            },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        """
        delete a specific article
        :param slug
        an author can only delete his/her article
        """
        article = Article.objects.filter(slug=slug)

        if not article:
            return Response({"Message": f"article {slug} not found"}, status=status.HTTP_404_NOT_FOUND)
        if request.user.id != article[0].author_id:
            return Response({
                "message": "you are not allowed to perform this action"
            },
                status=status.HTTP_403_FORBIDDEN
            )
        article[0].delete()
        return Response({"article": "deleted successfully"}, status=status.HTTP_200_OK)


class GetArticles(ListAPIView):
    """
    get all articles views
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = GetArticlesSerializer
    renderer_classes = (ArticlesJSONRenderer,)
    queryset = Article.objects.all()
