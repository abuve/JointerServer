#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from django.views import View
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from utils.mixin_utils import LoginRequiredMixin, PermissionRequiredMixin, WriteAccessLogsMixin

from repository.service import urlmaps_config


class UrlMapsConfigView(WriteAccessLogsMixin, LoginRequiredMixin, PermissionRequiredMixin, View):
    def get(self, request, server_id):
        response = urlmaps_config.ServerUrlMaps.get_server_urlmaps(server_id)
        return render(request, 'server_config_urlmaps.html', {'response': response})


class UrlMapsDetailView(WriteAccessLogsMixin, LoginRequiredMixin, PermissionRequiredMixin, View):
    def post(self, request):
        response = urlmaps_config.ServerUrlMaps.get_server_urlmaps_detial(request)
        return render(request, 'include/server_config_urlmaps_detail.html', {'response': response})


class UrlMapsConfigJsonView(WriteAccessLogsMixin, LoginRequiredMixin, PermissionRequiredMixin, View):
    def get(self, request, server_id):
        response = urlmaps_config.ServerUrlMaps.get_server_urlmaps_json(server_id)
        return HttpResponse(json.dumps(response.data))


class UpdateUrlMapsView(WriteAccessLogsMixin, LoginRequiredMixin, PermissionRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        response = urlmaps_config.ServerUrlMaps.get_urlmaps_by_id(request)
        return HttpResponse(json.dumps(response))

    def post(self, request):
        response = urlmaps_config.ServerUrlMaps.add_urlmaps(request)
        return JsonResponse(response.__dict__)

    def put(self, request):
        response = urlmaps_config.ServerUrlMaps.update_urlmaps(request)
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = urlmaps_config.ServerUrlMaps.delete_urlmaps(request)
        return JsonResponse(response.__dict__)


class UpdateUrlMapsGroupsView(WriteAccessLogsMixin, LoginRequiredMixin, PermissionRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        response = urlmaps_config.ServerUrlMaps.get_urlmaps_groups_by_id(request)
        return JsonResponse(response.__dict__)

    def post(self, request):
        response = urlmaps_config.ServerUrlMaps.update_urlmaps_groups(request)
        return JsonResponse(response.__dict__)
