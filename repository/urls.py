from django.conf.urls import url
from repository.views import web_config
from repository.views import group_config
from repository.views import instance_config
from repository.views import docker_config
from repository.views import logs_config
from repository.views import urlmaps_config

from django.contrib.auth.decorators import login_required

urlpatterns = [

    url(r'^webconf/nginx/config-(?P<server_id>\d+).html$', web_config.WebConfigNginxView.as_view(), name='server-config-nginx'),
    url(r'^webconf/nginx/fileTreeJson-(?P<server_id>\d+).html$', web_config.WebConfigNginxJsonView.as_view(), name='server-config-nginx-fileTreeJson'),
    url(r'^webconf/nginx/version-json-(?P<server_id>\d+).html$', web_config.WebConfigVersionJsonView.as_view(), name='server-config-nginx-version-json'),
    url(r'^webconf/nginx/version-tree-(?P<server_id>\d+).html$', web_config.WebConfigVersionListView.as_view(), name='server-config-nginx-version-tree'),
    url(r'^webconf/nginx/file-data-(?P<server_id>\d+).html$', web_config.WebConfigFileData.as_view(), name='server-config-nginx-file-data'),
    url(r'^webconf/nginx/file-push-(?P<server_id>\d+).html$', web_config.WebConfigFilePush.as_view(), name='server-config-nginx-file-push'),
    url(r'^webconf/nginx/get_version_status.html$', web_config.WebConfigVersionStatus.as_view(), name='server-config-nginx-rightStatus'),

    url(r'^config/group/(?P<server_id>\d+).html$', group_config.GroupConfigView.as_view(), name='server-config-group'),
    url(r'^config/group/json-(?P<server_id>\d+).html$', group_config.GroupConfigJsonView.as_view(), name='server-config-group-json'),
    url(r'^config/group/update-server-group.html$', group_config.UpdateServerGroupView.as_view(), name='server-config-group-update-server-group'),
    url(r'^config/group/update-public-group.html$', group_config.UpdatePublicGroupView.as_view(), name='server-config-group-update-public-group'),

    url(r'^config/instance/(?P<server_id>\d+).html$', instance_config.InstanceConfigView.as_view(), name='server-config-instance'),
    url(r'^config/instance/json-(?P<server_id>\d+).html$', instance_config.InstanceConfigJsonView.as_view(), name='server-config-instance-json'),
    url(r'^config/instance/update-server-instance.html$', instance_config.UpdateServerInstanceView.as_view(), name='server-config-instance-update-server-instance'),
    url(r'^config/instance/get-instance-by-groupid.html$', instance_config.GetInstanceByGroupIdView.as_view(), name='server-config-instance-get-instance-by-groupid'),

    url(r'^config/docker/(?P<server_id>\d+).html$', docker_config.DockerConfigView.as_view(), name='server-config-docker'),
    url(r'^config/docker/json-(?P<server_id>\d+).html$', docker_config.DockerConfigJsonView.as_view(), name='server-config-docker-json'),
    url(r'^config/docker/update-server-docker.html$', docker_config.UpdateServerDockerView.as_view(), name='server-config-docker-update-server-docker'),

    url(r'^config/logs/(?P<server_id>\d+).html$', logs_config.LogsConfigView.as_view(), name='server-config-logs'),
    url(r'^config/logs/json-(?P<server_id>\d+).html$', logs_config.LogsConfigJsonView.as_view(), name='server-config-logs-json'),
    url(r'^config/logs/update-server-logs.html$', logs_config.UpdateServerLogsView.as_view(), name='server-config-logs-update-server-logs'),

    url(r'^config/urlmaps/(?P<server_id>\d+).html$', urlmaps_config.UrlMapsConfigView.as_view(), name='server-config-urlmaps'),
    url(r'^config/urlmaps/json-(?P<server_id>\d+).html$', urlmaps_config.UrlMapsConfigJsonView.as_view(), name='server-config-urlmaps-json'),
    url(r'^config/urlmaps/get_urlmaps_detail.html$', urlmaps_config.UrlMapsDetailView.as_view(), name='server-config-get-urlmaps-detail'),
    url(r'^config/urlmaps/update-server-urlmaps.html$', urlmaps_config.UpdateUrlMapsView.as_view(), name='server-config-urlmaps-update-server-urlmaps'),
    url(r'^config/urlmaps/update-server-urlmaps-groups.html$', urlmaps_config.UpdateUrlMapsGroupsView.as_view(), name='server-config-urlmaps-update-server-urlmaps-groups'),

]
