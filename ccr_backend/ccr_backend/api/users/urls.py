# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from api.users.views import UserInformationViewSet

urlpatterns = [
    url(r'^inform/$', UserInformationViewSet.as_view({'get': 'list', 'post': 'create'}), name='information'),
]
