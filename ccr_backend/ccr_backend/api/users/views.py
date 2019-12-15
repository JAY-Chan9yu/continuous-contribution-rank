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
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        pass


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
