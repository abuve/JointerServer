#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from django.views import View
from django.shortcuts import render
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from utils.mixin_utils import LoginRequiredMixin, PermissionRequiredMixin, WriteAccessLogsMixin

from user_center.service import permission


class PermissionListView(WriteAccessLogsMixin, LoginRequiredMixin, PermissionRequiredMixin, View):
    def get(self, request):
        #response = permission.PermissionConfig.nginx_config(server_id)
        return render(request, 'permission_list.html', {'response': 1})


class PermissionJsonView(WriteAccessLogsMixin, LoginRequiredMixin, PermissionRequiredMixin, View):
    def get(self, request):
        response = permission.PermissionConfig().fetch_data(request)
        return JsonResponse(response.__dict__)

    def post(self, request):
        response = permission.PermissionConfig.data_create(request)
        return HttpResponseRedirect('/user_center/permission-list.html')

    def put(self, request):
        response = permission.PermissionConfig.data_update(request)
        return HttpResponseRedirect('/user_center/permission-list.html')

    def delete(self, request):
        response = permission.PermissionConfig.data_delete(request)
        return JsonResponse(response.__dict__)


class PermissionAddView(WriteAccessLogsMixin, LoginRequiredMixin, PermissionRequiredMixin, View):
    def get(self, request):
        return render(request, 'permission_add.html')


class PermissionUpdateView(WriteAccessLogsMixin, LoginRequiredMixin, PermissionRequiredMixin, View):
    def get(self, request, url_nid):
        response = permission.PermissionConfig.get_data_by_id(url_nid)
        return render(request, 'permission_edit.html', {'response': response})

