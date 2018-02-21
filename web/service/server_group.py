import json
from django.db.models import Q
from repository import models
from utils.pager import PageInfo
from utils.response import BaseResponse
from django.http.request import QueryDict

from .base import BaseServiceList
from repository import models as repository_models


class ServerGroup(BaseServiceList):
    def __init__(self):
        pass

    @staticmethod
    def get_server_groups_json(server_id):
        response = BaseResponse()

        try:
            from django.db.models import Count
            get_group_from_db = models.AppGroups.objects.filter(app_id__id=server_id).values('id', 'name', 'app_id__name', 'app_id__project_id__name', 'group_type').order_by("-id")
            response.data = list(get_group_from_db)
        except Exception as e:
            print(Exception, e)
            response.status = False
            response.message = str(e)
        return response.data

    def add_server_group(request):
        response = BaseResponse()
        try:
            response.error = {}
            print(request.body)
            post_dict = QueryDict(request.body, encoding='utf-8')

            add_group_app_id = post_dict.get('add_group_app_id')
            add_group_name = post_dict.get('add_group_name')
            add_group_yaml_path = post_dict.get('add_group_yaml_path')

            add_to_db = repository_models.AppGroups(
                name = add_group_name,
                yaml_path = add_group_yaml_path,
                app_id = repository_models.Applications.objects.get(id=add_group_app_id)
            )
            add_to_db.save()

        except Exception as e:
            print(Exception, e)
            response.status = False
            response.message = str(e)
        return response

    def update_server_group(request):
        response = BaseResponse()
        try:
            response.error = {}
            post_dict = QueryDict(request.body, encoding='utf-8')

            update_group_id = post_dict.get('group_id')
            add_group_name = post_dict.get('add_group_name')
            add_group_yaml_path = post_dict.get('add_group_yaml_path')

            get_group_from_db = repository_models.AppGroups.objects.get(id=update_group_id)
            get_group_from_db.name = add_group_name
            get_group_from_db.yaml_path = add_group_yaml_path
            get_group_from_db.save()

        except Exception as e:
            print(Exception, e)
            response.status = False
            response.message = str(e)
        return response

    def delete_server_group(request):
        response = BaseResponse()
        try:
            response.error = {}
            post_dict = QueryDict(request.body, encoding='utf-8')

            delete_group_id = post_dict.get('group_id')

            get_group_from_db = repository_models.AppGroups.objects.get(id=delete_group_id)
            get_group_from_db.delete()

        except Exception as e:
            print(Exception, e)
            response.status = False
            response.message = str(e)
        return response

    def get_group_by_id(request):
        response = BaseResponse()
        group_id = request.GET.get('group_id')
        get_edit_group_data = repository_models.AppGroups.objects.filter(id=group_id).values()
        response.data = list(get_edit_group_data)
        return response.data
