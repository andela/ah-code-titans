from .views import (
    FollowCreateAPIView, FollowersListAPIView, FollowingListAPIView
)

from django.urls import path


urlpatterns = [
    path('profiles/<str:username>/follow', FollowCreateAPIView.as_view(), name='follow'),
    path('profiles/followers', FollowersListAPIView.as_view(), name='followers'),
    path('profiles/following', FollowingListAPIView.as_view(), name='following'),
]
