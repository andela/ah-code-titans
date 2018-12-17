from rest_framework import serializers

from .models import Follower


class FollowerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follower
        fields = ['user', 'followed']
        read_only = ('followed_at',)

    def create(self, validated_data):
        """
        Creates a record that depicts one user following another user
        :param validated_data:
        :return:
        """
        return Follower.objects.create(**validated_data)
