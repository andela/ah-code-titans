from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from social_django.utils import load_backend, load_strategy
from social_core.exceptions import AuthAlreadyAssociated
from social_core.backends.oauth import BaseOAuth1, BaseOAuth2

from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer,
    RegistrationSerializer,
    UserSerializer,
    SocialAuthenticationSerializer
)
from .models import User
from .backends import Authentication


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


class SocialAuthenticationAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = SocialAuthenticationSerializer

    def create(self, request, *args, **kwargs):
        """
        This endpoint is responsible for the retrieval of the user's social
        media access token which is required for accessing the social media
        API resources.
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        """
        Checks if a user has already been logged in. If so, it still shall
        be passed to the Facebook API for token refreshing.
        """
        authed_user = request.user if not request.user.is_anonymous else None

        strategy = load_strategy(request)

        """
        Gets the backend from the social auth library responsible for forwarding
        the token request according to the provider set as 'name'.
        """
        backend = load_backend(
            strategy=strategy,
            name=request.data['provider'],
            redirect_uri=None
        )

        if isinstance(backend, BaseOAuth1):
            """
            This handles a provider's authentication type of BASEOAuth1 to ensure
            the API is forward the required details for such an authentication type.
            """
            token = {
                "oauth_token": serializer.data['authentication_token'],
                "oauth_token_secret": serializer.data[
                    'authentication_token_secret'
                ]
            }

        elif isinstance(backend, BaseOAuth2):
            """
            This handles a provider's authentication type of BaseOAuth2 to ensure
            the API is forward the required details for such an authentication type.
            """
            token = serializer.data['authentication_token']

        try:
            """
            This is where the forwarding of the API request for the access token is
            generated and executed.
            """
            user = backend.do_auth(token, user=authed_user)

        except AuthAlreadyAssociated:
            """
            This error is caused when the user has already been logged in using the
            specified provider.
            """
            return Response(
                {
                    "errors": {
                        "user": "The user is already registered!"
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if user and user.is_active:

            user_serializer = UserSerializer(user)
            user.is_verified = True

            auth_token = user.social_auth.get(
                provider=request.data['provider']
            )

            if not auth_token.extra_data['access_token']:
                """
                It is expected that in the response body received, we have an
                'access_token' value that shall be used to access the resources
                provided by the social media apps. If not found, we have to set
                a default token, which is the dict variable 'token' defined
                above.
                """
                auth_token.extra_data['access_token'] = token
                auth_token.save()

                user_serializer.save()
                user.save()

            user = User.objects.get(email=user_serializer.data['email'])

            """
            Here, the jwt token is generated. The app uses this token as opposed
            to the one provided by the social media API resources.
            """
            jwt_token = Authentication.generate_jwt_token(user.json())

            user_serializer.instance = user
            return Response(
                {
                    "user": {
                        "id": user.id,
                        "username": user_serializer.data['username'],
                        "email": user_serializer.data['email']
                    },
                    "token": jwt_token
                },
                status=status.HTTP_201_CREATED,
                headers=self.get_success_headers(user_serializer.data)
            )

        else:
            """
            This is executed when the social media backend is unable to provide
            the user's details from the social media API resource. The user variable
            is of the NoneType when this happens.
            """
            return Response(
                {
                    "errors": {
                        "user": "Failed to authenticate user. Please try again!"
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )
