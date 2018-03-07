#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from django.views import View
from django.shortcuts import render
from django.shortcuts import HttpResponse, HttpResponseRedirect
from utils.mixin_utils import LoginRequiredMixin, PermissionRequiredMixin, WriteAccessLogsMixin
from django.http import JsonResponse

from cmdb.service import dashboard


class DashBoardIndexView(WriteAccessLogsMixin, LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        response = dashboard.DashBoard.get_basic_count()
        return render(request, 'dashboard_index.html', {'response': response})

class DashBoardChartAjaxView(WriteAccessLogsMixin, LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        response = dashboard.DashBoard().get_chart_ajax()
        return JsonResponse(response.__dict__)