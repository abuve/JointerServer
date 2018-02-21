import json
from django.db.models import Q
from repository import models
from utils.pager import PageInfo
from utils.response import BaseResponse
from django.http.request import QueryDict

from .base import BaseServiceList
from repository import models as repository_models
from cmdb import models as CMDB_MODELS


class ServerDocker(BaseServiceList):
    def __init__(self):
        pass

    @staticmethod
    def get_asset_instance(server_id):
        response = BaseResponse()
        try:
            response.data = models.Applications.objects.filter(id=server_id).first()
            # 返回docker宿主机
            response.asset_data = CMDB_MODELS.Asset.objects.filter(device_type_id=2)

        except Exception as e:
            print(Exception, e)
            response.status = False
            response.message = str(e)
        return response

    @staticmethod
    def get_server_instances_json(server_id):
        response = BaseResponse()

        try:
            instance_asset_list = CMDB_MODELS.DockerInstance.objects.filter(dockers__app_id=server_id).values('id', 'obj_id',
                                                                                              'name',
                                                                                              'port',
                                                                                              'dockers__id',
                                                                                              'dockers__name',
                                                                                              'dockers__app_id__name',
                                                                                              'asset__server__ipaddress',
                                                                                              'dockers__app_id__project_id__name').order_by("-id")
            response.data = list(instance_asset_list)
        except Exception as e:
            print(Exception, e)
            response.status = False
            response.message = str(e)
        return response

    def add_server_instance(request):
        response = BaseResponse()
        try:
            response.error = {}
            post_dict = QueryDict(request.body, encoding='utf-8')

            add_docker_group_id = post_dict.get('add_docker_group_id')
            add_docker_id = post_dict.get('add_docker_id')

            add_to_db = repository_models.AppGroups.objects.get(id=add_docker_group_id)
            add_to_db.docker.add(CMDB_MODELS.DockerInstance.objects.get(id=add_docker_id))

        except Exception as e:
            response.status = False
            response.message = str(e)
        return response

    def delete_server_instance(request):
        response = BaseResponse()
        try:
            response.error = {}
            post_dict = QueryDict(request.body, encoding='utf-8')

            group_id = post_dict.get('group_id')
            docker_id = post_dict.get('docker_id')

            add_to_db = repository_models.AppGroups.objects.get(id=group_id)
            add_to_db.docker.remove(CMDB_MODELS.DockerInstance.objects.get(id=docker_id))

        except Exception as e:
            response.status = False
            response.message = str(e)
        return response

    def update_server_instance(request):
        response = BaseResponse()
        try:
            response.error = {}
            post_dict = QueryDict(request.body, encoding='utf-8')

            docker_group_id = post_dict.get('docker_group_id')
            new_docker_id = post_dict.get('new_docker_id')
            old_docker_id = post_dict.get('old_docker_id')

            get_group_from_db = repository_models.AppGroups.objects.get(id=docker_group_id)
            get_group_from_db.docker.remove(CMDB_MODELS.DockerInstance.objects.get(id=old_docker_id))
            get_group_from_db.docker.add(CMDB_MODELS.DockerInstance.objects.get(id=new_docker_id))

        except Exception as e:
            print(Exception, e)
            response.status = False
            response.message = str(e)
        return response

    def get_docker_by_id(request):
        response = BaseResponse()
        docker_id = request.GET.get('docker_id')
        get_edit_docker_data = CMDB_MODELS.DockerInstance.objects.filter(id=docker_id).values("id", "dockers__id", "asset__id")
        response.data = list(get_edit_docker_data)
        return response.data
