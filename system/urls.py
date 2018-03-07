from django.conf.urls import url
from system.views import page_control
from system.views import login

from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^login.html$', login.LoginView.as_view(), name='system-login'),
    url(r'^logout.html$', login.LogoutView.as_view(), name='system-logout'),
    url(r'^403.html$', page_control.PermissionDeniedView.as_view(), name='page-control-403'),
]
