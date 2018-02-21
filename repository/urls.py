from django.conf.urls import url
from repository.views import web_config
from repository.views import group_config
from repository.views import instance_config
from repository.views import docker_config
from repository.views import logs_config
from repository.views import urlmaps_config

from django.contrib.auth.decorators import login_required

urlpatterns = [

    url(r'^webconf/nginx/config-(?P<server_id>\d+).html$', login_required(web_config.WebConfigNginxView.as_view()), name='server-config-nginx'),
    url(r'^webconf/nginx/fileTreeJson-(?P<server_id>\d+).html$', login_required(web_config.WebConfigNginxJsonView.as_view())),
    url(r'^webconf/nginx/version-json-(?P<server_id>\d+).html$', login_required(web_config.WebConfigVersionJsonView.as_view())),
    url(r'^webconf/nginx/version-tree-(?P<server_id>\d+).html$', login_required(web_config.WebConfigVersionListView.as_view())),
    url(r'^webconf/nginx/file-data-(?P<server_id>\d+).html$', login_required(web_config.WebConfigFileData.as_view())),
    url(r'^webconf/nginx/file-push-(?P<server_id>\d+).html$', login_required(web_config.WebConfigFilePush.as_view())),
    url(r'^webconf/nginx/get_version_status.html$', login_required(web_config.WebConfigVersionStatus.as_view())),

    url(r'^config/group/(?P<server_id>\d+).html$', login_required(group_config.GroupConfigView.as_view()), name='server-config-group'),
    url(r'^config/group/json-(?P<server_id>\d+).html$', login_required(group_config.GroupConfigJsonView.as_view())),
    url(r'^config/group/update-server-group.html$', login_required(group_config.UpdateServerGroupView.as_view())),
    url(r'^config/group/update-public-group.html$', login_required(group_config.UpdatePublicGroupView.as_view())),

    url(r'^config/instance/(?P<server_id>\d+).html$', login_required(instance_config.InstanceConfigView.as_view()), name='server-config-instance'),
    url(r'^config/instance/json-(?P<server_id>\d+).html$', login_required(instance_config.InstanceConfigJsonView.as_view())),
    url(r'^config/instance/update-server-instance.html$', login_required(instance_config.UpdateServerInstanceView.as_view())),
    url(r'^config/instance/get-instance-by-groupid.html$', login_required(instance_config.GetInstanceByGroupIdView.as_view())),

    url(r'^config/docker/(?P<server_id>\d+).html$', login_required(docker_config.DockerConfigView.as_view()), name='server-config-docker'),
    url(r'^config/docker/json-(?P<server_id>\d+).html$', login_required(docker_config.DockerConfigJsonView.as_view())),
    url(r'^config/docker/update-server-docker.html$', login_required(docker_config.UpdateServerDockerView.as_view())),

    url(r'^config/logs/(?P<server_id>\d+).html$', login_required(logs_config.LogsConfigView.as_view()), name='server-config-logs'),
    url(r'^config/logs/json-(?P<server_id>\d+).html$', login_required(logs_config.LogsConfigJsonView.as_view())),
    url(r'^config/logs/update-server-logs.html$', login_required(logs_config.UpdateServerLogsView.as_view())),

    url(r'^config/urlmaps/(?P<server_id>\d+).html$', login_required(urlmaps_config.UrlMapsConfigView.as_view()), name='server-config-urlmaps'),
    url(r'^config/urlmaps/json-(?P<server_id>\d+).html$', login_required(urlmaps_config.UrlMapsConfigJsonView.as_view())),
    url(r'^config/urlmaps/get_urlmaps_detail.html$', login_required(urlmaps_config.UrlMapsDetailView.as_view())),
    url(r'^config/urlmaps/update-server-urlmaps.html$', login_required(urlmaps_config.UpdateUrlMapsView.as_view())),
    url(r'^config/urlmaps/update-server-urlmaps-groups.html$', login_required(urlmaps_config.UpdateUrlMapsGroupsView.as_view())),

]
