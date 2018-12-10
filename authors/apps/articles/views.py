# from django.shortcuts import render
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import ArticlesSerializer

from .models import Article


# Create your views here.


class ArticlesViews(CreateAPIView):
    """
    create a new article
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = request.data.get("article", {})
        context = {'request': request}
        serializer = ArticlesSerializer(data=data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Article created successfully"}, status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleView(RetrieveUpdateDestroyAPIView):
    """
    get, update, delete a specific article view
    """
    permission_classes = (IsAuthenticated,)

    def put(self, request, pk):
        """
        update a specific article
        an author can only update his/her article
        """
        article = Article.objects.get(pk=pk)

        if request.user.id != article.author_id:

            return Response({
                "message": "you are not allowed to perform this action"
            },
                status=status.HTTP_403_FORBIDDEN
            )
        data = request.data.get("article")
        serializer = ArticlesSerializer(
            instance=article, data=data, partial=True)
        serializer.is_valid()
        serializer.save()
        return Response({
            "message": "article updated successfully"
        },
            status=status.HTTP_200_OK
        )

    def delete(self, request, pk):
        """
        delete a specific article
        an author can only delete his/her article
        """
        article = Article.objects.get(pk=pk)
        serializer = ArticlesSerializer(instance=article)
        if request.user.id != article.author_id:
            return Response({
                "message": "you are not allowed to perform this action"
            },
                status=status.HTTP_403_FORBIDDEN
            )
        return Response({"article": "deleted successfully"}, status=status.HTTP_200_OK)

    def get(self, pk):
        """
        get a specific article
        anyone can get an article
        """
        article = Article.objects.get(pk=pk)
        serializer = ArticlesSerializer(instance=article)

        return Response({"article": serializer}, status=status.HTTP_200_OK)
