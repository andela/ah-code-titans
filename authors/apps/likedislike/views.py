from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.contenttypes.models import ContentType
from authors.apps.articles.models import Article

from .serializers import ArticleLikeDislikeSerializer
from .models import ArticleLikeDislike


class ArticleLikeDislikeView(CreateAPIView):
    """
    View class for liking and disliking of articles
    """
    # Require that the user be logged in to like/dislike
    permission_classes = (IsAuthenticated,)

    # Set the serializer for this view
    serializer_class = ArticleLikeDislikeSerializer

    # Set the the model for this view
    model = Article

    # Vote type can either be a Like or Dislike
    vote_type = None

    def post(self, request, slug):
        """
        Method to create a new like or dislike
        """
        # Search for article using its slug
        # Return a 404 if it does not exist
        obj = get_object_or_404(Article, slug=slug)

        try:
            # Check if the article has already been liked/disliked by user.
            # Filter by ContentType instance representing our Article model,
            # the id of our article object,
            # and the current user
            like_dislike = ArticleLikeDislike.objects.get(
                content_type=ContentType.objects.get_for_model(obj),
                object_id=obj.id,
                user=request.user
            )

            # Flip the votes if the incoming vote is a different one
            # update_fieids allows us to change just the votes field
            if like_dislike.vote is not self.vote_type:
                like_dislike.vote = self.vote_type
                like_dislike.save(update_fields=['vote'])
            else:
                # The existing vote record is deleted if the user is submitting a vote twice,
                # a user can hit like/dislike twice to remove their opinion
                like_dislike.delete()

        except ArticleLikeDislike.DoesNotExist:
            # If the article has never received a vote
            # create a new vote
            obj.votes.create(user=request.user, vote=self.vote_type)

        # Let's return some confirmation data
        # along with a response status
        return Response({
            "article_slug": slug,
            "article_id": obj.id,
            "total_likes": obj.votes.likes().count(),
            "total_dislikes": obj.votes.dislikes().count(),
            "total_votes": obj.votes.sum_rating(),
        },
            status=status.HTTP_201_CREATED
        )