from django.shortcuts import render_to_response, HttpResponseRedirect
from django.contrib import auth
from utils.response import BaseResponse
from utils.base import BaseServiceList
from utils import authSession
# from permission_manager.cores import session_handler


class LoginHandler(BaseServiceList):
    def __init__(self):
        pass

    @staticmethod
    def account_login(request):
        response = BaseResponse()
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                # 将权限配置写入session
                auth_handler = authSession.SessionUpload(request)
                auth_handler.load()
            else:
                response.status = False
                response.message = '用户名或密码错误'
        except Exception as e:
            response.status = False
            response.message = str(e)

        return response