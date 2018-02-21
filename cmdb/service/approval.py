#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json

from django.db.models import Q
from django.http.request import QueryDict

from cmdb import models
from utils.base import BaseServiceList
from utils.pager import PageInfo
from utils.response import BaseResponse

from cmdb.service import client_report_handler


class Approval(BaseServiceList):
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
                'q': 'ipaddress',
                'title': "IP Addr",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@ipaddress'}},
                'attr': {}
            },
            {
                'q': 'hostname',
                'title': "主机名",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@hostname'}},
                'attr': {}
            },
            {
                'q': 'sn',
                'title': "SN",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@sn'}},
                'attr': {}
            },
            {
                'q': 'manufactory',
                'title': "Manufactory",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@manufactory'}},
                'attr': {}
            },
            {
                'q': 'model',
                'title': "Model",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@model'}},
                'attr': {}
            },
            {
                'q': 'os_release',
                'title': "OS Version",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@os_release'}},
                'attr': {}
            },
            {
                'q': 'approved',
                'title': "Status",
                'display': 1,
                'text': {
                    'content': "<a type='button' class='btn btn-warning btn-xs'>Approved</a>",
                    'kwargs': {'n': '@approved'}},
                'attr': {}
            },
            {
                'q': None,
                'title': "选项",
                'display': 1,
                'text': {
                    'content': "<a href='/asset-{device_type_id}-{nid}.html'>查看详细</a> | <a href='/edit-asset-{device_type_id}-{nid}.html'>编辑</a>",
                    'kwargs': {'device_type_id': '@device_type_id', 'nid': '@id'}},
                'attr': {}
            },
        ]
        # 额外搜索条件
        extra_select = {
            'server_title': 'select hostname from cmdb_server where cmdb_server.asset_id=cmdb_asset.id and cmdb_asset.device_type_id=1',
            # 'network_title': 'select management_ip from repository_networkdevice where repository_networkdevice.asset_id=repository_asset.id and repository_asset.device_type_id=2',
        }
        super(Approval, self).__init__(condition_config, table_config, extra_select)


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
            asset_count = models.NewAssetApprovalZone.objects.filter(conditions).count()
            page_info = PageInfo(request.GET.get('pager', None), asset_count)
            asset_list = models.NewAssetApprovalZone.objects.filter(conditions).extra(select=self.extra_select).values(
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

    def new_assets_approval(request):
        if request.method == 'POST':
            request.POST = request.POST.copy()
            approved_asset_list = request.POST.getlist('approved_asset_list')
            get_approved_asset_list = CMDB_MODELS.NewAssetApprovalZone.objects.filter(id__in=approved_asset_list)

            approved_count = 0
            for obj in get_approved_asset_list:
                request.POST['asset_data'] = obj.data
                ass_handler = client_report_handler.Asset(request)
                if ass_handler.data_is_valid_without_id():
                    ass_handler.data_inject()
                    obj.approved = True
                    obj.approved_date = datetime.datetime.now()
                    obj.save()
                    approved_count += 1

            return_data = {'code': 1, 'msg': 'Total submit %s rows, approved %s rows!' % (
            len(approved_asset_list), approved_count)}
            return HttpResponse(json.dumps(return_data))

    @staticmethod
    def approved_data(request):
        response = BaseResponse()
        try:
            response.error = []
            id_list = QueryDict(request.body, encoding='utf-8').getlist('id_list')
            error_count = 0
            ass_handler = client_report_handler.Asset(request)
            for obj_id in id_list:
                try:
                    # 调用接口新增审批资产数据
                    get_source_data = models.NewAssetApprovalZone.objects.filter(id=obj_id)
                    json_data = json.loads(get_source_data[0].data)
                    request.POST = {"asset_data": json_data}
                    ass_handler = client_report_handler.Asset(request)
                    if ass_handler.data_is_valid_without_id():
                        ass_handler.data_inject()
                        models.NewAssetApprovalZone.objects.filter(id=obj_id).update(approved=True, asset_resume_num=ass_handler.asset_obj.asset_num)
                    else:
                        error_count += 1
                        response.error.append({'id': "ID %s" %obj_id, 'message': "Asset already exist."})

                except Exception as e:
                    response.error.append({'id': obj_id, 'message': str(e)})
                    response.status = False
                    error_count += 1

            if error_count:
                response.message = '共%s条,失败%s条' % (len(id_list), error_count,)
                response.status = False
            else:
                response.message = '更新成功'
        except Exception as e:
            response.status = False
            response.message = str(e)
        return response

    @staticmethod
    def assets_detail(device_type_id, asset_id):

        response = BaseResponse()
        try:
            if device_type_id == '1':
                response.data = models.Server.objects.filter(asset_id=asset_id).select_related('asset').first()
            else:
                response.data = models.NetworkDevice.objects.filter(asset_id=asset_id).select_related('asset').first()

        except Exception as e:
            response.status = False
            response.message = str(e)
        return response