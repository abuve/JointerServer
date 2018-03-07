#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from django.views import View
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from utils.mixin_utils import LoginRequiredMixin, PermissionRequiredMixin, WriteAccessLogsMixin

from repository.service import web_config
from repository.service import instance_config


class InstanceConfigView(WriteAccessLogsMixin, LoginRequiredMixin, PermissionRequiredMixin, View):
    def get(self, request, server_id):
        response = instance_config.ServerInstance.get_asset_instance(server_id)
        return render(request, 'server_config_instance.html', {'response': response})


class InstanceConfigJsonView(WriteAccessLogsMixin, LoginRequiredMixin, PermissionRequiredMixin, View):
    def get(self, request, server_id):
        response = instance_config.ServerInstance.get_server_instances_json(server_id)
        return HttpResponse(json.dumps(response.data))


class UpdateServerInstanceView(WriteAccessLogsMixin, LoginRequiredMixin, PermissionRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        response = instance_config.ServerInstance.get_instance_by_id(request)
        return HttpResponse(json.dumps(response))

    def post(self, request):
        response = instance_config.ServerInstance.add_server_instance(request)
        return JsonResponse(response.__dict__)

    def put(self, request):
        response = instance_config.ServerInstance.update_server_instance(request)
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = instance_config.ServerInstance.delete_server_instance(request)
        return JsonResponse(response.__dict__)

class GetInstanceByGroupIdView(WriteAccessLogsMixin, LoginRequiredMixin, PermissionRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        response = instance_config.ServerInstance.get_instance_by_groupid(request)
        return JsonResponse(response.__dict__)