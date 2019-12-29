# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from api.github.views import GitHubAddressViewSet, GitHubCommitViewSet

address = GitHubAddressViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

commit = GitHubCommitViewSet.as_view({
    'get': 'list',
})

urlpatterns = [
    url(r'^$', address, name='address'),
    url(r'^commit/$', commit, name='address'),
]
