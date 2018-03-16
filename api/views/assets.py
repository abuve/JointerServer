#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from django.views import View
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from api.service import assets


class AssetsView(View):
    def post(self, request):
        try:
            api_handler = assets.ApiHandler(request)
            if api_handler.check_data_component():
                request_data = api_handler.request_json_data
                if hasattr(api_handler, request_data.get('option')):
                    query_func = getattr(api_handler, request_data.get('option'))
                    response_data = query_func()
                else:
                    response_data = {'status': 500,
                                     'msg': 'unknow query function %s, please check api documents.' % request_data.get(
                                         'option')}
            else:
                response_data = api_handler.response_msg
        except Exception as e:
            print(Exception, e)
            response_data = {'status': 500, 'msg': 'Non-canonical json data.'}

        return HttpResponse(json.dumps(response_data))

