import datetime
import json

import requests
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.response import Response

from api.github.pagination import CustomCursorPagination
from api.github.serializers import GitHubAddressSerializer, GitHubCommitSerializer
from apps.github.models import GitHubAddress, GitHubCommit
from task.crawling_git import update_commit_history


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
        code = request.GET.get('code')

        # TODO: 로직 정리하기
        # 1. github 에서 access_token 을 가져온다.
        url = settings.GITHUB_ACCESS_TOKEN_URL.format(
            settings.GITHUB_CLIENT_ID,
            settings.GITHUB_CLIENT_SECRET,
            code
        )

        headers = {'Accept': 'application/json'}
        res = requests.post(url, headers=headers)
        data = json.loads(res.content)
        access_token = data.get('access_token')
        if access_token is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # 2. oauth 인증한 user 의 정보를 가져온다.
        headers = {'Authorization': 'token {}'.format(access_token)}
        url = settings.GITHUB_USER_URL
        res = requests.get(url, headers=headers)
        data = json.loads(res.content)

        github_data = {
            'name': data.get('login')
        }
        serializer = self.get_serializer(data=github_data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # GitHub address 등록
        result = self.perform_create(serializer)

        # GitHub Commit 기록 모델 생성
        utc_now = datetime.datetime.utcnow()
        github_commit = GitHubCommit.objects.create(
            created=utc_now,
            address=result
        )

        # worker 에서 기본 github 내용 크롤링
        update_commit_history.delay(github_commit.id)

        return Response(self.get_serializer(result).data, status=status.HTTP_201_CREATED)


class GitHubCommitViewSet(viewsets.ModelViewSet):
    queryset = GitHubCommit.objects.all()
    serializer_class = GitHubCommitSerializer
    pagination_class = CustomCursorPagination

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        self.pagination_class.cursor = self.request.query_params.get('cursor')
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(serializer.data)
