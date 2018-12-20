from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import UserReadStat
from authors.response import RESPONSE
from .serializers import UserReadStatSerializer


class ReadStatsView(ListAPIView):
    serializer_class = UserReadStatSerializer

    def get_queryset(self):
        """
        read all the articles read by a user
        """
        return UserReadStat.objects.filter(user=self.request.user)


class ReadCompleteView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, slug):
        """
        we are updating read status to true
        """
        try:
            user_read_stat = UserReadStat.objects.get(article__slug=slug)
        except UserReadStat.DoesNotExist:
            return Response(
                {
                    "errors": {
                        "article": RESPONSE['not_found'].format(data="User read stat")
                    }
                }, status.HTTP_404_NOT_FOUND
            )

        if user_read_stat.read:
            return Response({
                "errors": {
                    "article": "Article has already been read!"
                }
            }, status.HTTP_403_FORBIDDEN
            )

        user_read_stat.read = True
        user_read_stat.save()

        return Response(
            {
                "message": "Article Read!"
            }, status.HTTP_200_OK
        )
