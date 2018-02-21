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
    def get_server_groups(server_id):
        response = BaseResponse()
        try:
            response.data = models.Applications.objects.filter(id=server_id).first()

        except Exception as e:
            print(Exception, e)
            response.status = False
            response.message = str(e)
        return response

    @staticmethod
    def get_server_groups_json(request, server_id):
        response = BaseResponse()

        try:
            get_public_group_tag = request.GET.get('public_group')
            # from django.db.models import Count
            if get_public_group_tag:
                get_group_from_db = models.AppGroups.objects.filter(group_type=1).values('id', 'name',
                                                                                                 'app_id__name',
                                                                                                 'app_id__project_id__name',
                                                                                                 'group_type').order_by("-id")
            else:
                get_group_from_db = models.AppGroups.objects.filter(app_id__id=server_id).values('id', 'name',
                                                                                                 'app_id__name',
                                                                                                 'app_id__project_id__name',
                                                                                                 'group_type').order_by("-id")
            response.data = list(get_group_from_db)
        except Exception as e:
            print(Exception, e)
            response.status = False
            response.message = str(e)
        return response

    def add_server_group(request):
        response = BaseResponse()
        try:
            response.error = {}
            print(request.body)
            post_dict = QueryDict(request.body, encoding='utf-8')

            add_group_app_id = post_dict.get('add_group_app_id')
            add_group_name = post_dict.get('add_group_name')
            add_group_yaml_path = post_dict.get('add_group_yaml_path')
            add_group_type = post_dict.get('add_group_type')

            add_to_db = repository_models.AppGroups(
                name=add_group_name,
                yaml_path=add_group_yaml_path,
                # app_id = repository_models.Applications.objects.get(id=add_group_app_id)
                group_type=add_group_type,
            )

            add_to_db.save()
            add_to_db.app_id.add(repository_models.Applications.objects.get(id=add_group_app_id))

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
            add_group_type = post_dict.get('add_group_type')

            get_group_from_db = repository_models.AppGroups.objects.get(id=update_group_id)
            get_group_from_db.name = add_group_name
            get_group_from_db.yaml_path = add_group_yaml_path
            get_group_from_db.group_type = add_group_type
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

    @staticmethod
    def get_public_group(request):
        response = BaseResponse()

        try:
            get_group_from_db = models.AppGroups.objects.filter(group_type=1).values('id', 'name',
                                                                                     'app_id__name',
                                                                                     'app_id__project_id__name',
                                                                                     'group_type').order_by("-id")
            id_list = []
            data_list = []
            for obj in get_group_from_db:
                if obj.get('id') not in id_list:
                    data_list.append(obj)
                    id_list.append(obj.get('id'))
            response.data = data_list
        except Exception as e:
            print(Exception, e)
            response.status = False
            response.message = str(e)
        return response

    @staticmethod
    def bond_public_group(request):
        response = BaseResponse()

        try:
            post_dict = QueryDict(request.body, encoding='utf-8')

            add_group_app_id = post_dict.get('add_group_app_id')
            public_group_id = post_dict.get('public_group_id')

            print(public_group_id)

            get_group_from_db = models.AppGroups.objects.get(id=public_group_id)
            print(get_group_from_db)
            get_group_from_db.app_id.add(repository_models.Applications.objects.get(id=add_group_app_id))

        except Exception as e:
            print(Exception, e)
            response.status = False
            response.message = str(e)
        return response