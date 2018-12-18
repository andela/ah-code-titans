from django.urls import path

# local imports
from authors.apps.profiles.views import (
    AuthorsProfileListAPIView,
    GetUserProfileView,
    UpdateUserProfileView
)

urlpatterns = [
    path('profiles/', AuthorsProfileListAPIView.as_view(), name='authors_profile'),
    path('profiles/<str:username>', GetUserProfileView.as_view(), name='profile'),
    path('profiles/edit/<str:username>', UpdateUserProfileView.as_view(), name='update_profile')
]
