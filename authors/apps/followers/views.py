from django.http import JsonResponse
from rest_framework.exceptions import NotFound
from rest_framework.generics import (CreateAPIView, DestroyAPIView, ListAPIView)
from rest_framework.response import Response
from rest_framework import status
from ..profiles.serializers import GetProfileSerializer
from ..profiles.views import GetUserProfileView
from ..profiles.renderers import ProfileJSONRenderer
from django.db.models import F
from authors.apps.authentication.models import User
from authors.apps.profiles.models import Profile
from .models import Follower
from .serializers import FollowerSerializer
from rest_framework.permissions import IsAuthenticated


class FollowCreateAPIView(CreateAPIView, DestroyAPIView):
    """
    Authenticated users can follow or un-follow another user
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = FollowerSerializer
    renderer_classes = (ProfileJSONRenderer,)

    def post(self, request, **kwargs):
        """Follow a user"""
        username = kwargs.get('username', '')
        user_username = request.user.username
        if username == user_username:
            return Response(
                {'message': "You can't follow yourself"},
                status.HTTP_406_NOT_ACCEPTABLE
            )
        followed = check_user(username)

        data = {'user': request.user.id, 'followed': followed}

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        profile = GetUserProfileView.get_queryset(self)
        profile = GetProfileSerializer(profile, context={'request': request})

        return Response(profile.data, status.HTTP_201_CREATED)

    def delete(self, request, **kwargs):
        """Un-follow a user"""
        username = kwargs.get('username', '')
        user_username = request.user.username
        if username == user_username:
            return Response(
                {'message': "You can't un-follow yourself"},
                status.HTTP_406_NOT_ACCEPTABLE
            )

        followed = check_user(username)

        instance = Follower.objects.filter(user=request.user.id, followed=followed)
        self.perform_destroy(instance)

        profile = GetUserProfileView.get_queryset(self)
        profile = GetProfileSerializer(profile, context={'request': request})

        return Response(profile.data, status.HTTP_204_NO_CONTENT)


class FollowersListAPIView(ListAPIView):
    """
    Authenticated users can view their list of followers
    """
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Follower.objects.filter(followed=self.request.user.id)

    def get(self, request, *args, **kwargs):
        data = follow_list(self, 'user')
        return JsonResponse({'followers': list(data)})


class FollowingListAPIView(ListAPIView):
    """
    Authenticated users can view a list of those they follow
    """
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Follower.objects.filter(user=self.request.user.id)

    def get(self, request, *args, **kwargs):
        data = follow_list(self, 'followed')
        return JsonResponse({'following': list(data)})


def follow_list(self, user):
    data = self.get_queryset().values(user)
    data = Profile.objects.filter(pk__in=data).values()
    data = data.values(
        username=F('user__username'),
        bio=F('bio'),
        image=F('image')
    )
    return data


def check_user(username):
    try:
        followed = User.objects.get(username=username).id
    except User.DoesNotExist:
        raise NotFound('User not found')

    return followed
