from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.response import Response

from api.github.serializers import GitHubAddressSerializer
from apps.github.models import GitHubAddress
from task.crawling_git import update_commit_history, say_hello


class GitHubAddressViewSet(viewsets.ModelViewSet):
    queryset = GitHubAddress.objects.all()
    serializer_class = GitHubAddressSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        result = serializer.save()
        return result

    def create(self, request, *args, **kwargs):
        github_address = request.data
        serializer = self.get_serializer(data=github_address)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        result = self.perform_create(serializer)
        update_commit_history.delay(result.id)
        return Response(self.get_serializer(result).data, status=status.HTTP_201_CREATED)


