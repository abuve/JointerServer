from django.contrib import admin
from repository import models

admin.site.register(models.ProjectInfo)
admin.site.register(models.Applications)
admin.site.register(models.AppGroups)
admin.site.register(models.AppInstances)
admin.site.register(models.MissionProject)
admin.site.register(models.MissionApp)
admin.site.register(models.MissionAppInstance)
admin.site.register(models.Mission)
admin.site.register(models.DockerYamlConf)
admin.site.register(models.WebConfig)
admin.site.register(models.WebConfigLogsCenter)
admin.site.register(models.UrlConfigHandler)