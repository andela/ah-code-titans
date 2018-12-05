from rest_framework import status
from rest_framework.generics import (
    RetrieveUpdateAPIView, CreateAPIView, UpdateAPIView
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.core.mail import send_mail

from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer,
    ResetSerializer
)
from ...settings import EMAIL_HOST_USER
from .backends import Authentication
from .models import User


class RegistrationAPIView(CreateAPIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})
        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})

        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't actually have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})

        # Here is that serialize, validate, save pattern we talked about
        # before.
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class RequestResetAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = ResetSerializer

    def post(self, request):
        user_data = request.data['user']

        serializer = self.serializer_class(data=user_data)
        serializer.is_valid(raise_exception=True)

        # Pick the token from data
        token = serializer.data.get('token')

        # Format the email
        host = request.get_host()
        if request.is_secure():
            protocol = "https://"
        else:
            protocol = "http://"
        resetpage = protocol + host + '/api/resetpassword/' + token
        subject = "Password Reset Request"
        message = (
            "Hello {user_data} you have requested for a password reset.\n"
            "If you wish to continue please press this link below\n\n{link}\n\n "
            "Else ignore this request.\n "
            "The link expires in 1 hour".format(user_data=user_data['email'], link=resetpage))
        from_email = EMAIL_HOST_USER
        to_list = [user_data['email'], EMAIL_HOST_USER]

        # Send the email
        send_mail(
            subject,
            message,
            from_email,
            to_list, fail_silently=True
        )

        # Respond back to the user
        return Response(
            {"message": "Check your email for the link",
                "linker": resetpage},
            status=status.HTTP_200_OK)


class ResetPasswordAPIView(UpdateAPIView):
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer
    validation_checker = RegistrationSerializer

    def put(self, request, token, **kwargs):
        # Decode token
        decoded = Authentication.decode_jwt_token(token)

        # Validate the data
        self.validation_checker.validate_password(
            None,
            request.data['user']['password'])

        # Find the user instance with the the decoded username
        user = User.objects.get(username=decoded['username'])

        # Update the password
        self.serializer_class.update(
            None,
            user,
            {
                "password": request.data['user']['password']
            }
        )

        # Respond back to the user
        return Response(
            {"message": "Your password was successfully changed"},
            status=status.HTTP_200_OK)
