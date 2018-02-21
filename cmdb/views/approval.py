#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from django.views import View
from django.shortcuts import render
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse

from cmdb.service import approval
from cmdb.service import client_report_handler


class ApprovalListView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'cmdb_approval_list.html')


class ApprovalJsonView(View):
    def post(self, request):
        response = server.Server.add_data(request)
        return HttpResponseRedirect('/server.html')

    def get(self, request):
        # obj = server.Server()
        response = approval.Approval().fetch_assets(request)
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = server.Server.delete_data(request)
        return JsonResponse(response.__dict__)

    # 提交资产审批
    def put(self, request):
        response = approval.Approval.approved_data(request)
        return JsonResponse(response.__dict__)


def asset_report_use_asset_id(request):
    if request.method == 'POST':
        ass_handler = client_report_handler.Asset(request)
        if ass_handler.data_is_valid():
            print("----asset data valid:")
            ass_handler.data_inject()

        return HttpResponse(json.dumps(ass_handler.response))

    return HttpResponse('--wrong--')


def asset_with_no_asset_id(request):
    if request.method == 'POST':
        ass_handler = client_report_handler.Asset(request)
        res = ass_handler.check_asset_from_approval_zone()

        return HttpResponse(json.dumps(res))