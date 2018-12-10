from django.urls import path
from .views import ArticlesViews, ArticleView

urlpatterns = [
    path("articles/", ArticlesViews.as_view(), name="articles"),
    path("article/<int:pk>", ArticleView.as_view(), name="article"),

]
