from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.generics import ListAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# local imports
from .models import Profile
from .serializers import GetProfileSerializer, UpdateProfileSerializer
from .renderers import ProfileJSONRenderer


class GetUserProfileView(RetrieveAPIView):
    """
    Authenticated users can view their own profile and other user's profile.
    """
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = GetProfileSerializer

    def get_queryset(self):
        try:
            profile = Profile.objects.select_related('user').get(
                user__username=self.kwargs.get('username')
            )
            return profile
        except Exception:

            raise NotFound('User profile not found')

    def retrieve(self, request, **kwargs):
        data = self.get_queryset()
        serializer = self.serializer_class(data, context={'request': request})

        return Response(serializer.data)


class AuthorsProfileListAPIView(ListAPIView):
    """
    Gets a list of authors profiles
    """

    permission_classes = (IsAuthenticated,)
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = GetProfileSerializer
    queryset = Profile.objects.all()


class UpdateUserProfileView(UpdateAPIView):
    """
    Enables a user to edit own profile but can not edit another user's profile.

    """
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = UpdateProfileSerializer
    queryset = Profile.objects.all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.select_related('user').get(
            user__username=self.request.user.username
        )
        return obj

    def put(self, request, username):
        if request.user.username != username:
            raise PermissionDenied('Edit permission denied')

        else:

            return super().put(request, username)
