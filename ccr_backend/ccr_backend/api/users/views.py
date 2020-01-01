from django.conf import settings
from rest_framework import viewsets
from rest_framework.response import Response

from api.users.serializers import UserSerializer, UserGitHubSerializer
from apps.users.models import User, UserGitHub


class UserInformationViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        response = Response(serializer.data, content_type='application/json')

        return response

    def perform_create(self, serializer):
        result = serializer.save()
        return result


class UserRegisterGitHubViewSet(viewsets.ModelViewSet, viewsets.ViewSetMixin):
    """
        User 의 github 주소, contribution count 관한 api
    """

    queryset = UserGitHub.objects.all()
    serializer_class = UserGitHubSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = UserGitHubSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        result = serializer.save()
        return result


class GitHubLoginViewSet(viewsets.ModelViewSet, viewsets.ViewSetMixin):
    """
        User 의 github 주소, contribution count 관한 api
    """
    queryset = UserGitHub.objects.all()
    serializer_class = UserGitHubSerializer

    def list(self, request, *args, **kwargs):
        rl = settings.GITHUB_AUTH_URL.format(
            settings.GITHUB_HOST,
            settings.GITHUB_CLIENT_ID,
            'user:email'
        )
        response = Response(rl, content_type='application/json')

        return response

