from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny

from django.shortcuts import get_object_or_404

from .serializers import CommentSerializer, ArticleSerializer
from .models import Comment, Article
from authors.response import RESPONSE


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

    def put(self, request, slug):
        """
        update a specific article
        :param slug
        an author can only update his/her article
        """
        article = get_object_or_404(Article.objects.all(), slug=slug)
        ArticleSerializer().validate_user_permissions(request, article)
        data = request.data.get("article")
        serializer = ArticleSerializer(
            instance=article, data=data, partial=True)
        serializer.is_valid()
        serializer.save()
        return Response({
            "message": "article updated successfully"
        },
            status=status.HTTP_200_OK
        )

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
    permission_classes = (AllowAny,)

    def get(self, request):
        articles = Article.objects.all()
        if articles:
            return Response({
                "articles": [article.json() for article in articles]
            }, status.HTTP_200_OK
            )
        return Response({"message": "There are no articles currently"}, status.HTTP_404_NOT_FOUND)


class CommentsView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()

    """
    This IsAuthenticatedOrReadOnly class ensures that a user needs to be logged in,
    in order to access the API write endpoints in this view. The get endpoint does
    not require a user to be logged in. For a user to prove his authenticity, a JWT
    token needs to be provided in the authorization header which is handled by the
    authors.apps.authentication.backends.Authentication class.
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)

    serializer_class = CommentSerializer

    def get(self, request, *args, **kwargs):
        # We need to get the article slug from the url parameter.
        article_slug = kwargs["slug"]

        page_size = 20
        offset = kwargs["offset"]

        # This checks if the article slug provided matches any article in the database.
        if not Article.objects.filter(slug=article_slug).exists():
            return Response(
                {
                    "errors": {
                        "article": RESPONSE['not_found'].format(data="Article")
                    }
                }, status.HTTP_404_NOT_FOUND
            )

        # This tries to fetch a list of reply comments for the specified comment,
        # from the database. If the comment id provided does not match any in
        # the database, an error 404 response is sent back to the API user.
        comments = Comment.objects.filter(article__slug=article_slug, parent=0)[
            offset:page_size]

        if not comments:

            return Response(
                {
                    "errors": {
                        "comments": RESPONSE['not_found'].format(data="Comments")
                    }
                }, status.HTTP_404_NOT_FOUND
            )

        return Response(
            {
                "comments": [comment.json() for comment in comments],
                "offset": {
                    "next": offset + len(comments),
                    "previous": offset
                },
                "comment": RESPONSE['comment']['get_success']
            }, status.HTTP_200_OK
        )

    def post(self, request, *args, **kwargs):

        # This tries to fetch an article from the database by using the slug provided
        # in the url parameter(kwargs). If the article slug provided does not match
        # any in the database, an error 404 response is sent back to the API user.
        article = get_object_or_404(Article.objects.all(), slug=kwargs['slug'])

        # This retrieves the new comment data from the request payload
        comment = request.data

        comment['article'] = article.id

        # This gets the current logged in user's id, so we can assign it to the comment
        # as its author.
        comment['user'] = request.user.id

        # We initialize a comment serializer in order to run validations on the comment
        # data provided.
        comment_serializer = CommentSerializer(data=comment)

        # This runs a validation check on the comment data provided. If it fails, it sends
        # an error response informing the API user of the field causing the error and how
        # to fix it.
        if not comment_serializer.is_valid():
            return Response(
                {
                    "errors": comment_serializer.errors
                }, status.HTTP_400_BAD_REQUEST
            )

        # This is where we save the validated comment data to the database.
        comment_serializer.save()

        return Response(
            {
                "comment": RESPONSE['comment']['post_success']
            }, status.HTTP_201_CREATED
        )


class CommentView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()

    """
    This IsAuthenticatedOrReadOnly class ensures that a user needs to be logged in,
    in order to access the API write endpoints in this view. The get endpoint does
    not require a user to be logged in. For a user to prove his authenticity, a JWT
    token needs to be provided in the authorization header which is handled by the
    authors.apps.authentication.backends.Authentication class.
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)

    serializer_class = CommentSerializer

    def get(self, request, *args, **kwargs):
        # We need to get the comment id from the url parameter.
        comment_id = kwargs["pk"]

        page_size = 20
        offset = kwargs["offset"]

        # This tries to fetch a list of reply comments for the specified comment,
        # from the database. If the comment id provided does not match any in
        # the database, an error 404 response is sent back to the API user.
        comments = Comment.objects.filter(parent=comment_id)[offset:page_size]

        if not comments:

            return Response(
                {
                    "errors": {
                        "comments": RESPONSE['not_found'].format(data="Comments")
                    }
                }, status.HTTP_404_NOT_FOUND
            )

        return Response(
            {
                "comments": [comment.json() for comment in comments],
                "offset": {
                    "next": offset + len(comments),
                    "previous": offset
                },
                "comment": RESPONSE['comment']['replies']['get_success']
            }, status.HTTP_200_OK
        )

    def put(self, request, *args, **kwargs):
        """
        This is the update comment endpoint
        """

        # We need to get the comment id from the url parameter.
        comment_id = kwargs["pk"]

        # This tries to fetch a comment from the database. If the comment
        # id provided does not match any in the database, an error 404 response
        # is sent back to the API user.
        comment = get_object_or_404(Comment.objects.all(), id=comment_id)

        # This tries to ensure that the current logged in user is the owner of
        # the comment, and has the authority to update the comment. If this check
        # fails, we inform the user that this action is forbidden.
        if comment.user.id != request.user.id:
            return Response(
                {
                    "user": {
                        "user": RESPONSE['not_found'].format(data="User")
                    }
                }, status.HTTP_403_FORBIDDEN
            )

        # This checks the request body for a text field. This is required to update
        # a comment.
        if 'text' not in request.data:
            return Response(
                {
                    "errors": {
                        "text": RESPONSE['no_field'].format('text')
                    }
                }, status.HTTP_400_BAD_REQUEST
            )

        # This checks the request body for a non empty value in the text field.
        if request.data['text'] == "":
            return Response(
                {
                    "errors": {
                        "text": RESPONSE['empty_field'].format('text')
                    }
                }, status.HTTP_400_BAD_REQUEST
            )

        # This is responsible for mapping the text value we have provided to the
        # comment text value in order to update the comment.
        comment_serializer = CommentSerializer(
            comment,
            data=request.data,
            partial=True
        )

        # This ensures the current comment values conform to the validation
        # checks for a comment.
        if not comment_serializer.is_valid():
            return Response(
                {
                    "user": comment_serializer.errors
                }, status.HTTP_400_BAD_REQUEST
            )

        # This is responsible for saving the current comment data, thus updating
        # the comment.
        comment.save()

        return Response(
            {
                "user": {
                    "comment": RESPONSE['comment']['update_success']
                }
            }, status.HTTP_200_OK
        )

    def delete(self, request, *args, **kwargs):
        """
        This is the delete comment endpoint.
        """

        # We need to get the comment id from the url parameter.
        comment_id = kwargs["pk"]

        # This tries to fetch a comment from the database. If the comment
        # id provided does not match any in the database, an error 404 response
        # is sent back to the API user.
        comment = get_object_or_404(Comment.objects.all(), id=comment_id)

        # This tries to ensure that the current logged in user is the owner of
        # the comment, and has the authority to delete the comment. If this check
        # fails, we inform the user that this action is forbidden.
        if comment.user.id != request.user.id:
            return Response(
                {
                    "errors": {
                        "user": RESPONSE['not_found'].format(data="User")
                    }
                }, 403
            )

        # This is responsible for deleting the comment from the database.
        comment.delete()

        return Response(
            {
                "comment": RESPONSE['comment']['delete_success']
            }, 200
        )
