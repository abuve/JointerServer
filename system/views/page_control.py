#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from django.views import View
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from repository.service import web_config


class PermissionDeniedView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'page_control/403.html')