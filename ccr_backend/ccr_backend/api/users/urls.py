# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from api.users.views import UserInformationViewSet, UserRegisterGitHubViewSet, GitHubLoginViewSet

# TODO: view method define 정리하기
urlpatterns = [
    url(r'^inform/$', UserInformationViewSet.as_view({'get': 'list', 'post': 'create'}), name='information'),
    url(r'^(?P<user_id>\d+)/github/$', UserRegisterGitHubViewSet.as_view({'get': 'list', 'post': 'create'}), name='user_github'),
    url(r'^github/$', GitHubLoginViewSet.as_view({'get': 'list', 'post': 'create'}), name='github'),
]
