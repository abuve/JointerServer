from __future__ import absolute_import, division, print_function, unicode_literals

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^login/$', views.login_sp, name='login'),
    url(r'^auth/$', views.auth, name='auth'),
    url(r'^acs', views.acs, name='acs'),
]