# -*- coding: utf-8 -*-
# @Time    : 1/26/2018 10:18 AM
# @Author  : Abbott
# @Site    : 
# @File    : urls.py
# @Software: PyCharm

from django.conf.urls import url

from user_center.views import userprofile, usergroups
from user_center.views import permission
from user_center.views import roles

from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^user-list.html$', userprofile.UserProfileListView.as_view(), name='user_center-user-list'),
    url(r'^users.html$', userprofile.UserJsonView.as_view(), name='user_center-users'),
    url(r'^edit-user-(?P<user_id>\d+).html$', userprofile.UpdateUserView.as_view(), name='user_center-edit-user'),

    url(r'^group-list.html$', usergroups.GroupProfileListView.as_view(), name='user_center-group-list'),
    url(r'^groups.html$', usergroups.GroupJsonView.as_view(), name='user_center-groups'),
    url(r'^add-group.html$', usergroups.AddGroupView.as_view(), name='user_center-add-group'),
    url(r'^edit-group-(?P<group_id>\d+).html$', usergroups.UpdateGroupView.as_view(), name='user_center-edit-group'),

    url(r'^permission-list.html$', permission.PermissionListView.as_view(), name='user_center-permission-list'),
    url(r'^permission-json.html$', permission.PermissionJsonView.as_view(), name='user_center-permission-json'),
    url(r'^permission-add.html$', permission.PermissionAddView.as_view(), name='user_center-permission-add'),
    url(r'^permission-edit-(?P<url_nid>\d+).html$', permission.PermissionUpdateView.as_view(), name='user_center-permission-edit'),

    url(r'^roles-list.html$', roles.RolesListView.as_view(), name='user_center-roles-list'),
    url(r'^roles-json.html$', roles.RolesJsonView.as_view(), name='user_center-roles-json'),
    url(r'^roles-add.html$', roles.RolesAddView.as_view(), name='user_center-roles-add'),
    url(r'^roles-edit-(?P<role_nid>\d+).html$', roles.RolesUpdateView.as_view(), name='user_center-roles-edit'),

]
