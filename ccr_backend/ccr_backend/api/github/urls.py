# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from api.github.views import GitHubAddressViewSet

address = GitHubAddressViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

urlpatterns = [
    url(r'^$', address, name='address'),
]
