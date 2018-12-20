from django.urls import path

from .views import articles, comments, share
from ..rating.views import RateArticleView, GetArticleRatingsView
from ...apps.favorite.views import FavoriteView, GetAllFavorites
from ...apps.bookmark.views import BookmarkArticleView, GetAllBoookmarksView

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
    path("article/<str:slug>/rating", GetArticleRatingsView.as_view(), name="rated_article"),
    path("article/<str:slug>/share/<str:provider>", share.ShareArticleView.as_view(), name="share_article"),
    path("article/<str:slug>/favorite", FavoriteView.as_view(), name="favorite"),
    path("articles/all/favorites", GetAllFavorites.as_view(), name="favorites"),
    path("article/<str:slug>/bookmark", BookmarkArticleView.as_view(), name="bookmark"),
    path("articles/all/bookmarks", GetAllBoookmarksView.as_view(), name="all_bookmarks")
]
