# -*- coding: utf-8 -*-
# @Time    : 1/26/2018 10:18 AM
# @Author  : Abbott
# @Site    : 
# @File    : models.py
# @Software: PyCharm

from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    """
    用户信息
    """
    phone = models.CharField(u'手机', max_length=32)
    department = models.CharField(blank=True, max_length=256, null=True, verbose_name='部门')

    class Meta:
        verbose_name_plural = "用户信息"

    def __str__(self):
        return self.username


class UserGroup(models.Model):
    """
    用户组
    """
    name = models.CharField(max_length=32, unique=True)
    users = models.ManyToManyField('UserProfile', related_name='user_groups')

    class Meta:
        verbose_name_plural = "用户组表"

    def __str__(self):
        return self.name