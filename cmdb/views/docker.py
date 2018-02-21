#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from django.views import View
from django.shortcuts import render
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse

from cmdb.service import docker


class DockerListView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'cmdb_docker_list.html')


class DockerJsonView(View):
    def post(self, request):
        response = server.Server.add_data(request)
        return HttpResponseRedirect('/server.html')

    def get(self, request):
        # obj = server.Server()
        response = docker.Docker().fetch_assets(request)
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = server.Server.delete_data(request)
        return JsonResponse(response.__dict__)

    def put(self, request):
        response = server.Server.put_assets(request)
        return JsonResponse(response.__dict__)


class AssetDetailView(View):
    def get(self, request, asset_nid):
        response = server.Server.assets_detail(asset_nid)
        return render(request, 'cmdb_asset_detail.html', {"response": response})