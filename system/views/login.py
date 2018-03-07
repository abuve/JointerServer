#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from django.views import View
from django.shortcuts import render
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import auth

from system.service import login


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        response = login.LoginHandler.account_login(request)
        return JsonResponse(response.__dict__)


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        auth.logout(request)
        return HttpResponseRedirect("/system/login.html?next=/")