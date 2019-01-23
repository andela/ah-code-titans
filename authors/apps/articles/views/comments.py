from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.shortcuts import get_object_or_404

from ..serializers import CommentSerializer, CommentHistorySerializer, CreateCommentSerializer
from ..models import Comment, Article, CommentHistory
from ..renderers import CommentHistoryJSONRenderer
from authors.response import RESPONSE


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
        article_exists = check_if_article_exists(article_slug)

        if isinstance(article_exists, Response):
            return article_exists

        # This tries to fetch a list of reply comments for the specified comment,
        # from the database. If the comment id provided does not match any in
        # the database, an error 404 response is sent back to the API user.
        comments = get_comments(
            article_slug=article_slug,
            comment_id=0,
            offset=offset,
            page_size=page_size
        )

        if isinstance(comments, Response):
            return comments

        serializer = CommentSerializer(comments, many=True)

        return Response(
            {
                "comments": serializer.data,
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

        comment_serializer = CreateCommentSerializer(data=comment)

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
        article_slug = kwargs["slug"]

        page_size = 20
        offset = kwargs["offset"]

        # This checks if the article slug provided matches any article in the database.
        article_exists = check_if_article_exists(article_slug)

        if isinstance(article_exists, Response):
            return article_exists

        # This tries to fetch a list of reply comments for the specified comment,
        # from the database. If the comment id provided does not match any in
        # the database, an error 404 response is sent back to the API user.
        comments = get_comments(
            article_slug=article_slug,
            comment_id=comment_id,
            offset=offset,
            page_size=page_size
        )

        if isinstance(comments, Response):
            return comments

        serializer = CommentSerializer(comments, many=True)

        return Response(
            {
                "comments": serializer.data,
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

        error_response = None

        # This tries to fetch a comment from the database. If the comment
        # id provided does not match any in the database, an error 404 response
        # is sent back to the API user.
        comment = get_object_or_404(Comment.objects.all(), id=comment_id)

        # This tries to ensure that the current logged in user is the owner of
        # the comment, and has the authority to update the comment. If this check
        # fails, we inform the user that this action is forbidden.
        if comment.user.id != request.user.id:
            error_response = self.get_error_text_response(
                'forbidden',
                status.HTTP_403_FORBIDDEN
            )

        # This checks the request body for a text field. This is required to update
        # a comment.
        elif 'text' not in request.data:
            error_response = self.get_error_text_response(
                'no_field',
                status.HTTP_400_BAD_REQUEST
            )

        # This checks the request body for a non empty value in the text field.
        elif request.data['text'] == "":
            error_response = self.get_error_text_response(
                'empty_field',
                status.HTTP_400_BAD_REQUEST
            )

        if error_response is not None:
            return Response(error_response['response'], error_response['code'])

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
        comment_serializer.save()

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

    def get_error_text_response(self, error, code):
        return {
            "response": {
                "errors": {
                    "text": RESPONSE[error].format('text')
                }
            },
            "code": code
        }


class CommentHistoryView(generics.ListAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = CommentHistorySerializer
    renderer_classes = [CommentHistoryJSONRenderer]

    def get_queryset(self):
        return CommentHistory.objects.filter(comment=self.kwargs['pk'])


def get_comments(**kwargs):
    comments = Comment.objects.filter(
        article__slug=kwargs['article_slug'],
        parent=kwargs['comment_id']
    )[kwargs['offset']:kwargs['offset'] + kwargs['page_size']]

    if not comments:
        return Response(
            {
                "errors": {
                    "comments": RESPONSE['not_found'].format(data="Comments")
                }
            }, status.HTTP_404_NOT_FOUND
        )

    return comments


def check_if_article_exists(article_slug):
    if not Article.objects.filter(slug=article_slug).exists():
        return Response(
            {
                "errors": {
                    "article": RESPONSE['not_found'].format(data="Article")
                }
            }, status.HTTP_404_NOT_FOUND
        )

    return True
