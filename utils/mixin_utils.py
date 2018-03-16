#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import AccessMixin
from django.conf.urls import url
import json
from user_center.models import UserProfile
from system.models import AccessLogs
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from utils import authSession


# 登录认证
class LoginRequiredMixin(AccessMixin):
    """
    登录认证
    """
    @method_decorator(login_required(login_url='/system/login.html'))
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class WriteAccessLogsMixin(AccessMixin):
    """
    日志记录
    """

    def dispatch(self, request, *args, **kwargs):
        username = request.user.get_username()
        if len(username) == 0: username = 'nobody'
        routing = request.build_absolute_uri()
        cookies = json.dumps(request.COOKIES)[:200]
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ipaddress = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ipaddress = request.META['REMOTE_ADDR']
        if 'HTTP_USER_AGENT' in request.META:
            browser = str(request.META['HTTP_USER_AGENT'])
            if 'OS' in request.META:
                os = str(request.META['OS'])
            else:
                os = browser.split('(')[1].split(')')[0]
        else:
            browser = ''
            os = ''
        access_logs_obj = AccessLogs.objects
        if len(access_logs_obj.filter(username=username)) == 0:
            access_logs_obj.create(username=username, routing=routing, ip_address=ipaddress,
                                   cookies=cookies, browser=browser, system=os).save()
        else:
            if len(access_logs_obj.filter(cookies=cookies)) == 0:
                access_logs_obj.create(username=username, routing=routing, ip_address=ipaddress,
                                       cookies=cookies, browser=browser, system=os).save()

        return super(WriteAccessLogsMixin, self).dispatch(request, *args, **kwargs)


class RemoveSessionMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        request.session.set_expiry(0)
        return super(RemoveSessionMixin, self).dispatch(request, *args, **kwargs)


class PermissionRequiredMixin(AccessMixin):
    """
    权限认证
    """
    def dispatch(self, request, *args, **kwargs):
        try:
            auth_handler = authSession.SessionUpload(request)
            if auth_handler.checkout():
                return super(PermissionRequiredMixin, self).dispatch(request, *args, **kwargs)
            else:
                return HttpResponseRedirect('/system/403.html')
        except Exception as e:
            print(Exception, e)
            return HttpResponse(403)
