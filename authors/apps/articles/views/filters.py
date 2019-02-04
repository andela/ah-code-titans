
import django_filters as filters

from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter

from authors.apps.articles.models import Article
from authors.apps.articles.serializers import GetArticlesSerializer


class ArticleFilterView(filters.FilterSet):
    """
    Filterset class for article search and filter.
    """
    title = filters.CharFilter(
        field_name='title',
        lookup_expr='iexact'
    )
    author = filters.CharFilter(
        field_name='author__username',
        lookup_expr='iexact'
    )

    class Meta:
        model = Article
        fields = ['title', 'author']


class ArticleSearchListAPIView(ListAPIView):
    """
    View class for article search and filter
    using title and author.
    """
    serializer_class = GetArticlesSerializer

    filter_backends = (filters.rest_framework.DjangoFilterBackend, SearchFilter)
    filterset_class = ArticleFilterView
    search_fields = ('title', 'author__username')

    def get_queryset(self):
        tags = self.request.query_params.get('tags', '')
        author = self.request.query_params.get('author', '')

        if(tags == ""):
            return Article.objects.all()

        tag_list = tags.split(",")
        articles = Article.objects.all()

        if tag_list:
            for tag in tag_list:
                articles = articles.filter(tag_list__name=tag)

        if author:
            articles = articles.filter(author__username=author)

        return articles
