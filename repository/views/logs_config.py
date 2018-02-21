#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from django.views import View
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import JsonResponse

from repository.service import logs_config


class LogsConfigView(View):
    def get(self, request, server_id):
        response = logs_config.ServerLogs.get_server_logs(server_id)
        return render(request, 'server_config_logs.html', {'response': response})


class LogsConfigJsonView(View):
    def get(self, request, server_id):
        response = logs_config.ServerLogs.get_server_logs_json(server_id)
        return HttpResponse(json.dumps(response.data))


class UpdateServerLogsView(View):
    def get(self, request, *args, **kwargs):
        response = logs_config.ServerLogs.get_logs_by_id(request)
        return HttpResponse(json.dumps(response))

    def post(self, request):
        response = logs_config.ServerLogs.add_server_logs(request)
        return JsonResponse(response.__dict__)

    def put(self, request):
        response = logs_config.ServerLogs.update_server_logs(request)
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = logs_config.ServerLogs.delete_server_logs(request)
        return JsonResponse(response.__dict__)
