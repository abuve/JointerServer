import json
from django.db.models import Q
from repository import models
from utils.pager import PageInfo
from utils.response import BaseResponse
from django.http.request import QueryDict

from .base import BaseServiceList
from repository import models as repository_models


class ServerProject(BaseServiceList):
    def __init__(self):
        # 查询条件的配置
        condition_config = [
            {'name': 'name', 'text': 'App Name', 'condition_type': 'input'},
        ]
        # 表格的配置
        table_config = [
            {
                'q': 'id',  # 用于数据库查询的字段，即Model.Tb.objects.filter(*[])
                'title': "APP ID",  # 前端表格中显示的标题
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
                'q': None,
                'title': "System",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': 'test_system'}},
                'attr': {}
            },
            {
                'q': 'app_type',
                'title': "Type",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@app_type'}},
                'attr': {}
            },
            {
                'q': None,
                'title': "Leader",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': 'test_user'}},
                'attr': {}
            },
            {
                'q': None,
                'title': "Options",
                'display': 1,
                'text': {
                    'content': '<div class="btn-group">' + \
                                '<a type="button" class="btn btn-default btn-xs" href="/server-config-{nid}.html"><span class="glyphicon glyphicon-edit" aria-hidden="true"></span> Config</a>' + \
                                '<a type="button" class="btn btn-default btn-xs" href="/edit-asset-{device_type_id}-{nid}.html"><span class="glyphicon glyphicon-edit" aria-hidden="true"></span> Edit</a>' + \
                                '<a type="button" class="btn btn-default btn-xs" ><span class="glyphicon glyphicon-remove" aria-hidden="true"></span> Delete</a>' + \
                                '<button type="button" class="btn btn-default dropdown-toggle btn-xs"data-toggle="1dropdown"> <span class="caret"></span> <span class="sr-only">切换下拉菜单</span> </button> <ul class="dropdown-menu" role="menu" style="margin:2px 164px; min-width:130px"> <li><a href="#">More Option</a></li> </ul>' + \
                                    '</div>',
                    'kwargs': {'device_type_id': '@device_type_id', 'nid': '@id'}},
                'attr': {'width': '300px'}
            },
        ]
        # 额外搜索条件
        extra_select = {
            #'server_title': 'select hostname from repository_server where repository_server.asset_id=repository_asset.id and repository_asset.device_type_id=1',
            #'network_title': 'select management_ip from repository_networkdevice where repository_networkdevice.asset_id=repository_asset.id and repository_asset.device_type_id=2',
        }
        #super(Server, self).__init__(condition_config, table_config, extra_select)

    # 用于创建app获取父级project信息
    def get_project_info(request):
        response = BaseResponse()
        try:
            response.data = repository_models.ProjectInfo.objects.all()
        except Exception as e:
            response.status = False
            response.message = str(e)
        return response

    # 返回项目应用组件
    @staticmethod
    def get_app_by_project(request):
        response = BaseResponse()
        post_dict = QueryDict(request.body, encoding='utf-8')
        project_id = post_dict.get('project_id')
        try:
            data_list = repository_models.Applications.objects.filter(project_id__id=project_id).values()
            response.data = list(data_list)

        except Exception as e:
            response.status = False
            response.message = str(e)
        return response