#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from django.views import View
from django.shortcuts import render
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse

from cmdb.service import business


class BusinessListView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'cmdb_business_list.html')


class BusinessJsonView(View):
    def post(self, request):
        response = business.Business().add_data(request)
        return JsonResponse(response.__dict__)

    def get(self, request):
        # obj = server.Server()
        response = business.Business().fetch_assets(request)
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = business.Business.delete_data(request)
        return JsonResponse(response.__dict__)

    def put(self, request):
        response = business.Business.put_data(request)
        return JsonResponse(response.__dict__)


class BusinessDetailView(View):
    def get(self, request, business_nid):
        response = business.Business.get_buesiness_detail(business_nid)
        return render(request, 'include/cmdb_business_detail.html', {"response": response})