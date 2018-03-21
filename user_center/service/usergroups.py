# -*- coding: utf-8 -*-
# @Time    : 1/26/2018 10:25 AM
# @Author  : Abbott
# @Site    : 
# @File    : userprofile.py
# @Software: PyCharm

import json
from django.db.models import Q
from repository import models
from utils.pager import PageInfo
from utils.response import BaseResponse
from django.http.request import QueryDict

from utils.base import BaseServiceList
from repository import models as repository_models
from cmdb import models as CMDB_MODELS
from user_center import models as user_models
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from conf import settings


class UserGroups(BaseServiceList):
    def __init__(self):
        # 查询条件的配置
        condition_config = [
            {'name': 'name', 'text': '分组名称', 'condition_type': 'input'},
        ]
        # 表格的配置
        table_config = [
            {
                'q': 'id',  # 用于数据库查询的字段，即Model.Tb.objects.filter(*[])
                'title': "User ID",  # 前端表格中显示的标题
                'display': 0,  # 是否在前端显示，0表示在前端不显示, 1表示在前端隐藏, 2表示在前段显示
                'text': {'content': "{id}", 'kwargs': {'id': '@id'}},
                'attr': {'k1':'v1'}  # 自定义属性
            },
            {
                'q': 'name',
                'title': "分组名称",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@name'}},
                'attr': {}
            },

            {
                'q': None,
                'title': "操作",
                'display': 1,
                'text': {
                    'content': '<div class="btn-group">' + \
                                '<a type="button" class="btn btn-default btn-xs" href="/user_center/edit-group-{nid}.html"><span class="glyphicon glyphicon-edit" aria-hidden="true"></span> 编辑</a>' + \
                               '<a type="button" class="btn btn-default btn-xs" onclick=delete_group_data_fn({nid})><span class="glyphicon glyphicon-remove" aria-hidden="true"></span> 删除</a>' + \
                               '<button type="button" class="btn btn-default dropdown-toggle btn-xs"data-toggle="1dropdown"> <span class="caret"></span> <span class="sr-only">切换下拉菜单</span> </button> <ul class="dropdown-menu" role="menu" style="margin:2px 164px; min-width:130px"> <li><a href="#">More Option</a></li> </ul>' + \
                                '</div>',
                    'kwargs': {'device_type_id': '@device_type_id', 'nid': '@id', 'name': '@name'}},
                'attr': {'width': '300px'}
            },
        ]
        # 额外搜索条件
        extra_select = {
            #'server_title': 'select hostname from repository_server where repository_server.asset_id=repository_asset.id and repository_asset.device_type_id=1',
            #'network_title': 'select management_ip from repository_networkdevice where repository_networkdevice.asset_id=repository_asset.id and repository_asset.device_type_id=2',
        }
        super(UserGroups, self).__init__(condition_config, table_config, extra_select)

    # @property
    # def group_list(self):
    #     result = map(lambda x: {'id': x[0], 'name': x[1]}, user_models.UserGroup.objects.values_list())
    #     return list(result)

    def get_group_info(request):
        response = BaseResponse()
        try:
            response.data = user_models.UserGroup.objects.all()
        except Exception as e:
            response.status = False
            response.message = str(e)
        return response


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

    def fetch_group(self, request):
        response = BaseResponse()
        try:
            ret = {}
            conditions = self.assets_condition(request)
            group_count = user_models.UserGroup.objects.filter(conditions).count()
            page_info = PageInfo(request.GET.get('pager', None), group_count)
            group_list = user_models.UserGroup.objects.filter(conditions).extra(select=self.extra_select).values(
                *self.values_list).order_by("-id")[page_info.start:page_info.end]
            ret['table_config'] = self.table_config
            ret['condition_config'] = self.condition_config
            ret['data_list'] = list(group_list)
            ret['page_info'] = {
                "page_str": page_info.pager(),
                "page_start": page_info.start,
            }
            # ret['global_dict'] = {
            #     "group_list": self.group_list
            # }

            response.data = ret
            response.message = '获取成功'
        except Exception as e:
            response.status = False
            response.message = str(e)

        return response

    @staticmethod
    def delete_data(request):
        response = BaseResponse()
        try:
            recv_data = QueryDict(request.body, encoding='utf-8')
            group_id = recv_data.get("group_id")
            user_models.UserGroup.objects.get(id=group_id).delete()
            response.message = '删除成功'
        except Exception as e:
            response.status = False
            response.message = str(e)
        return response

    @staticmethod
    def add_data(request):
        response = BaseResponse()
        try:
            response.error = []
            post_dict = QueryDict(request.body, encoding='utf-8')

            # print(post_dict)
            group_name = post_dict.get('group_name')

            add_to_db = user_models.UserGroup(
                name=group_name,

            )
            add_to_db.save()

        except Exception as e:
            print(Exception, e)
            response.status = False
            response.message = str(e)
        return response

    @staticmethod
    def put_data(request):
        response = BaseResponse()
        try:
            response.error = []
            put_dict = QueryDict(request.body, encoding='utf-8')
            user_id = put_dict.get('group_id')
            group_name = put_dict.get('group_name')

            update_data = user_models.UserGroup.objects.get(id=user_id)

            update_data.name = group_name
            update_data.save()

        except Exception as e:
            print(Exception,e)
            response.status = False
            response.message = str(e)
        return response

    @staticmethod
    def group_config(group_id):

        response = BaseResponse()
        try:
            response.data = user_models.UserGroup.objects.filter(id=group_id).first()

        except Exception as e:
            print(Exception, e)
            response.status = False
            response.message = str(e)
        return response