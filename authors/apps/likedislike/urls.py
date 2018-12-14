from django.urls import path

from .views import ArticleLikeDislikeView
from .models import ArticleLikeDislike
from authors.apps.articles.models import Article


urlpatterns = [
    path('articles/<slug>/like/',
         ArticleLikeDislikeView.as_view(model=Article, vote_type=ArticleLikeDislike.LIKE), name='article-like'),
    path('articles/<slug>/dislike/',
         ArticleLikeDislikeView.as_view(model=Article, vote_type=ArticleLikeDislike.DISLIKE), name='article-dislike'),
]
