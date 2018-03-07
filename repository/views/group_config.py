#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from django.views import View
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from utils.mixin_utils import LoginRequiredMixin, PermissionRequiredMixin, WriteAccessLogsMixin

from repository.service import group_config


class GroupConfigView(WriteAccessLogsMixin, LoginRequiredMixin, PermissionRequiredMixin, View):
    def get(self, request, server_id):
        response = group_config.ServerGroup.get_server_groups(server_id)
        return render(request, 'server_config_group.html', {'response': response})


class GroupConfigJsonView(WriteAccessLogsMixin, LoginRequiredMixin, PermissionRequiredMixin, View):
    def get(self, request, server_id):
        response = group_config.ServerGroup.get_server_groups_json(request, server_id)
        return HttpResponse(json.dumps(response.data))


class UpdateServerGroupView(WriteAccessLogsMixin, LoginRequiredMixin, PermissionRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        response = group_config.ServerGroup.get_group_by_id(request)
        return HttpResponse(json.dumps(response))

    def post(self, request):
        response = group_config.ServerGroup.add_server_group(request)
        return JsonResponse(response.__dict__)

    def put(self, request):
        response = group_config.ServerGroup.update_server_group(request)
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = group_config.ServerGroup.delete_server_group(request)
        return JsonResponse(response.__dict__)


class UpdatePublicGroupView(WriteAccessLogsMixin, LoginRequiredMixin, PermissionRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        response = group_config.ServerGroup.get_public_group(request)
        return HttpResponse(json.dumps(response.data))

    def post(self, request):
        response = group_config.ServerGroup.bond_public_group(request)
        return JsonResponse(response.__dict__)
