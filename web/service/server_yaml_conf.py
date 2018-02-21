import json
from django.db.models import Q
from repository import models
from utils.pager import PageInfo
from utils.response import BaseResponse
from django.http.request import QueryDict

from .base import BaseServiceList
from repository import models as repository_models

import yaml


class ServerYamlConf(BaseServiceList):
    def __init__(self):
        pass

    def __json_to_yaml(self, data):
        try:
            yaml_data = yaml.dump(data)
            return yaml_data
        except:
            return False

    def __yaml_to_json(self, data):
        try:
            yaml_data = yaml.load(data)
            return yaml_data
        except:
            return False

    #@staticmethod
    def get_yaml_conf(self, request):
        response = BaseResponse()
        group_id = request.GET.get('group_id')
        try:
            get_yaml_from_db = repository_models.DockerYamlConf.objects.get(group_id__id=group_id)

            json_data = {}
            json_data['id'] = get_yaml_from_db.id
            json_data['group_id'] = get_yaml_from_db.group_id_id
            json_data['yaml_data'] = self.__json_to_yaml(json.loads(get_yaml_from_db.yaml_data))
            json_data['update_date'] = get_yaml_from_db.update_date.strftime('%Y-%m-%d %H:%M:%S')
            response.data = json_data

        except Exception as e:
            print(Exception, e)
            response.status = False
            response.message = str(e)
        return response

    def update_yaml_conf(self, request):
        response = BaseResponse()
        try:
            response.error = {}
            post_dict = QueryDict(request.body, encoding='utf-8')

            update_group_id = post_dict.get('group_id')
            yaml_conf_data = post_dict.get('yaml_conf_data')

            get_yaml_from_db = repository_models.DockerYamlConf.objects.get(group_id__id=update_group_id)
            get_yaml_from_db.yaml_data = json.dumps(self.__yaml_to_json(yaml_conf_data))
            get_yaml_from_db.save()

        except Exception as e:
            print(Exception, e)
            response.status = False
            response.message = str(e)
        return response

    def add_yaml_conf(self, request):
        response = BaseResponse()
        try:
            response.error = {}
            post_dict = QueryDict(request.body, encoding='utf-8')

            update_group_id = post_dict.get('group_id')
            yaml_conf_data = post_dict.get('yaml_conf_data')

            get_yaml_from_db = repository_models.DockerYamlConf(
                group_id = repository_models.AppGroups.objects.get(id=update_group_id),
                yaml_data = json.dumps(self.__yaml_to_json(yaml_conf_data))
            )
            get_yaml_from_db.save()

        except Exception as e:
            print(Exception, e)
            response.status = False
            response.message = str(e)
        return response