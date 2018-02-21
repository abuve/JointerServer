# -*- coding: utf-8 -*-
# @Time    : 1/26/2018 10:17 AM
# @Author  : Abbott
# @Site    : 
# @File    : admin.py
# @Software: PyCharm

from django.contrib import admin
from user_center import models


admin.site.register(models.UserProfile)
admin.site.register(models.UserGroup)