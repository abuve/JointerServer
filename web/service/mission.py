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


class Mission(BaseServiceList):
    def __init__(self):
        # 查询条件的配置
        condition_config = [
            {'name': 'name', 'text': 'App Name', 'condition_type': 'input'},
        ]
        # 表格的配置
        table_config = [
            {
                'q': 'id',  # 用于数据库查询的字段，即Model.Tb.objects.filter(*[])
                'title': "Mission ID",  # 前端表格中显示的标题
                'display': 1,  # 是否在前端显示，0表示在前端不显示, 1表示在前端隐藏, 2表示在前段显示
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
                'q': 'mission_type',
                'title': "Mission Type",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@@mission_type_list'}},
                'attr': {}
            },
            {
                'q': 'project__name',
                'title': "Project",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@project__name'}},
                'attr': {}
            },
            {
                'q': None,
                'title': "Status",
                'display': 0,
                'text': {'content': "{n}", 'kwargs': {'n': 'test_user'}},
                'attr': {}
            },
            {
                'q': None,
                'title': "Options",
                'display': 1,
                'text': {
                    'content': "<a href=/mission-detail-{mission_id}.html>Detail</a>",
                    'kwargs': {'mission_id': '@id'}},
                'attr': {}
            },
        ]
        # 额外搜索条件
        extra_select = {
            #'server_title': 'select hostname from repository_server where repository_server.asset_id=repository_asset.id and repository_asset.device_type_id=1',
            #'network_title': 'select management_ip from repository_networkdevice where repository_networkdevice.asset_id=repository_asset.id and repository_asset.device_type_id=2',
        }
        super(Mission, self).__init__(condition_config, table_config, extra_select)

    @property
    def mission_type_list(self):
        result = map(lambda x: {'id': x[0], 'name': x[1]}, models.Mission.mission_type_choices)
        print(result)
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
            asset_count = repository_models.Mission.objects.filter(conditions).count()
            page_info = PageInfo(request.GET.get('pager', None), asset_count)
            asset_list = repository_models.Mission.objects.filter(conditions).extra(select=self.extra_select).values(
                *self.values_list).order_by("-id")[page_info.start:page_info.end]

            ret['table_config'] = self.table_config
            ret['condition_config'] = self.condition_config
            ret['data_list'] = list(asset_list)
            ret['page_info'] = {
                "page_str": page_info.pager(),
                "page_start": page_info.start,
            }
            ret['global_dict'] = {
                'mission_type_list': self.mission_type_list
            }
            response.data = ret
            response.message = '获取成功'
        except Exception as e:
            response.status = False
            response.message = str(e)

        return response

    @staticmethod
    def add_mission(request):
        response = BaseResponse()
        post_dict = QueryDict(request.body, encoding='utf-8')
        mission_name = post_dict.get('mission_name')
        mission_type = post_dict.get('mission_type')
        project_name = post_dict.get('project_name')
        app_list = post_dict.getlist('app_list')

        print(post_dict)

        try:
            # create mission project.
            mission_project = repository_models.MissionProject(
                name = project_name
            )
            mission_project.save()

            # create mission app
            for app_id in app_list:

                mission_app = repository_models.MissionApp(
                    name=repository_models.Applications.objects.get(id=app_id).name
                )
                mission_app.save()

                # create app ip first.
                get_app_instances = repository_models.AppInstances.objects.filter(group_id__name='production', group_id__app_id__id=app_id, group_id__app_id__project_id__name=project_name).values()
                for instance_obj in get_app_instances:
                    mission_appinstance = repository_models.MissionAppInstance(
                        ip = instance_obj.get('ip')
                    )
                    mission_appinstance.save()
                    mission_app.ip.add(mission_appinstance)

                mission_project.app.add(mission_app)

            # create mission
            mission_create = repository_models.Mission(
                name = mission_name,
                mission_type = mission_type,
            )
            mission_create.save()
            mission_create.project.add(mission_project)

            response.data = {'mission_id': mission_create.id}
        except Exception as e:
            print(Exception, e)
            response.status = False
            response.message = str(e)
        return response

    def get_mission_detail_json(request, mission_id):
        response = BaseResponse()

        obj = models.Mission.objects.get(id=mission_id)
        print(obj.get_mission_type_display())

        try:
            get_mission_detail_from_db = models.MissionApp.objects.filter(mission_projects__missions__id=mission_id).values('id', 'name', 'mission_projects__name', 'status')
            response.data = list(get_mission_detail_from_db)

        except Exception as e:
            print(Exception, e)
            response.status = False
            response.message = str(e)

        return response