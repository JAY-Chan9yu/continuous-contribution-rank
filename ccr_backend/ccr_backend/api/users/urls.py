# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from api.users.views import UserInformationViewSet, UserRegisterGitHubViewSet, GitHubLoginViewSet

information = UserInformationViewSet.as_view({
    'get': 'list', 'post': 'create'
})

user_github = UserRegisterGitHubViewSet.as_view({
    'get': 'list', 'post': 'create'
})

github = GitHubLoginViewSet.as_view({
    'get': 'list', 'post': 'create'
})

urlpatterns = [
    url(r'^inform/$', information, name='information'),
    url(r'^(?P<user_id>\d+)/github/$', user_github, name='user_github'),
    url(r'^github/$', github, name='github'),
]
