from django.db import models

from cmdb import models as CMDB_MODELS


# 访问日志记录
class AccessLogs(models.Model):
    username = models.CharField(verbose_name=u'访问用户', max_length=35, blank=True, null=False)
    create_at = models.DateTimeField(verbose_name=u'访问时间', blank=True, auto_now_add=True, null=False)
    routing = models.CharField(verbose_name=u'访问地址', max_length=200, blank=True, null=False)
    ip_address = models.GenericIPAddressField(verbose_name=u'源地址')
    # 确定是否是同一次访问，只是刷新页面而已
    cookies = models.CharField(verbose_name=u'cookies值', max_length=300, blank=True, null=False)
    browser = models.CharField(verbose_name=u'浏览器信息', max_length=250, blank=True, null=True, default='')
    system = models.CharField(verbose_name=u'客户端系统信息', max_length=250, blank=True, null=True, default='')

    class Meta:
        verbose_name = "访问日志"
        verbose_name_plural = verbose_name
        ordering = ['-create_at']

    def __unicode__(self):
        return "{0},{1},{2},{3},{4},{5}".format(self.username, self.create_at, self.routing,
                                                self.ip_address, self.browser, self.system)

    __str__ = __unicode__