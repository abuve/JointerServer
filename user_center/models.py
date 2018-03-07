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
    roles = models.ManyToManyField('Roles', related_name='user_roles')

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


class Permission(models.Model):
    """
    权限配置管理
    """
    url_name = models.CharField(max_length=150)
    url_method_choice = (
        ('GET', 'GET'),
        ('POST', 'POST'),
        ('PUT', 'PUT'),
        ('DELETE', 'DELETE'),
    )
    url_method = models.CharField(u'url请求方法', max_length=10, choices=url_method_choice, default='GET')
    memo = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name_plural = "权限配置管理"

    def __str__(self):
        return self.url_name


class Roles(models.Model):
    """
    角色配置管理
    """
    name = models.CharField(u'角色名称', max_length=32)
    permissions = models.ManyToManyField('Permission', related_name='roles_permission')
    memo = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name_plural = "角色配置管理"

    def __str__(self):
        return self.name