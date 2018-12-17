from django.urls import path

from .views import ArticlesViews, ArticleView, GetArticles, CommentsView, CommentView
from .views import ArticlesViews, ArticleView
from ..rating.views import RateArticleView, GetArticleRatingsView

urlpatterns = [
    path("articles/", ArticlesViews.as_view(), name="articles"),
    path("article/<str:slug>", ArticleView.as_view(), name="article"),
    path("articles/all", GetArticles.as_view(), name="all_articles"),
    path("articles/<str:slug>/comments",
         CommentsView.as_view(), name="article_comments"),
    path("articles/<str:slug>/comments/<int:offset>",
         CommentsView.as_view(), name="article_comments_list"),
    path("articles/<str:slug>/comment/<int:pk>",
         CommentView.as_view(), name="article_comment"),
    path("articles/<str:slug>/comment/<int:pk>/<int:offset>",
         CommentView.as_view(), name="article_comment_replies"),
    path("article/<str:slug>/rate", RateArticleView.as_view(), name="rate_article"),
    path("article/<str:slug>/rating", GetArticleRatingsView.as_view(), name="rated_article")
]
