#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from django.views import View
from django.shortcuts import render
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse

from cmdb.service import dashboard


class DashBoardIndexView(View):
    def get(self, request, *args, **kwargs):
        response = dashboard.DashBoard.get_basic_count()
        return render(request, 'dashboard_index.html', {'response': response})

class DashBoardChartAjaxView(View):
    def get(self, request, *args, **kwargs):
        response = dashboard.DashBoard().get_chart_ajax()
        return JsonResponse(response.__dict__)