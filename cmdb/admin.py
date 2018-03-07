from django.contrib import admin
from cmdb import models
from django.contrib.auth.models import User

'''
配置Django后台admin数据编辑显示
'''
class ServerInline(admin.TabularInline):
    model = models.Server


class MemoryInline(admin.TabularInline):
    model = models.RAM


class DiskInline(admin.TabularInline):
    model = models.Disk


'''
定制后台数据加载项
'''
# class ServerAdmin(admin.ModelAdmin):
#     list_display = ('id', 'hostname', 'manufacturer')
#     inlines = [MemoryInline, DiskInline]

class AssetAdmin(admin.ModelAdmin):
    search_fields = ['sn', ]
    inlines = [ServerInline]

#admin.site.register(User)
admin.site.register(models.Asset, AssetAdmin)
admin.site.register(models.Server)
# admin.site.register(models.UserProfile)
# admin.site.register(models.UserGroup)
admin.site.register(models.BusinessUnit)
admin.site.register(models.IDC)
admin.site.register(models.Tag)
admin.site.register(models.Disk)
admin.site.register(models.RAM)
admin.site.register(models.NewAssetApprovalZone)
admin.site.register(models.AssetRecord)
admin.site.register(models.ErrorLog)
admin.site.register(models.DockerInstance)