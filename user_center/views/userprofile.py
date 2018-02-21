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


from user_center.service import userprofile



class UserProfileListView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'user_center/user_list.html')


class UserJsonView(View):
    def post(self, request):
        response = project.Project.add_data(request)
        return HttpResponseRedirect('/project.html')

    def get(self, request):
        obj = userprofile.UserProfile()
        response = obj.fetch_user(request)
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = userprofile.UserProfile.delete_data(request)
        return JsonResponse(response.__dict__)

    def put(self, request):
        response = userprofile.UserProfile.put_data(request)
        return JsonResponse(response.__dict__)


class AddProjectView(View):
    def get(self, request, *args, **kwargs):
        # response = server_project.ServerProject.get_project_info(request)
        return render(request, 'add_project.html')


class UpdateUserView(View):
    def get(self, request, user_id):
        # project_info = server_project.ServerProject.get_project_info(request)
        group_info = userprofile.UserProfile.get_group_info(request)
        response = userprofile.UserProfile.user_config(user_id)
        return render(request, 'user_center/edit_user.html', {'response': response, 'group_info': group_info})


