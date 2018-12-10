
# import datetime
from rest_framework import serializers


from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """
    serializers for user profile upon user registration.
    """

    bio = serializers.CharField(allow_blank=True, required=False)
    image = serializers.SerializerMethodField()
    company = serializers.CharField(allow_blank=True, required=False)
    website = serializers.CharField(allow_blank=True, required=False)
    location = serializers.CharField(allow_blank=True, required=False)
    phone = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = Profile

        fields = ('bio', 'image', 'company', 'website', 'location', 'phone')
        read_only_fields = ("username", "created_at", "updated_at")

    def get_image(self, obj):
        if obj.image:
            return obj.image

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
