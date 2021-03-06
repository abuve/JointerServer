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


class PermissionConfig(BaseServiceList):
    def __init__(self):
        # 查询条件的配置
        condition_config = [
            {'name': 'url_name', 'text': 'URL名称', 'condition_type': 'input'},
            {'name': 'url_method', 'text': 'URL方法', 'condition_type': 'select', 'global_name': 'url_method_list'},
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
                'q': 'url_name',
                'title': "URL名称",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@url_name'}},
                'attr': {}
            },
            {
                'q': 'url_method',
                'title': "Url方法",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@url_method'}},
                'attr': {}
            },
            {
                'q': 'memo',
                'title': "备注",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@memo'}},
                'attr': {}
            },
            {
                'q': None,
                'title': "操作",
                'display': 1,
                'text': {
                    'content': '<div class="btn-group"><a type="button" class="btn btn-default btn-xs" href="/user_center/permission-edit-{nid}.html"><span class="glyphicon glyphicon-edit" aria-hidden="true"></span> 编辑</a><a type="button" class="btn btn-default btn-xs" onclick="delete_url_fn({nid})"><span class="glyphicon glyphicon-remove" aria-hidden="true"></span> 删除</a></div>',
                    # 'content': "<a href='/cmdb/asset-detail-{nid}.html'>查看详细</a> | <a href='/edit-asset-{device_type_id}-{nid}.html'>编辑</a>",
                    'kwargs': {'device_type_id': '@device_type_id', 'nid': '@id'}},
                'attr': {'style': 'text-align: left; width: 260px'}
            },
        ]
        # 额外搜索条件
        extra_select = {
            'server_title': '',
            # 'network_title': 'select management_ip from repository_networkdevice where repository_networkdevice.asset_id=repository_asset.id and repository_asset.device_type_id=2',
        }
        super(PermissionConfig, self).__init__(condition_config, table_config, extra_select)

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
            asset_count = USER_CENTER_MODELS.Permission.objects.filter(conditions).count()
            page_info = PageInfo(request.GET.get('pager', None), asset_count)
            asset_list = USER_CENTER_MODELS.Permission.objects.filter(conditions).extra(
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

    def asset_create(self):
        response = BaseResponse()
        try:
            ret = {}

            ret['asset_type'] = self.device_type_list
            ret['idc'] = self.idc_list

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
            url_name = post_data.get('url_name')
            url_method = post_data.get('url_method')
            url_memo = post_data.get('url_memo')

            # 创建url permission
            data_obj = USER_CENTER_MODELS.Permission(
                url_name=url_name,
                url_method=url_method,
                memo=url_memo,
            )
            data_obj.save()

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
            USER_CENTER_MODELS.Permission.objects.get(id=obj_id).delete()
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
            obj_id = put_data.get('obj_id')
            url_name = put_data.get('url_name')
            url_method = put_data.get('url_method')
            memo = put_data.get('memo')

            update_data = USER_CENTER_MODELS.Permission.objects.get(id=obj_id)
            update_data.url_name = url_name
            update_data.url_method = url_method
            update_data.memo = memo
            update_data.save()

        except Exception as e:
            response.status = False
            response.message = str(e)
        return response

    @staticmethod
    def assets_detail(asset_id):

        response = BaseResponse()
        try:
            print(asset_id)
            response.data = USER_CENTER_MODELS.Asset.objects.filter(id=asset_id).first()

        except Exception as e:
            response.status = False
            response.message = str(e)
        return response

    @staticmethod
    def get_data_by_id(url_nid):
        response = BaseResponse()
        try:
            response.data = USER_CENTER_MODELS.Permission.objects.filter(id=url_nid).first()

        except Exception as e:
            response.status = False
            response.message = str(e)
        return response
