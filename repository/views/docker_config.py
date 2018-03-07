#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from django.views import View
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from utils.mixin_utils import LoginRequiredMixin, PermissionRequiredMixin, WriteAccessLogsMixin

from repository.service import docker_config


class DockerConfigView(WriteAccessLogsMixin, LoginRequiredMixin, PermissionRequiredMixin, View):
    def get(self, request, server_id):
        response = docker_config.ServerDocker.get_asset_instance(server_id)
        return render(request, 'server_config_docker.html', {'response': response})


class DockerConfigJsonView(WriteAccessLogsMixin, LoginRequiredMixin, PermissionRequiredMixin, View):
    def get(self, request, server_id):
        response = docker_config.ServerDocker.get_server_instances_json(server_id)
        return HttpResponse(json.dumps(response.data))


class UpdateServerDockerView(WriteAccessLogsMixin, LoginRequiredMixin, PermissionRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        response = docker_config.ServerDocker.get_docker_by_id(request)
        return HttpResponse(json.dumps(response))

    def post(self, request):
        response = docker_config.ServerDocker.add_server_instance(request)
        return JsonResponse(response.__dict__)

    def put(self, request):
        response = docker_config.ServerDocker.update_server_instance(request)
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = docker_config.ServerDocker.delete_server_instance(request)
        return JsonResponse(response.__dict__)
