from django.urls import path

from .views import (
    LoginAPIView,
    RegistrationAPIView,
    UserRetrieveUpdateAPIView,
    SocialAuthenticationAPIView
)

urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view()),
    path('users/', RegistrationAPIView.as_view(), name="create_user"),
    path('users/login', LoginAPIView.as_view(), name="user_login"),
    path('users/login/social', SocialAuthenticationAPIView.as_view(), name="social_login")
]
