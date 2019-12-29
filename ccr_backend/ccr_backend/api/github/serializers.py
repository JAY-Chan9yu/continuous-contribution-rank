from rest_framework import serializers

from apps.github.models import GitHubAddress, GitHubCommit


class GitHubAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = GitHubAddress
        fields = ['id', 'name']


class GitHubCommitSerializer(serializers.ModelSerializer):

    class Meta:
        model = GitHubCommit
        fields = ['id', 'address', 'last_commit', 'total_commit', 'continuous_commit', 'max_continuous_commit']

    def to_representation(self, instance):
        ret = super(GitHubCommitSerializer, self).to_representation(instance)
        ret['address'] = GitHubAddressSerializer(instance.address).data.get('name')
        return ret

