#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json

from django.db.models import Q
from django.http.request import QueryDict

from cmdb import models
from user_center import models as user_center_models
from utils.base import BaseServiceList
from utils.pager import PageInfo
from utils.response import BaseResponse


class Business(BaseServiceList):
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
                'attr': {'k1': 'v1'}  # 自定义属性
            },
            {
                'q': 'obj_id',
                'title': "Container ID",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@obj_id'}},
                'attr': {}
            },
            {
                'q': 'name',
                'title': "Container Name",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@name'}},
                'attr': {}
            },
            {
                'q': 'asset__server__ipaddress',
                'title': "Host IP",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@asset__server__ipaddress'}},
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
                'title': "Options",
                'display': 1,
                'text': {
                    'content': '<div class="btn-group"><a type="button" href="/cmdb/asset-detail-{nid}.html" target="_blank" class="btn btn-default btn-xs"><span class="glyphicon glyphicon-book" aria-hidden="true"></span> Detail</a>   <a type="button" class="btn btn-default btn-xs"><span class="glyphicon glyphicon-edit" aria-hidden="true"></span> Edit</a>  <button type="button" class="btn btn-default dropdown-toggle btn-xs" data-toggle="dropdown"> <span class="caret"></span> </button> </div>',
                    # 'content': "<a href='/cmdb/asset-detail-{nid}.html'>查看详细</a> | <a href='/edit-asset-{device_type_id}-{nid}.html'>编辑</a>",
                    'kwargs': {'device_type_id': '@device_type_id', 'nid': '@id'}},
                'attr': {}
            },
        ]
        # 额外搜索条件
        extra_select = {
            'server_title': 'select hostname from cmdb_server where cmdb_server.asset_id=cmdb_asset.id and cmdb_asset.device_type_id=1',
            # 'network_title': 'select management_ip from repository_networkdevice where repository_networkdevice.asset_id=repository_asset.id and repository_asset.device_type_id=2',
        }
        super(Business, self).__init__(condition_config, table_config, extra_select)

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
        add_data = request.GET.get('add', None)
        edit_data = request.GET.get('edit', None)
        get_from = request.GET.get('from', None)
        try:
            ret = [
                # { 'id':1, 'pId':0, 'name':"父节点 1", 'open': True},
                # {'id': 11, 'pId': 1, 'name': "叶子节点 1-1"},
            ]

            if get_from == "cmdb_asset_create":
                open_tag = False
                callback="select_business_node(this, %s);"
            else:
                open_tag = True
                callback = "get_business_detail_fn(%d);"

            get_data = models.BusinessUnit.objects.all()
            for obj in get_data:
                if not obj.parent_unit:
                    dict = {'id': obj.id, 'pId': 0, 'name': obj.name, 'open': open_tag,
                            "click": callback % obj.id}
                    ret.append(dict)
                    for child in obj.parent_level.all():
                        dict = {'id': child.id, 'pId': obj.id, 'name': child.name, 'open': open_tag,
                                "click": callback % child.id}
                        ret.append(dict)

            # add data, get other info from db.
            if add_data:
                response.group_data = self.get_user_groups

            if edit_data:
                response.group_data = self.get_user_groups
                obj_id = request.GET.get('obj_id')
                response.edit_data = self.get_business_detail_json(obj_id)

            response.data = ret
            response.message = '获取成功'
        except Exception as e:
            print(Exception, e)
            response.status = False
            response.message = str(e)

        return response

    @staticmethod
    def delete_data(request):
        response = BaseResponse()
        try:
            delete_dict = QueryDict(request.body, encoding='utf-8')
            obj_id = delete_dict.get('obj_id')
            models.BusinessUnit.objects.filter(id=obj_id).delete()
            response.message = '删除成功'
        except Exception as e:
            response.status = False
            response.message = str(e)
        return response

    @staticmethod
    def put_data(request):
        response = BaseResponse()
        try:
            post_dict = QueryDict(request.body, encoding='utf-8')

            obj_id = post_dict.get('obj_id', None)
            add_business_parent_id = post_dict.get('add_business_parent_id', None)
            add_business_name = post_dict.get('add_business_name')
            add_business_admin_list = post_dict.getlist('add_business_admin_list', [])
            add_business_contact_list = post_dict.getlist('add_business_contact_list', [])
            add_business_memo = post_dict.get('add_business_memo')

            edit_data_to_db = models.BusinessUnit.objects.get(id=obj_id)

            # 如果业务线包含子类，不允许更换至其他父级分组
            if not edit_data_to_db.parent_level.all():
                edit_data_to_db.parent_unit_id = add_business_parent_id
            else:
                response.message = "this is text."
            edit_data_to_db.name = add_business_name
            edit_data_to_db.memo = add_business_memo
            edit_data_to_db.save()

            edit_data_to_db.manager.clear()
            edit_data_to_db.contact.clear()

            for obj_id in add_business_admin_list:
                edit_data_to_db.manager.add(user_center_models.UserGroup.objects.get(id=obj_id))
            for obj_id in add_business_contact_list:
                edit_data_to_db.contact.add(user_center_models.UserGroup.objects.get(id=obj_id))

        except Exception as e:
            response.status = False
            response.message = str(e)
        return response

    def add_data(self, request):
        response = BaseResponse()
        try:
            post_dict = QueryDict(request.body, encoding='utf-8')

            add_business_parent_id = post_dict.get('add_business_parent_id', None)
            add_business_name = post_dict.get('add_business_name')
            add_business_admin_list = post_dict.getlist('add_business_admin_list', [])
            add_business_contact_list = post_dict.getlist('add_business_contact_list', [])
            add_business_memo = post_dict.get('add_business_memo')

            add_data_to_db = models.BusinessUnit(
                parent_unit_id=add_business_parent_id,
                name=add_business_name,
                memo=add_business_memo
            )

            add_data_to_db.save()

            for obj_id in add_business_admin_list:
                add_data_to_db.manager.add(user_center_models.UserGroup.objects.get(id=obj_id))
            for obj_id in add_business_contact_list:
                add_data_to_db.contact.add(user_center_models.UserGroup.objects.get(id=obj_id))

        except Exception as e:
            response.status = False
            response.message = str(e)
        return response

    @staticmethod
    def get_buesiness_detail(business_nid):
        response = BaseResponse()
        try:
            response.data = models.BusinessUnit.objects.get(id=business_nid)

        except Exception as e:
            response.status = False
            response.message = str(e)
        return response

    # public functions
    @property
    def get_user_groups(self):
        result = user_center_models.UserGroup.objects.values()
        return (list(result))

    def get_business_detail_json(self, obj_id):
        result = models.BusinessUnit.objects.filter(id=obj_id).values()[0]

        manager_groups = models.BusinessUnit.objects.filter(id=obj_id).values_list('manager')
        contact_groups = models.BusinessUnit.objects.filter(id=obj_id).values_list('contact')

        result['manager_groups'] = list(manager_groups)
        result['contact_groups'] = list(contact_groups)

        return result
