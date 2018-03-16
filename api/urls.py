from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from api.views import assets

urlpatterns = [
    url(r'^assets/$', assets.AssetsView.as_view()),
]
