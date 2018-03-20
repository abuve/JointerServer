#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from django.views import View
from django.shortcuts import render
from django.shortcuts import HttpResponse, HttpResponseRedirect
from utils.mixin_utils import LoginRequiredMixin, PermissionRequiredMixin, WriteAccessLogsMixin
from django.http import JsonResponse

from cmdb.service import server
from cmdb import models as CMDB_MODELS


class ServerListView(WriteAccessLogsMixin, LoginRequiredMixin, PermissionRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'cmdb_server_list.html')


class ServerJsonView(WriteAccessLogsMixin, LoginRequiredMixin, PermissionRequiredMixin, View):
    def post(self, request):
        response = server.Server.asset_data_create(request)
        return JsonResponse(response.__dict__)

    def get(self, request):
        # obj = server.Server()
        response = server.Server().fetch_assets(request)
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = server.Server.delete_data(request)
        return JsonResponse(response.__dict__)

    def put(self, request):
        response = server.Server.put_assets(request)
        return JsonResponse(response.__dict__)


class AssetDetailView(WriteAccessLogsMixin, LoginRequiredMixin, PermissionRequiredMixin, View):
    def get(self, request, asset_nid):
        response = server.Server.assets_detail(asset_nid)
        return render(request, 'cmdb_asset_detail.html', {"response": response})


class AssetCreateView(WriteAccessLogsMixin, LoginRequiredMixin, PermissionRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        response = server.Server().asset_create()
        return render(request, 'cmdb_asset_create.html', {'response': response})


# def test(request):
#
#     from cmdb.service import asset_num
#
#     server_data = CMDB_MODELS.Server.objects.all()
#     for obj in server_data:
#         old_ip = obj.ipaddress.split('.')
#         new_ip = '%s.%s.28.%s' % (old_ip[0], old_ip[1], old_ip[3])
#
#         obj.hostname = 'PRODUCTION-WEB-%s' % old_ip[3]
#         obj.ipaddress = new_ip
#         obj.asset.sn = asset_num.asset_num_builder()
#         obj.configuration = '16C / 64GB / 2480GB'
#         obj.asset.memo = '生产服务器'
#         obj.manage_ip = '%s.10.28.%s' % (old_ip[0], old_ip[3])
#         obj.cpu_count = 2
#         obj.cpu_core_count = 8
#         obj.cpu_model = 'Intel(R) Xeon(R) CPU E5640 @ 2.67GHz'
#         obj.os_release = 'CentOS Linux release 7.2.1511 (Core)'
#
#         obj.save()
#         obj.asset.save()
#
#     return HttpResponse(1)
#
#
# def rsync_old_data(request):
#     def request_post(page):
#         from urllib import parse, request
#         import json
#         textmod = {"option": "querybytype", "token": "NEBB5oMQOPMpLTn6PneJKBDEMU0WeBxd", "parameters": {"data": ["Physics", "DockerPhysics", "XenPhysics", "OpenVZPhysics", "CloudServer"], "page": page, "limit": 10}}
#         # json串数据使用
#         textmod = json.dumps(textmod).encode(encoding='utf-8')
#         header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
#                        "Content-Type": "application/json"}
#         url = 'http://cmdb.omtools.me/cmdb/api/'
#         req = request.Request(url=url, data=textmod, headers=header_dict)
#         res = request.urlopen(req)
#         res = res.read()
#         data = json.loads(res.decode(encoding='utf-8'))
#         return data
#
#     type_map = {
#         'Physics': 1,
#         'DockerPhysics': 2,
#         'XenPhysics': 1,
#         'OpenVZPhysics': 1,
#         'CloudServer': 3
#     }
#
#     for page in range(1, 10):
#         get_data_from_api = request_post(page)
#         if not get_data_from_api['data']:
#             break
#         else:
#             asset_data = get_data_from_api['data']
#             for obj in asset_data:
#                 print(obj)
#                 try:
#                     # 创建asset obj
#                     asset_obj = CMDB_MODELS.Asset(
#                         device_type_id=type_map[obj.get('asset_type')],
#                         asset_num=obj.get('asset_id'),
#                         sn=obj['sn'],
#                     )
#                     asset_obj.save()
#
#                     # 创建server obj
#                     server_obj = CMDB_MODELS.Server(
#                         asset_id=asset_obj.id,
#                         hostname=obj.get('hostname'),
#                         ipaddress=obj.get('ip'),
#                         configuration=obj.get('configuration'),
#                         manage_ip=obj.get('manage_ip'),
#                     )
#                     server_obj.save()
#                 except Exception as e:
#                     print(Exception, e)
#
#     return HttpResponse(1)
#
# def upload_cloud_server(request):
#     from cmdb.service import asset_num
#     f = open('./ips.txt', 'r')
#     data = f.readlines()
#     f.close()
#     cloud_filter = CMDB_MODELS.Asset.objects.filter(device_type_id=3)
#     cloud_filter.delete()
#     for line in data:
#         obj = line.split('\t')
#         try:
#             # 创建asset obj
#             asset_obj = CMDB_MODELS.Asset(
#                 device_type_id=3,
#                 idc=CMDB_MODELS.IDC.objects.get(name=obj[1]),
#                 asset_num=asset_num.asset_num_builder(),
#                 memo=obj[8],
#                 create_date=obj[6]
#             )
#             asset_obj.save()
#
#             # 创建server obj
#             server_obj = CMDB_MODELS.Server(
#                 asset_id=asset_obj.id,
#                 ipaddress=obj[0],
#                 configuration=obj[8],
#             )
#             server_obj.save()
#         except Exception as e:
#             print(obj[1])
#             print(Exception, e)
#     return HttpResponse(1)