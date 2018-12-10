
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied


# local imports
from .models import Profile
from .serializers import ProfileSerializer


class GetUserProfile(RetrieveAPIView):
    """
    Authenticated users can view their own profile and other user's profile.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer
    lookup_field = 'username'
    queryset = Profile.objects.all()


class UpdateUserProfile(UpdateAPIView):
    """
    Enables a user to edit own profile but can not edit another user's profile.

    """
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    lookup_field = 'username'

    def put(self, request, username):
        if request.user.username != username:
            raise PermissionDenied('Edit permission denied')

        else:
            return super().put(request, username)
