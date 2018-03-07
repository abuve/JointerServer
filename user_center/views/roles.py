#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from django.views import View
from django.shortcuts import render
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from utils.mixin_utils import LoginRequiredMixin, PermissionRequiredMixin, WriteAccessLogsMixin

from user_center.service import roles


class RolesListView(WriteAccessLogsMixin, LoginRequiredMixin, PermissionRequiredMixin, View):
    def get(self, request):
        #response = permission.PermissionConfig.nginx_config(server_id)
        return render(request, 'roles_list.html', {'response': 1})


class RolesJsonView(WriteAccessLogsMixin, LoginRequiredMixin, PermissionRequiredMixin, View):
    def get(self, request):
        response = roles.RolesConfig().fetch_data(request)
        return JsonResponse(response.__dict__)

    def post(self, request):
        response = roles.RolesConfig.data_create(request)
        return JsonResponse(response.__dict__)

    def put(self, request):
        response = roles.RolesConfig.data_update(request)
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = roles.RolesConfig.data_delete(request)
        return JsonResponse(response.__dict__)


class RolesAddView(WriteAccessLogsMixin, LoginRequiredMixin, PermissionRequiredMixin, View):
    def get(self, request):
        response = roles.RolesConfig.get_permission_data()
        return render(request, 'roles_add.html', {'response': response})


class RolesUpdateView(WriteAccessLogsMixin, LoginRequiredMixin, PermissionRequiredMixin, View):
    def get(self, request, role_nid):
        response = roles.RolesConfig.get_data_by_id(role_nid)
        return render(request, 'roles_edit.html', {'response': response})

