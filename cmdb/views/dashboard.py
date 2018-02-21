#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from django.views import View
from django.shortcuts import render
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse


class DashBoardView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard_index.html')