# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from api.users.views import UserInformationViewSet, UserRegisterGitHubViewSet

urlpatterns = [
    url(r'^inform/$', UserInformationViewSet.as_view({'get': 'list'}), name='information'),
    url(r'^(?P<user_id>\d+)/github/$', UserRegisterGitHubViewSet.as_view({'get': 'list', 'post': 'create'}), name='github'),
]
