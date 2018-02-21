"""AutoCmdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin

from django.contrib.auth.decorators import login_required

from PySAMLSP import views as auth_views
from cmdb.views import dashboard

urlpatterns = [
    url(r'^acs/', auth_views.acs, name='acs'),
    url(r'^auth/', auth_views.auth, name='auth'),
    url(r'^logout.html$', auth_views.logout, name='logout'),
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('api.urls')),
    url(r'^cmdb/', include('cmdb.urls')),
    url(r'^server/', include('repository.urls')),
    url(r'^', include('web.urls')),
    url(r'', include('web.urls')),
    url(r'user_center/', include('user_center.urls')),
    url(r'dashboard.html$', login_required(dashboard.DashBoardView.as_view())),
]
