from django.urls import path

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView,
    RequestResetAPIView, ResetPasswordAPIView, ActivateAccountAPIView, SocialAuthView,
    SocialAuthErrorView, SocialAuthNewUserView, RefreshTokenAPIView
)


urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view()),
    path('users/', RegistrationAPIView.as_view(), name="create_user"),
    path('users/login', LoginAPIView.as_view(), name="user_login"),
    path('token/refresh', RefreshTokenAPIView.as_view(), name="token_refresh"),
    path("resetrequest", RequestResetAPIView.as_view(), name="reset_request"),
    path("change_password/<str:token>",
         ResetPasswordAPIView.as_view(), name='reset_password'),
    path(
        "activate/account/<str:pk>/<str:token>",
        ActivateAccountAPIView.as_view(), name="activate_account"
    ),
    path("auth/social", SocialAuthView.as_view(), name="social_auth"),
    path("auth/social/new", SocialAuthNewUserView.as_view(), name="social_auth_new_user"),
    path("auth/social/error", SocialAuthErrorView.as_view(), name="social_auth_error")
]
