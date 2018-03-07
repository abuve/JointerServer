#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json

from django.db.models import Q
from django.http.request import QueryDict

from user_center import models as USER_CENTER_MODELS
from utils.base import BaseServiceList
from utils.pager import PageInfo
from utils.response import BaseResponse

from cmdb.service import asset_num


class RolesConfig(BaseServiceList):
    def __init__(self):
        # 查询条件的配置
        condition_config = [
            {'name': 'url_name', 'text': 'URL Name', 'condition_type': 'input'},
            {'name': 'url_method', 'text': 'URL Method', 'condition_type': 'select', 'global_name': 'url_method_list'},
        ]
        # 表格的配置
        table_config = [
            {
                'q': 'id',  # 用于数据库查询的字段，即Model.Tb.objects.filter(*[])
                'title': "ID",  # 前段表格中显示的标题
                'display': 0,  # 是否在前段显示，0表示在前端不显示, 1表示在前端隐藏, 2表示在前段显示
                'text': {'content': "{id}", 'kwargs': {'id': '@id'}},
                'attr': {'k1': 'v1'}  # 自定义属性
            },
            {
                'q': 'name',
                'title': "Role Name",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@name'}},
                'attr': {}
            },
            {
                'q': 'memo',
                'title': "Memo",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@memo'}},
                'attr': {}
            },
            {
                'q': None,
                'title': "Options",
                'display': 1,
                'text': {
                    'content': '<div class="btn-group"><a type="button" class="btn btn-default btn-xs" href="/user_center/roles-edit-{nid}.html"><span class="glyphicon glyphicon-edit" aria-hidden="true"></span> Edit Url</a><a type="button" class="btn btn-default btn-xs" onclick="delete_role_fn({nid})"><span class="glyphicon glyphicon-remove" aria-hidden="true"></span> Delete</a></div>',
                    'kwargs': {'device_type_id': '@device_type_id', 'nid': '@id'}},
                'attr': {'style': 'text-align: left; width: 260px'}
            },
        ]
        # 额外搜索条件
        extra_select = {
            'server_title': '',
            # 'network_title': 'select management_ip from repository_networkdevice where repository_networkdevice.asset_id=repository_asset.id and repository_asset.device_type_id=2',
        }
        super(RolesConfig, self).__init__(condition_config, table_config, extra_select)

    @property
    def url_method_list(self):
        result = map(lambda x: {'id': x[0], 'name': x[1]}, USER_CENTER_MODELS.Permission.url_method_choice)
        return list(result)

    @property
    def device_type_list(self):
        result = map(lambda x: {'id': x[0], 'name': x[1]}, USER_CENTER_MODELS.Asset.device_type_choices)
        return list(result)

    @property
    def idc_list(self):
        values = USER_CENTER_MODELS.IDC.objects.only('id', 'name', 'floor')
        result = map(lambda x: {'id': x.id, 'name': x.name}, values)
        return list(result)

    @property
    def status_map(self):
        result = [
            {'id': 1, 'name': 'success'},
            # {'id': 2, 'name': 'danger'},
            {'id': 3, 'name': 'warning'}
        ]
        return result

    @property
    def business_unit_list(self):
        values = USER_CENTER_MODELS.BusinessUnit.objects.only('id', 'name')
        result = map(lambda x: {'id': x.id, 'name': x.name}, values)
        return list(result)

    @staticmethod
    def assets_condition(request):
        con_str = request.GET.get('condition', None)
        if not con_str:
            con_dict = {}
        else:
            con_dict = json.loads(con_str)

        con_q = Q()
        for k, v in con_dict.items():
            temp = Q()
            temp.connector = 'OR'
            for item in v:
                temp.children.append((k, item))
            con_q.add(temp, 'AND')

        return con_q

    def fetch_data(self, request):
        response = BaseResponse()
        try:
            ret = {}
            conditions = self.assets_condition(request)
            asset_count = USER_CENTER_MODELS.Roles.objects.filter(conditions).count()
            page_info = PageInfo(request.GET.get('pager', None), asset_count)
            asset_list = USER_CENTER_MODELS.Roles.objects.filter(conditions).extra(
                select=self.extra_select).values(
                *self.values_list)[page_info.start:page_info.end]

            ret['table_config'] = self.table_config
            ret['condition_config'] = self.condition_config
            ret['data_list'] = list(asset_list)
            ret['page_info'] = {
                "page_str": page_info.pager(),
                "page_start": page_info.start,
            }
            ret['global_dict'] = {
                'url_method_list': self.url_method_list,
            }
            response.data = ret
            response.message = '获取成功'
        except Exception as e:
            response.status = False
            response.message = str(e)

        return response

    @staticmethod
    def data_create(request):
        response = BaseResponse()
        try:
            post_data = QueryDict(request.body, encoding='utf-8')
            role_name = post_data.get('role_name')
            role_memo = post_data.get('role_memo')
            permission_list = post_data.getlist('permission_list')

            # 创建role
            data_obj = USER_CENTER_MODELS.Roles(
                name=role_name,
                memo=role_memo,
            )
            data_obj.save()

            # 关联permission
            for obj_id in permission_list:
                data_obj.permissions.add(obj_id)

        except Exception as e:
            print(Exception, e)
            response.status = False
            response.message = str(e)

        return response

    @staticmethod
    def data_delete(request):
        response = BaseResponse()
        try:
            delete_data = QueryDict(request.body, encoding='utf-8')
            obj_id = delete_data.get('obj_id')
            USER_CENTER_MODELS.Roles.objects.get(id=obj_id).delete()
            response.message = '删除成功'
        except Exception as e:
            response.status = False
            response.message = str(e)
        return response

    @staticmethod
    def data_update(request):
        response = BaseResponse()
        try:
            put_data = QueryDict(request.body, encoding='utf-8')
            obj_id = put_data.get('role_id')
            role_name = put_data.get('role_name')
            role_memo = put_data.get('role_memo')
            permission_list = put_data.getlist('permission_list')

            update_data = USER_CENTER_MODELS.Roles.objects.get(id=obj_id)
            update_data.name = role_name
            update_data.memo = role_memo
            update_data.save()

            update_data.permissions.clear()

            for obj_id in permission_list:
                update_data.permissions.add(obj_id)

        except Exception as e:
            print(Exception, e)
            response.status = False
            response.message = str(e)
        return response

    @staticmethod
    def get_permission_data():

        response = BaseResponse()
        try:
            response.data = USER_CENTER_MODELS.Permission.objects.all().order_by('-id')

        except Exception as e:
            response.status = False
            response.message = str(e)
        return response

    @staticmethod
    def get_data_by_id(role_nid):
        response = BaseResponse()
        try:
            response.data = USER_CENTER_MODELS.Roles.objects.filter(id=role_nid).first()
            permission_all = USER_CENTER_MODELS.Permission.objects.all()
            left_data = list(set(permission_all) - set(response.data.permissions.all()))
            response.left_data = left_data

        except Exception as e:
            response.status = False
            response.message = str(e)
        return response
