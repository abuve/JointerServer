#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import os
import datetime

from django.db.models import Q
from django.http.request import QueryDict

from cmdb import models as CMDB_MODELS
from repository import models as REST_MODELS
from utils.base import BaseServiceList
from utils.pager import PageInfo
from utils.response import BaseResponse

from repository import models as repository_models
from cmdb import models as CMDB_MODELS

from conf.settings import web_conf_path
from repository.cores import FileHandler

from conf import settings


class WebConfig(BaseServiceList):
    def __init__(self):
        pass

    def nginx_config(self, server_id):

        response = BaseResponse()
        try:
            response.data = REST_MODELS.Applications.objects.filter(id=server_id).first()
            version_data = REST_MODELS.WebConfigLogs.objects.filter(app_id=server_id).order_by("-id")
            if version_data:
                response.version_id = version_data[0].id

        except Exception as e:
            print(Exception, e)
            response.status = False
            response.message = str(e)
        return response

    def load_tree_data(self, request, server_id):
        response = BaseResponse()
        try:
            post_dict = QueryDict(request.body, encoding='utf-8')
            server_id = post_dict.get('server_id')
            version = post_dict.get('version')

            select_name = post_dict.get('n')
            select_level = post_dict.get('lv')
            select_id = post_dict.get('id')

            file_handler = FileHandler.Manager(server_id, 'nginx', version, select_id)
            ret = file_handler.get_items()

            response.data = ret
            response.message = '获取成功'
        except Exception as e:
            print(Exception, e)
            response.status = False
            response.message = str(e)

        return response

    def load_version_data(request, server_id):
        response = BaseResponse()
        try:
            file_handler = FileHandler.Manager(server_id, 'nginx')
            ret = file_handler.get_items()

            response.data = ret
            response.message = '获取成功'
        except Exception as e:
            print(Exception, e)
            response.status = False
            response.message = str(e)
        return response

    def create_last_version(request, server_id):
        response = BaseResponse()

        file_handler = FileHandler.Manager(server_id, 'nginx')
        response.status = file_handler.create_items('last_version', '', 'dir')
        return response

    def set_last_version(request, server_id):
        response = BaseResponse()
        post_dict = QueryDict(request.body, encoding='utf-8')
        version = post_dict.get('version')
        file_handler = FileHandler.Manager(server_id, 'nginx', version)
        file_handler.set_to_last_version()
        return response

    def get_file(request, server_id):
        response = BaseResponse()
        try:
            get_dict = request.GET
            version = get_dict.get('version')
            select_id = get_dict.get('select_id')
            file_handler = FileHandler.Manager(server_id, 'nginx', version, select_id)
            file_data = file_handler.get_file()
            response.data = file_data
        except Exception as e:
            print(Exception, e)
            response.status = False
            response.message = str(e)
        return response

    def create_file(request, server_id):
        response = BaseResponse()
        try:
            post_dict = QueryDict(request.body, encoding='utf-8')
            obj_name = post_dict.get('create_object_name')
            obj_type = post_dict.get('create_object_type')
            obj_path = post_dict.get('create_object_path')
            version = post_dict.get('version')
            file_handler = FileHandler.Manager(server_id, 'nginx', version)
            exec_status = file_handler.create_items(obj_name, obj_path, obj_type)
        except Exception as e:
            response.status = False
            response.message = str(e)
        return response

    def delete_file(request, server_id):
        response = BaseResponse()

        post_dict = QueryDict(request.body, encoding='utf-8')
        delete_object_path = post_dict.get('delete_object_path')
        version = post_dict.get('version')

        file_handler = FileHandler.Manager(server_id, 'nginx', version)
        exec_status = file_handler.delete_items(delete_object_path)

        response.status = exec_status['status']
        response.message = exec_status['msg']
        return response

    def edit_file(request, server_id):
        response = BaseResponse()

        post_dict = QueryDict(request.body, encoding='utf-8')
        edit_object_path = post_dict.get('edit_object_path')
        version = post_dict.get('version')
        edit_data = post_dict.get('edit_data')

        file_handler = FileHandler.Manager(server_id, 'nginx', version)
        exec_status = file_handler.edit_items(edit_object_path, edit_data)

        response.status = exec_status['status']
        response.message = exec_status['msg']
        return response

    def push_file(request, server_id):
        response = BaseResponse()
        current_version = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        try:
            post_dict = QueryDict(request.body, encoding='utf-8')
            push_group_id = post_dict.get('push_group_id')
            push_memo = post_dict.get('push_memo')
            __push_version = 'last_version'
            __push_target_path = settings.web_config_nginx_path
            get_asset_from_select_group = CMDB_MODELS.Asset.objects.filter(instances__id=push_group_id).values('server__ipaddress')
            asset_list = list(get_asset_from_select_group)

            # 创建日志记录
            app_obj = repository_models.Applications.objects.get(id=server_id)
            mission_obj = repository_models.WebConfigLogs(
                app_id=app_obj,
                version=current_version,
                user=request.user,
                memo=push_memo
            )
            mission_obj.save()

            # 创建ip状态数据
            asset_obj_list = [] # 包含任务详情数据，一起传递给任务执行模块
            for ip_obj in asset_list:
                instance_obj = repository_models.WebConfigInstance(
                    mission_id_id = mission_obj.id,
                    ip = ip_obj.get('server__ipaddress'),
                )
                instance_obj.save()
                asset_obj_list.append(instance_obj)

            file_handler = FileHandler.Manager(server_id, 'nginx', __push_version)
            exec_status = file_handler.push_version(__push_target_path, asset_obj_list)

            if exec_status['status']:
                # 发布完成后，将last_version拷贝至新的版本目录中
                file_handler.set_to_current_version(current_version)
                # 将version id 返回至前台，用于刷新右侧版本状态列表
                response.data = {'version_id': mission_obj.id, 'version_name': current_version}

        except Exception as e:
            print(Exception, e)
            response.status = False
            response.message = str(e)
        return response

    def get_version_status(request):
        response = BaseResponse()
        try:
            post_dict = QueryDict(request.body, encoding='utf-8')
            server_id = post_dict.get('server_id')
            version_id = post_dict.get('version_id')
            print(server_id)
            current_version_status = repository_models.WebConfigLogs.objects.get(id=version_id)
            all_version_from_server = repository_models.WebConfigLogs.objects.filter(app_id_id=server_id).order_by('-id')[:10]
            response.current_version_status = current_version_status
            response.all_version_from_server = all_version_from_server
        except Exception as e:
            print(Exception, e)
            response.status = False
            response.message = str(e)
        return response

    def get_version_tree(server_id):
        response = BaseResponse()
        try:
            server_obj = repository_models.WebConfigLogs.objects.filter(app_id=server_id).values('id', 'version').order_by("-id")[:10]
            response.data = list(server_obj)
        except Exception as e:
            print(Exception, e)
            response.status = False
            response.message = str(e)
        return response