from django.urls import path

from .views import ReadStatsView, ReadCompleteView

urlpatterns = [
    path("read-stats", ReadStatsView.as_view(), name="user_read_stats"),
    path("read/<str:slug>", ReadCompleteView.as_view(), name="article_read"),
]
