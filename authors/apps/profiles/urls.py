
from django.urls import path


# local imports
from .views import GetUserProfileView, UpdateUserProfileView


urlpatterns = [
    path('profiles/<str:username>', GetUserProfileView.as_view(), name='profile'),
    path('profiles/edit/<str:username>', UpdateUserProfileView.as_view(), name='update_profile')
]
