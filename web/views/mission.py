#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from django.views import View
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import JsonResponse

from web.service import mission
from web.service import server_project
from repository import models as repository_models


class MissionListView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'mission_list.html')


class MissionJsonView(View):
    def get(self, request):
        obj = mission.Mission()
        response = obj.fetch_assets(request)
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = asset.Asset.delete_assets(request)
        return JsonResponse(response.__dict__)

    def put(self, request):
        response = asset.Asset.put_assets(request)
        return JsonResponse(response.__dict__)


class MissionCreateView(View):
    def get(self, request):
        response = server_project.ServerProject.get_project_info(request)
        return render(request, 'mission_create.html', {'response': response})

    def post(self, request):
        response = mission.Mission.add_mission(request)
        return JsonResponse(response.__dict__)


class MissionDetailListView(View):
    def get(self, request, mission_id):
        response = {'mission_id': mission_id}
        return render(request, 'mission_detail_list.html', {'response': response})



class MissionDetailListJsonView(View):
    def get(self, request, mission_id):
        response = mission.Mission.get_mission_detail_json(request, mission_id)
        return HttpResponse(json.dumps(response.data))




