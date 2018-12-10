from django.urls import path

from .views import ArticlesViews, ArticleView, GetArticles, CommentsView, CommentView

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
]
