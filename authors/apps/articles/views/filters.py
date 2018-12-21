from django_filters import rest_framework as filters

from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter

from authors.apps.articles.models import Article
from authors.apps.articles.serializers import GetArticlesSerializer


class ArticleFilterView(filters.FilterSet):
    """
    Filterset class for article search and filter.
    """

    title = filters.CharFilter(field_name='title', lookup_expr='iexact')
    author = filters.CharFilter(field_name='author__username', lookup_expr='iexact')

    class Meta:
        model = Article
        fields = ['title', 'author']


class ArticleSearchListAPIView(ListAPIView):
    """
    View class for article search and filter
    using title and author.
    """
    queryset = Article.objects.all()
    serializer_class = GetArticlesSerializer

    filter_backends = (filters.DjangoFilterBackend, SearchFilter)
    filterset_class = ArticleFilterView
    search_fields = ('title', 'author__username')


class ArticleTagSearchAPIView(ListAPIView):
    """
    View class for articles filter using tags.
    """
    serializer_class = GetArticlesSerializer

    def get_queryset(self):
        tags = self.request.query_params.get('tags', '')
        tag_list = tags.split(",")

        if tag_list:
            return Article.objects.filter(tag_list__name__in=tag_list)
