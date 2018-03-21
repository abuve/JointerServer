from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from web.views import account
from web.views import home
from web.views import asset
from web.views import user
from web.views import server
from web.views import mission
from web.views import project

from django.contrib.auth.decorators import login_required

urlpatterns = [
    # url(r'^login.html$', account.LoginView.as_view()),
    # url(r'^logout.html$', account.LogoutView.as_view()),
    # url(r'^index.html$', home.IndexView.as_view()),
    # url(r'^cmdb.html$', home.CmdbView.as_view()),
    #
    # url(r'^asset.html$', asset.AssetListView.as_view()),
    # url(r'^assets.html$', asset.AssetJsonView.as_view()),
    #
    # url(r'^idc.html$', asset.IDCListView.as_view()),
    # url(r'^idcjson.html$', asset.IDCJsonView.as_view()),
    #
    # url(r'^asset-(?P<device_type_id>\d+)-(?P<asset_nid>\d+).html$', asset.AssetDetailView.as_view()),
    # url(r'^add-asset.html$', asset.AddAssetView.as_view()),
    #
    # url(r'^users.html$', user.UserListView.as_view()),
    # url(r'^user.html$', user.UserJsonView.as_view()),


    url(r'^$', login_required(server.ServerListView.as_view())),
    url(r'^server.html$', login_required(server.ServerListView.as_view()), name='application-server'),
    url(r'^servers.html$', login_required(server.ServerJsonView.as_view()), name='application-servers'),
    url(r'^server-config-(?P<asset_nid>\d+).html$', login_required(server.ServerDetailView.as_view()), name='server-config'),
    url(r'^add-server.html$', login_required(server.AddServerView.as_view()), name='application-add-server'),
    url(r'^edit-server-(?P<server_nid>\d+).html$', login_required(server.UpdateServerView.as_view()), name='application-edit-server'),

    url(r'^get_app_by_project/$', login_required(server.get_app_by_project), name='application-get-app-by-project'),

    # url(r'^update-server-group.html$', server.UpdateServerGroupView.as_view()),
    # url(r'^server-groups-(?P<asset_nid>\d+).html$', server.ServerDetaiGroupView.as_view()),

    #url(r'^server-instances-(?P<asset_nid>\d+).html$', server.ServerDetaiInstanceView.as_view()),
    #url(r'^update-server-instance.html$', server.UpdateServerInstanceView.as_view()),
    #url(r'^get-server-instance_type.html$', server.GetServerInstanceTypeView.as_view()),

    #url(r'^update-yaml-nginx.html$', server.UpdateYamlConfView.as_view()),

    url(r'^mission.html$', login_required(mission.MissionListView.as_view()), name='mission-mission-list'),
    url(r'^missions.html$', login_required(mission.MissionJsonView.as_view()), name='mission-mission-json'),
    url(r'^mission-create.html$', login_required(mission.MissionCreateView.as_view()), name='mission-mission-create'),
    url(r'^mission-detail-(?P<mission_id>\d+).html$', login_required(mission.MissionDetailListView.as_view()), name='mission-mission-detail'),
    url(r'^mission-detail-json-(?P<mission_id>\d+).html$', login_required(mission.MissionDetailListJsonView.as_view()), name='mission-mission-detail-json'),

    url(r'^project.html$', login_required(project.ProjectListView.as_view()), name='project-project-list'),
    url(r'^projects.html$', login_required(project.ProjectJsonView.as_view()), name='project-project-json'),
    url(r'^add-project.html$', login_required(project.AddProjectView.as_view()), name='project-add-project'),
    url(r'^edit-project-(?P<project_nid>\d+).html$', login_required(project.UpdateProjectView.as_view()), name='project-edit-project'),

    url(r'^project/projectviews/(?P<project_nid>\d+).html$', login_required(project.ProjectProjectViewsView.as_view()), name='project-projectviews'),
    url(r'^project/appviews/(?P<project_nid>\d+).html$', login_required(project.ProjectAppViewsView.as_view()), name='project-appviews'),

    # url(r'^chart-(?P<chart_type>\w+).html$', home.ChartView.as_view()),
]
