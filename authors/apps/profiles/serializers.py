
from rest_framework import serializers
from ..followers.models import Follower

from .models import Profile


class GetProfileSerializer(serializers.ModelSerializer):
    """
    serializers for user profile upon user registration.
    """

    username = serializers.CharField(source='user.username')
    following = serializers.SerializerMethodField()

    class Meta:
        model = Profile

        fields = ('username', 'bio', 'image', 'company', 'website', 'location', 'phone', 'following')
        read_only_fields = ("created_at", "updated_at")

    def get_following(self, username):
        request = self.context.get('request')
        profile_owner = username.id
        user = request.user.id
        following = Follower.objects.filter(user=user, followed=profile_owner).exists()
        return following


class UpdateProfileSerializer(serializers.ModelSerializer):
    """
    serializers for user profile upon user registration.
    """

    class Meta:
        model = Profile

        fields = ('bio', 'image', 'company', 'website', 'location', 'phone')
        read_only_fields = ("created_at", "updated_at")

    def update(self, instance, validated_data):
        """
        Update profile function.
        """
        instance.bio = validated_data.get('bio', instance.bio)
        instance.image = validated_data.get('image', instance.image)
        instance.company = validated_data.get('company', instance.company)
        instance.website = validated_data.get('website', instance.website)
        instance.location = validated_data.get('location', instance.location)
        instance.phone = validated_data.get('phone', instance.phone)

        instance.save()
        return instance
