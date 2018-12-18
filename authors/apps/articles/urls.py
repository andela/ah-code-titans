from django.urls import path

from .views import articles, comments
from ..rating.views import RateArticleView, GetArticleRatingsView

urlpatterns = [
    path("articles/", articles.ArticlesViews.as_view(), name="articles"),
    path("article/<str:slug>", articles.ArticleView.as_view(), name="article"),
    path("articles/all", articles.GetArticles.as_view(), name="all_articles"),
    path("articles/<str:slug>/comments",
         comments.CommentsView.as_view(), name="article_comments"),
    path("articles/<str:slug>/comments/<int:offset>",
         comments.CommentsView.as_view(), name="article_comments_list"),
    path("articles/<str:slug>/comment/<int:pk>",
         comments.CommentView.as_view(), name="article_comment"),
    path("articles/<str:slug>/comment/<int:pk>/<int:offset>",
         comments.CommentView.as_view(), name="article_comment_replies"),
    path("article/<str:slug>/rate", RateArticleView.as_view(), name="rate_article"),
    path("article/<str:slug>/rating", GetArticleRatingsView.as_view(), name="rated_article")
]
