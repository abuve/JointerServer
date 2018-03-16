from django.shortcuts import render, render_to_response, HttpResponse

# Create your views here.
from django.core.urlresolvers import resolve
from user_center.models import UserProfile


class SessionUpload:
    def __init__(self, request):
        self.request = request

    def load(self):
        url_perm_dic = {}
        user_obj = UserProfile.objects.get(username=self.request.user.username)
        for roles_obj in user_obj.roles.all():
            for perm_obj in roles_obj.permissions.all():
                if url_perm_dic.get(perm_obj.url_name):
                    url_perm_dic[perm_obj.url_name].append(perm_obj.url_method)
                else:
                    url_perm_dic[perm_obj.url_name] = [perm_obj.url_method]

        self.request.session[self.request.user.username] = url_perm_dic

    def checkout(self):
        request_method = self.request.method
        resolve_url_name = resolve(self.request.path).url_name

        try:
            if request_method in self.request.session[self.request.user.username][resolve_url_name]:
                return True
            else:
                return False
        except Exception as e:
            print(Exception, e)
            return False
