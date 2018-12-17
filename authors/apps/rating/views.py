from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import RateArticleSerializer

# Create your views here.


class RateArticleView(CreateAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = RateArticleSerializer

    """
    View to add ratings to an article
    """
    def post(self, request, slug):

        # Pick user rating information
        user_data = request.data.get('article')

        # Make a query with the slug and return article id
        # else tell user article was not found.
        to_rate = RateArticleSerializer().get_article_to_rate(slug=slug)

        # Pass the data to the serializer
        self.serializer_class.rate_article(
            data=user_data,
            user_id=request.user.id,
            article_id=to_rate.id)

        # Return response to user
        return Response(
            {"message": "Successfully rated the article"},
            status=status.HTTP_201_CREATED)


class GetArticleRatingsView(RetrieveAPIView):
    serializer_class = RateArticleSerializer
    permission_classes = (AllowAny,)

    """
    View to return current ratings on an article
    """
    def get(self, request, slug):

        # Retrieve the current rate
        current_rate = self.serializer_class.get_rating_per_article(
            slug=slug
        )

        # Return response to user
        return Response({"Rated at": current_rate}, status=status.HTTP_200_OK)
