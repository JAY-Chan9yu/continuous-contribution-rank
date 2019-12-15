from rest_framework import serializers

from apps.users.models import User, UserGitHub


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username']


class UserGitHubSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserGitHub
        fields = ['id', 'user', 'address']
