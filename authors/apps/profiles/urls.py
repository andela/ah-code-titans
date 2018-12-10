
from django.urls import path


# local imports
from .views import GetUserProfile, UpdateUserProfile


urlpatterns = [
    path('profiles/<str:username>', GetUserProfile.as_view(), name='profile'),
    path('profiles/edit/<str:username>', UpdateUserProfile.as_view(), name='update_profile')
]
