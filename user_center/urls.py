# -*- coding: utf-8 -*-
# @Time    : 1/26/2018 10:18 AM
# @Author  : Abbott
# @Site    : 
# @File    : urls.py
# @Software: PyCharm

from django.conf.urls import url


from user_center.views import userprofile, usergroups

from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^user-list.html$', login_required(userprofile.UserProfileListView.as_view())),
    url(r'^users.html$', login_required(userprofile.UserJsonView.as_view())),
    url(r'^edit-user-(?P<user_id>\d+).html$', login_required(userprofile.UpdateUserView.as_view())),

    url(r'^group-list.html$', login_required(usergroups.GroupProfileListView.as_view())),
    url(r'^groups.html$', login_required(usergroups.GroupJsonView.as_view())),
    url(r'^add-group.html$', login_required(usergroups.AddGroupView.as_view())),
    url(r'^edit-group-(?P<group_id>\d+).html$', login_required(usergroups.UpdateGroupView.as_view())),


]
