from rest_framework import serializers

from apps.github.models import GitHubAddress


class GitHubAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = GitHubAddress
        fields = ['id', 'name']
