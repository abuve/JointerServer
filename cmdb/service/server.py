#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json

from django.db.models import Q
from django.http.request import QueryDict

from cmdb import models
from utils.base import BaseServiceList
from utils.pager import PageInfo
from utils.response import BaseResponse

from cmdb.service import asset_num


class Server(BaseServiceList):
    def __init__(self):
        # 查询条件的配置
        condition_config = [
            {'name': 'server__ipaddress', 'text': 'IP地址', 'condition_type': 'input'},
            {'name': 'device_type_id', 'text': '资产类型', 'condition_type': 'select', 'global_name': 'device_type_list'},
            {'name': 'device_status_id', 'text': '资产状态', 'condition_type': 'select','global_name': 'device_status_list'},
            {'name': 'idc', 'text': 'IDC机房', 'condition_type': 'select','global_name': 'idc_list'},
            {'name': 'sn', 'text': 'SN号', 'condition_type': 'input'},
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
                'q': 'server__ipaddress',
                'title': "IP地址",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@server__ipaddress'}},
                'attr': {}
            },
            {
                'q': 'server__hostname',
                'title': "主机名",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@server__hostname'}},
                'attr': {}
            },
            {
                'q': 'sn',
                'title': "SN号",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@sn'}},
                'attr': {}
            },
            {
                'q': 'device_type_id',
                'title': "资产类型",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@@device_type_list'}},
                'attr': {'name': 'device_type_id', 'id': '@device_type_id', 'origin': '@device_type_list', 'edit-enable': 'true',
                         'edit-type': 'select',
                         'global-name': 'device_type_list'}
            },
            {
                'q': 'idc_id',
                'title': "IDC机房",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@@idc_list'}},
                'attr': {'name': 'idc_id', 'id': '@idc_id', 'origin': '@idc_list', 'edit-enable': 'true',
                         'edit-type': 'select',
                         'global-name': 'idc_list'}
            },
            {
                'q': 'business_unit__parent_unit__name',
                'title': "归属业务线",
                'display': 0,
                'text': {'content': "{n}", 'kwargs': {'n': '@business_unit__parent_unit__name'}},
                'attr': {}
            },
            {
                'q': 'business_unit__name',
                'title': "归属业务线",
                'display': 1,
                'text': {'content': "<font color='red'>{business_unit__name}</font>", 'kwargs': {'business_unit__name': '@business_unit__name'}},
                'attr': {}
            },
            {
                'q': 'server__configuration',
                'title': "配置信息",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@server__configuration'}},
                'attr': {}
            },
            {
                'q': 'memo',
                'title': "备注",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@memo'}},
                'attr': {'name': 'memo', 'id': '@id', 'edit-enable': 'true', 'edit-type': 'input'}
            },
            {
                'q': 'device_status_id',
                'title': "状态",
                'display': 1,
                'text': {'content': '<a type="button" class="btn btn-{class} btn-xs">{n}</a>', 'kwargs': {'n': '@@device_status_list', 'class': '@@status_map'}},
                'attr': {'name': 'device_status_id', 'id': '@device_status_id', 'origin': '@device_status_list', 'edit-enable': 'true',
                         'edit-type': 'select','global-name': 'device_status_list'}
            },
            {
                'q': None,
                'title': "操作",
                'display': 1,
                'text': {
                    'content': '<div class="btn-group"><a type="button" href="/cmdb/asset-detail-{nid}.html" class="btn btn-default btn-xs"><span class="glyphicon glyphicon-book" aria-hidden="true"></span> 资产详情</a>   <a type="button" class="btn btn-default btn-xs" onclick="business_update_fn({nid})"><span class="glyphicon glyphicon-edit" aria-hidden="true"></span> 修改业务线</a>  <button type="button" class="btn btn-default dropdown-toggle btn-xs" data-toggle="dropdown"> <span class="caret"></span> </button> </div>',
                    'kwargs': {'device_type_id': '@device_type_id', 'nid': '@id'}},
                'attr': {}
            },
        ]
        # 额外搜索条件
        extra_select = {

        }
        super(Server, self).__init__(condition_config, table_config, extra_select)


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
        result = map(lambda x: {'id': x.id, 'name': x.name}, values)
        return list(result)

    @property
    def status_map(self):
        result = [
            {'id': 1, 'name': 'success'},
            {'id': 2, 'name': 'warning'},
            {'id': 3, 'name': 'danger'}
        ]
        return result

    @property
    def business_unit_list(self):
        values = models.BusinessUnit.objects.only('id', 'name')
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

    def fetch_assets(self, request):
        response = BaseResponse()
        try:
            ret = {}
            conditions = self.assets_condition(request)
            asset_count = models.Asset.objects.filter(conditions).count()
            page_info = PageInfo(request.GET.get('pager', None), asset_count)
            asset_list = models.Asset.objects.filter(conditions).extra(select=self.extra_select).values(
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
                'business_unit_list': self.business_unit_list,
                'status_map': self.status_map
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

    def asset_data_create(request):
        response = BaseResponse()
        try:
            asset_data = QueryDict(request.body, encoding='utf-8')
            new_asset_num = asset_num.asset_num_builder()
            asset_sn = asset_data.get('sn')

            try:
                Memory = int(asset_data.get('Memory'))
            except:
                Memory = None
            try:
                DeviceSize = int(asset_data.get('DeviceSize'))
            except:
                DeviceSize = None
            try:
                cpu_count = int(asset_data.get('cpu_count'))
            except:
                cpu_count = None

            if not asset_sn:
                asset_sn = new_asset_num

            # 创建asset obj
            asset_obj = models.Asset(
                device_type_id = asset_data.get('device_type_id'),
                asset_num = new_asset_num,
                sn = asset_sn,
                idc_id = asset_data.get('idc_id'),
                business_unit_id = asset_data.get('business_unit_id'),
            )
            asset_obj.save()

            # 创建server obj
            server_obj = models.Server(
                asset_id = asset_obj.id,
                hostname = asset_data.get('hostname'),
                ipaddress = asset_data.get('ipaddress'),
                manage_ip = asset_data.get('manage_ip'),
                Memory = Memory,
                DeviceSize = DeviceSize,
                cpu_count = cpu_count,
            )
            server_obj.save()

            response.message = '获取成功'
        except Exception as e:
            print(Exception, e)
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

        except Exception as e:
            response.status = False
            response.message = str(e)
        return response