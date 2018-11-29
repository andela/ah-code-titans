from django.conf.urls import url

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView
)

urlpatterns = [
    url(r'^user/?$', UserRetrieveUpdateAPIView.as_view()),
    url(r'^users/?$', RegistrationAPIView.as_view(), name="create_user"),
    url(r'^users/login/?$', LoginAPIView.as_view(), name="user_login"),
]
