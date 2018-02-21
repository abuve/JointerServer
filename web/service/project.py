#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from django.db.models import Q
from repository import models
from utils.pager import PageInfo
from utils.response import BaseResponse
from django.http.request import QueryDict

from .base import BaseServiceList
from repository import models as repository_models
from cmdb import models as CMDB_MODELS

from conf import settings


class Project(BaseServiceList):
    def __init__(self):
        # 查询条件的配置
        condition_config = [
            {'name': 'name', 'text': 'Project', 'condition_type': 'input'},
        ]
        # 表格的配置
        table_config = [
            {
                'q': 'id',  # 用于数据库查询的字段，即Model.Tb.objects.filter(*[])
                'title': "Project ID",  # 前端表格中显示的标题
                'display': 0,  # 是否在前端显示，0表示在前端不显示, 1表示在前端隐藏, 2表示在前段显示
                'text': {'content': "{id}", 'kwargs': {'id': '@id'}},
                'attr': {'k1':'v1'}  # 自定义属性
            },
            {
                'q': 'name',
                'title': "Name",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@name'}},
                'attr': {}
            },
            {
                'q': 'business_unit__name',
                'title': "Business Unit",
                'display': 1,
                'text': {'content': "<font color='red'>{business_unit__parent_unit_id__name}-{business_unit__name}</font>",
                         'kwargs': {'business_unit__name': '@business_unit__name', 'business_unit__parent_unit_id__name': '@business_unit__parent_unit_id__name'}},
                'attr': {}
            },
            {
                'q': 'business_unit__parent_unit_id__name',
                'title': "Business Unit",
                'display': 0,
                'text': {'content': "<font color='red'>{business_unit__parent_unit_id__name}-{business_unit__parent_unit_id__name}</font>",
                         'kwargs': {'business_unit__parent_unit_id__name': '@business_unit__parent_unit_id__name'}},
                'attr': {}
            },
            {
                'q': None,
                'title': "Options",
                'display': 1,
                'text': {
                    'content': '<div class="btn-group">' + \
                               '<a type="button" class="btn btn-default btn-xs" href="/project/projectviews/{nid}.html"><span class="glyphicon glyphicon-eye-open" aria-hidden="true"></span> ProjectViews</a>' + \
                               '<a type="button" class="btn btn-default btn-xs" href="/project/appviews/{nid}.html"><span class="glyphicon glyphicon-eye-open" aria-hidden="true"></span> AppViews</a>' + \
                               '<a type="button" class="btn btn-default btn-xs" href="/edit-project-{nid}.html"><span class="glyphicon glyphicon-edit" aria-hidden="true"></span> Edit</a>' + \
                               '<a type="button" class="btn btn-default btn-xs" onclick=delete_project_data_fn({nid})><span class="glyphicon glyphicon-remove" aria-hidden="true"></span> Delete</a>' + \
                               '<button type="button" class="btn btn-default dropdown-toggle btn-xs"data-toggle="1dropdown"> <span class="caret"></span> <span class="sr-only">切换下拉菜单</span> </button> <ul class="dropdown-menu" role="menu" style="margin:2px 164px; min-width:130px"> <li><a href="#">More Option</a></li> </ul>' + \
                                '</div>',
                    'kwargs': {'device_type_id': '@device_type_id', 'nid': '@id', 'name': '@name'}},
                'attr': {'style': 'text-align: center','width': '360px'}
            },
        ]
        # 额外搜索条件
        extra_select = {
            #'server_title': 'select hostname from repository_server where repository_server.asset_id=repository_asset.id and repository_asset.device_type_id=1',
            #'network_title': 'select management_ip from repository_networkdevice where repository_networkdevice.asset_id=repository_asset.id and repository_asset.device_type_id=2',
        }
        super(Project, self).__init__(condition_config, table_config, extra_select)



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

    def fetch_project(self, request):
        response = BaseResponse()
        try:
            ret = {}
            conditions = self.assets_condition(request)
            project_count = models.ProjectInfo.objects.filter(conditions).count()
            page_info = PageInfo(request.GET.get('pager', None), project_count)
            project_list = models.ProjectInfo.objects.filter(conditions).extra(select=self.extra_select).values(
                *self.values_list).order_by("-id")[page_info.start:page_info.end]
            ret['table_config'] = self.table_config
            ret['condition_config'] = self.condition_config
            ret['data_list'] = list(project_list)
            ret['page_info'] = {
                "page_str": page_info.pager(),
                "page_start": page_info.start,
            }

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
            project_id = recv_data.get("project_id")
            repository_models.ProjectInfo.objects.get(id=project_id).delete()
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

            print(post_dict)
            project_name = post_dict.get('project_name')
            business_unit_id = post_dict.get('business_unit_id')

            add_to_db = repository_models.ProjectInfo(
                name=project_name,
                business_unit=CMDB_MODELS.BusinessUnit.objects.get(id=business_unit_id),

            )
            add_to_db.save()

        except Exception as e:
            print(Exception, e)
            response.status = False
            response.message = str(e)
        return response

    @staticmethod
    def put_assets(request):
        response = BaseResponse()
        try:
            response.error = []
            put_dict = QueryDict(request.body, encoding='utf-8')
            project_id = put_dict.get('project_id')
            project_name = put_dict.get('project_name')
            business_unit_id = put_dict.get('business_unit_id')

            update_data = repository_models.ProjectInfo.objects.get(id=project_id)
            update_data.name = project_name
            update_data.business_unit = CMDB_MODELS.BusinessUnit.objects.get(id=business_unit_id)
            update_data.save()

        except Exception as e:
            print(Exception,e)
            response.status = False
            response.message = str(e)
        return response

    @staticmethod
    def project_config(project_id):
        response = BaseResponse()
        try:
            response.data = models.ProjectInfo.objects.filter(id=project_id).first()
            td_rowspan = {}
            for app_obj in response.data.applications.all():
                count = 1
                for group_obj in app_obj.groups.all():
                    count += len(group_obj.webconfiglogscenter.all())
                td_rowspan[app_obj.name] = count
            print(td_rowspan)
            response.td_rowspan = td_rowspan
        except Exception as e:
            print(Exception, e)
            response.status = False
            response.message = str(e)
        return response