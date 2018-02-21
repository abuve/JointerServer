# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404,redirect

from django.views.decorators.csrf import csrf_exempt
from .samlsp import samuelSP
import urllib
from django.contrib.auth import authenticate,login
from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib.auth import logout as django_logout
# from permission_manager.cores import session_handler

from conf import settings as conf_settings


try:
    urlencoder = urllib.urlencode
except:
    urlencoder = urllib.parse.urlencode


sp = samuelSP(settings.CERTPEM,settings.LOGIN_IDP_ENDPOINT,settings.LOGIN_PROVIDER,settings.LOGIN_ISSUER)


def auth(request):
    if request.user.is_anonymous():
        params = {"SAMLRequest": sp.genAuthnRequest(settings.LOGIN_ACS_URL)}
        return redirect(settings.LOGIN_IDP_ENDPOINT + '?' + urllib.parse.urlencode(params))
    return redirect(settings.LOGIN_REDIRECT_URL)


def login_sp(request):
    if not request.user.is_authenticated():
        return render(request, 'login.html')
    return redirect(settings.LOGIN_REDIRECT_URL)


def logout(request):
    django_logout(request)
    #return redirect('https://sso.monaco1.me/logout')
    return redirect(conf_settings.logout_url)


@csrf_exempt
def acs(request):
    if request.method =='POST':
        samlResponse = request.POST.get('SAMLResponse')
        response = sp.decodeAndValidate(samlResponse)
        if response:
            user = sp.getName(response)
            attr = sp.getAttributeList(response)
            if user is not None:
                auths = authenticate(username=user)
                if auths is not None:
                    login(request,auths)
                    if attr:
                        request.session['attr'] = attr
                        request.session.modified=True
                        # add user permission
                        #session_upload = session_handler.SessionUpload(request, user)
                        #session_upload.load()
                    return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)

    return redirect('auth')