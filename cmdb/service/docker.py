#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json

from django.db.models import Q
from django.http.request import QueryDict

from cmdb import models
from utils.base import BaseServiceList
from utils.pager import PageInfo
from utils.response import BaseResponse


class Docker(BaseServiceList):
    def __init__(self):
        # 查询条件的配置
        condition_config = [
            {'name': 'cabinet_num', 'text': '机柜号', 'condition_type': 'input'},
            {'name': 'device_type_id', 'text': '资产类型', 'condition_type': 'select', 'global_name': 'device_type_list'},
            {'name': 'device_status_id', 'text': '资产状态', 'condition_type': 'select',
             'global_name': 'device_status_list'},
        ]
        # 表格的配置
        table_config = [
            {
                'q': 'id',  # 用于数据库查询的字段，即Model.Tb.objects.filter(*[])
                'title': "ID",  # 前段表格中显示的标题
                'display': 0,  # 是否在前段显示，0表示在前端不显示, 1表示在前端隐藏, 2表示在前段显示
                'text': {'content': "{id}", 'kwargs': {'id': '@id'}},
                'attr': {'k1':'v1'}  # 自定义属性
            },
            {
                'q': 'obj_id',
                'title': "实例ID",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@obj_id'}},
                'attr': {}
            },
            {
                'q': 'name',
                'title': "实例名称",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@name'}},
                'attr': {}
            },
            {
                'q': 'asset__server__ipaddress',
                'title': "宿主机IP地址",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@asset__server__ipaddress'}},
                'attr': {}
            },
            {
                'q': 'port',
                'title': "宿主机端口",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@port'}},
                'attr': {}
            },
            {
                'q': 'cpu',
                'title': "CPU",
                'display': 1,
                'text': {'content': "{n}C", 'kwargs': {'n': '@cpu'}},
                'attr': {}
            },
            {
                'q': 'mem',
                'title': "Memory",
                'display': 1,
                'text': {'content': "{n}GB", 'kwargs': {'n': '@mem'}},
                'attr': {}
            },
            {
                'q': 'disk',
                'title': "Disk",
                'display': 1,
                'text': {'content': "{n}GB", 'kwargs': {'n': '@disk'}},
                'attr': {}
            },
            {
                'q': None,
                'title': "操作",
                'display': 1,
                'text': {
                    'content': '<div class="btn-group"><a type="button" href="/cmdb/asset-detail-{nid}.html" target="_blank" class="btn btn-default btn-xs"><span class="glyphicon glyphicon-book" aria-hidden="true"></span> Detail</a>   <a type="button" class="btn btn-default btn-xs"><span class="glyphicon glyphicon-edit" aria-hidden="true"></span> Edit</a>  <button type="button" class="btn btn-default dropdown-toggle btn-xs" data-toggle="dropdown"> <span class="caret"></span> </button> </div>',
                    #'content': "<a href='/cmdb/asset-detail-{nid}.html'>查看详细</a> | <a href='/edit-asset-{device_type_id}-{nid}.html'>编辑</a>",
                    'kwargs': {'device_type_id': '@device_type_id', 'nid': '@id'}},
                'attr': {}
            },
        ]
        # 额外搜索条件
        extra_select = {
            'server_title': 'select hostname from cmdb_server where cmdb_server.asset_id=cmdb_asset.id and cmdb_asset.device_type_id=1',
            # 'network_title': 'select management_ip from repository_networkdevice where repository_networkdevice.asset_id=repository_asset.id and repository_asset.device_type_id=2',
        }
        super(Docker, self).__init__(condition_config, table_config, extra_select)


    @property
    def device_status_list(self):
        result = map(lambda x: {'id': x[0], 'name': x[1]}, models.Asset.device_status_choices)
        return list(result)

    @property
    def device_type_list(self):
        result = map(lambda x: {'id': x[0], 'name': x[1]}, models.Asset.device_type_choices)
        return list(result)

    @property
    def idc_list(self):
        values = models.IDC.objects.only('id', 'name', 'floor')
        result = map(lambda x: {'id': x.id, 'name': "%s-%s" % (x.name, x.floor)}, values)
        return list(result)

    @property
    def business_unit_list(self):
        values = models.BusinessUnit.objects.values('id', 'name')
        return list(values)

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

    def fetch_assets(self, request):
        response = BaseResponse()
        try:
            ret = {}
            conditions = self.assets_condition(request)

            asset_count = models.DockerInstance.objects.filter(conditions).count()
            page_info = PageInfo(request.GET.get('pager', None), asset_count, request.GET.get('limit', 20))
            asset_list = models.DockerInstance.objects.filter(conditions).extra(select=self.extra_select).values(
                *self.values_list)[page_info.start:page_info.end]

            ret['table_config'] = self.table_config
            ret['condition_config'] = self.condition_config
            ret['data_list'] = list(asset_list)
            ret['page_info'] = {
                "page_str": page_info.pager(),
                "page_start": page_info.start,
            }
            ret['global_dict'] = {
                'device_status_list': self.device_status_list,
                'device_type_list': self.device_type_list,
                'idc_list': self.idc_list,
                'business_unit_list': self.business_unit_list
            }
            response.data = ret
            response.message = '获取成功'
        except Exception as e:
            response.status = False
            response.message = str(e)

        return response

    @staticmethod
    def delete_assets(request):
        response = BaseResponse()
        try:
            delete_dict = QueryDict(request.body, encoding='utf-8')
            id_list = delete_dict.getlist('id_list')
            models.Asset.objects.filter(id__in=id_list).delete()
            response.message = '删除成功'
        except Exception as e:
            response.status = False
            response.message = str(e)
        return response

    @staticmethod
    def put_assets(request):
        response = BaseResponse()
        try:
            response.error = []
            put_dict = QueryDict(request.body, encoding='utf-8')
            update_list = json.loads(put_dict.get('update_list'))
            error_count = 0
            for row_dict in update_list:
                nid = row_dict.pop('nid')
                num = row_dict.pop('num')
                try:
                    models.Asset.objects.filter(id=nid).update(**row_dict)
                except Exception as e:
                    response.error.append({'num': num, 'message': str(e)})
                    response.status = False
                    error_count += 1
            if error_count:
                response.message = '共%s条,失败%s条' % (len(update_list), error_count,)
            else:
                response.message = '更新成功'
        except Exception as e:
            response.status = False
            response.message = str(e)
        return response

    @staticmethod
    def assets_detail(asset_id):

        response = BaseResponse()
        try:
            print(asset_id)
            response.data = models.Asset.objects.filter(id=asset_id).first()
            print(response.data)

        except Exception as e:
            response.status = False
            response.message = str(e)
        return response