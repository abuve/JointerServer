# -*- coding: utf-8 -*-
# @Time    : 1/26/2018 10:25 AM
# @Author  : Abbott
# @Site    : 
# @File    : userprofile.py
# @Software: PyCharm

import json
from django.views import View
from django.shortcuts import render
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse


from user_center.service import usergroups



class GroupProfileListView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'user_center/group_list.html')


class GroupJsonView(View):
    def post(self, request):
        response = usergroups.UserGroups.add_data(request)
        return HttpResponseRedirect('/user_center/group-list.html')

    def get(self, request):
        obj = usergroups.UserGroups()
        response = obj.fetch_group(request)
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = usergroups.UserGroups.delete_data(request)
        return JsonResponse(response.__dict__)

    def put(self, request):
        response = usergroups.UserGroups.put_data(request)
        return JsonResponse(response.__dict__)


class AddGroupView(View):
    def get(self, request, *args, **kwargs):
        # response = usergroups.UserGroups.get_group_info(request)
        return render(request, 'user_center/add_group.html')


class UpdateGroupView(View):
    def get(self, request, group_id):
        # project_info = server_project.ServerProject.get_project_info(request)
        response = usergroups.UserGroups.group_config(group_id)
        return render(request, 'user_center/edit_group.html', {'response': response})









