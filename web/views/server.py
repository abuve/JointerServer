#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from django.views import View
from django.shortcuts import render
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse

from web.service import server
from web.service import server_project
from web.service import server_group
from web.service import server_instance
from web.service import server_yaml_conf
from repository import models as repository_models


class ServerListView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'server_list.html')


class ServerJsonView(View):
    def post(self, request):
        response = server.Server.add_data(request)
        return HttpResponseRedirect('/server.html')

    def get(self, request):
        obj = server.Server()
        response = obj.fetch_assets(request)
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = server.Server.delete_data(request)
        return JsonResponse(response.__dict__)

    def put(self, request):
        response = server.Server.put_assets(request)
        return JsonResponse(response.__dict__)


class ServerDetailView(View):
    def get(self, request, asset_nid):
        response = server.Server.server_config(asset_nid)
        if request.GET.get('data_from') == 'appviews':
            return render(request, 'project_appviews_detail.html', {'response': response})
        else:
            return render(request, 'server_config.html', {'response': response})


class ServerDetaiGroupView(View):
    def get(self, request, asset_nid):
        response = server_group.ServerGroup.get_server_groups_json(asset_nid)
        return HttpResponse(json.dumps(response))


class AddServerView(View):
    def get(self, request, *args, **kwargs):
        response = server_project.ServerProject.get_project_info(request)
        return render(request, 'add_server.html', {'response': response})


class UpdateServerView(View):
    def get(self, request, server_nid):
        project_info = server_project.ServerProject.get_project_info(request)
        response = server.Server.server_config(server_nid)
        return render(request, 'edit_server.html', {'response': response, 'project_info': project_info})


class UpdateServerGroupView(View):
    def get(self, request, *args, **kwargs):
        response = server_group.ServerGroup.get_group_by_id(request)
        return HttpResponse(json.dumps(response))

    def post(self, request):
        response = server_group.ServerGroup.add_server_group(request)
        return JsonResponse(response.__dict__)

    def put(self, request):
        response = server_group.ServerGroup.update_server_group(request)
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = server_group.ServerGroup.delete_server_group(request)
        return JsonResponse(response.__dict__)


class UpdateServerInstanceView(View):
    def get(self, request, *args, **kwargs):
        response = server_instance.ServerInstance.get_instance_by_id(request)
        return HttpResponse(json.dumps(response))

    def post(self, request):
        response = server_instance.ServerInstance.add_server_instance(request)
        return JsonResponse(response.__dict__)

    def put(self, request):
        response = server_instance.ServerInstance.update_server_instance(request)
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = server_instance.ServerInstance.delete_server_instance(request)
        return JsonResponse(response.__dict__)


class GetServerInstanceTypeView(View):
    def get(self, request, *args, **kwargs):
        response = server.Server.instance_type_list(request)
        return HttpResponse(json.dumps(response))


class ServerDetaiInstanceView(View):
    def get(self, request, asset_nid):
        response = server_instance.ServerInstance.get_server_instances_json(asset_nid)
        return HttpResponse(json.dumps(response))


class UpdateYamlConfView(View):
    def get(self, request, *args, **kwargs):
        service_handler = server_yaml_conf.ServerYamlConf()
        response = service_handler.get_yaml_conf(request)
        return JsonResponse(response.__dict__)

    def post(self, request):
        response = server_yaml_conf.ServerYamlConf().add_yaml_conf(request)
        return JsonResponse(response.__dict__)

    def put(self, request):
        response = server_yaml_conf.ServerYamlConf().update_yaml_conf(request)
        return JsonResponse(response.__dict__)


def get_app_by_project(request):
    response = server_project.ServerProject.get_app_by_project(request)
    return JsonResponse(response.__dict__)
