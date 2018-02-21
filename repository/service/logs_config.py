import json
from django.db.models import Q
from repository import models
from utils.pager import PageInfo
from utils.response import BaseResponse
from django.http.request import QueryDict

from .base import BaseServiceList
from repository import models as repository_models
from cmdb import models as CMDB_MODELS


class ServerLogs(BaseServiceList):
    def __init__(self):
        pass

    @staticmethod
    def get_server_logs(server_id):
        response = BaseResponse()
        try:
            response.data = models.Applications.objects.filter(id=server_id).first()

        except Exception as e:
            print(Exception, e)
            response.status = False
            response.message = str(e)
        return response

    @staticmethod
    def get_server_logs_json(server_id):
        response = BaseResponse()

        try:
            server_logs_list = repository_models.WebConfigLogsCenter.objects.filter(group_id__app_id=server_id).values(
                                                                                              'id',
                                                                                              'url',
                                                                                              'memo',
                                                                                              'group_id__name',
                                                                                              'group_id__app_id__name',
                                                                                              'group_id__app_id__project_id__name',
                                                                                              ).order_by("-id")
            response.data = list(server_logs_list)
        except Exception as e:
            print(Exception, e)
            response.status = False
            response.message = str(e)
        return response

    def add_server_logs(request):
        response = BaseResponse()
        try:
            response.error = {}
            post_dict = QueryDict(request.body, encoding='utf-8')

            add_logs_group_id = post_dict.get('add_logs_group_id')
            add_server_log_url = post_dict.get('add_server_log_url')
            add_server_log_memo = post_dict.get('add_server_log_memo')

            add_to_db = repository_models.WebConfigLogsCenter(
                group_id_id = add_logs_group_id,
                url = add_server_log_url,
                memo = add_server_log_memo
            )
            add_to_db.save()

        except Exception as e:
            print(Exception, e)
            response.status = False
            response.message = str(e)
        return response

    def delete_server_logs(request):
        response = BaseResponse()
        try:
            response.error = {}
            post_dict = QueryDict(request.body, encoding='utf-8')

            log_id = post_dict.get('log_id')

            add_to_db = repository_models.WebConfigLogsCenter.objects.get(id=log_id)
            add_to_db.delete()

        except Exception as e:
            response.status = False
            response.message = str(e)
        return response

    def update_server_logs(request):
        response = BaseResponse()
        try:
            response.error = {}
            post_dict = QueryDict(request.body, encoding='utf-8')

            log_id = post_dict.get('log_id')
            add_server_log_url = post_dict.get('add_server_log_url')
            add_server_log_memo = post_dict.get('add_server_log_memo')

            get_logs_from_db = repository_models.WebConfigLogsCenter.objects.get(id=log_id)
            get_logs_from_db.url = add_server_log_url
            get_logs_from_db.memo = add_server_log_memo
            get_logs_from_db.save()

        except Exception as e:
            print(Exception, e)
            response.status = False
            response.message = str(e)
        return response

    def get_logs_by_id(request):
        response = BaseResponse()
        log_id = request.GET.get('log_id')
        get_edit_logs_data = repository_models.WebConfigLogsCenter.objects.filter(id=log_id).values("id", "group_id_id", "url", "memo")
        response.data = list(get_edit_logs_data)
        return response.data
