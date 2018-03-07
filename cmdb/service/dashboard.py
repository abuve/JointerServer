#!/usr/bin/env python
# -*- coding:utf-8 -*-

from utils.response import BaseResponse
from django.http.request import QueryDict

from utils.base import BaseServiceList
from repository import models as REPOSITORY_MODELS
from cmdb import models as CMDB_MODELS


class DashBoard(BaseServiceList):
    def __init__(self):
        pass

    @staticmethod
    def get_basic_count():
        response = BaseResponse()
        try:
            basic_count = {
                'physical_count': CMDB_MODELS.Asset.objects.filter(device_type_id__in=[1,2]).count(),
                'cloud_count': CMDB_MODELS.Asset.objects.filter(device_type_id__in=[3]).count(),
                'docker_count': CMDB_MODELS.DockerInstance.objects.count(),
                'business_count': CMDB_MODELS.BusinessUnit.objects.count(),
                'project_count': REPOSITORY_MODELS.ProjectInfo.objects.count(),
                'application_count': REPOSITORY_MODELS.Applications.objects.count(),
            }
            response.basic_count = basic_count
        except Exception as e:
            print(Exception, e)
            response.status = False
            response.message = str(e)
        return response

    def get_assetAjax_count(self,):
        get_asset_type = CMDB_MODELS.Asset.device_type_choices
        asset_type_dict = {type_obj[1]: type_obj[0] for type_obj in get_asset_type}
        asset_type_list = list(map(lambda x: x[1], get_asset_type))
        asset_count_list = []
        for asset_type in asset_type_list:
            asset_count_list.append({'name': asset_type, 'value': CMDB_MODELS.Asset.objects.filter(device_type_id=asset_type_dict[asset_type]).count()})

        return {'name_list': asset_type_list, 'value_list': asset_count_list}

    def get_idcAjax_count(self,):
        get_idc_data = CMDB_MODELS.IDC.objects.values_list('name')
        idc_list = [idc_obj[0] for idc_obj in get_idc_data]
        idc_count_list = []
        for idc in idc_list:
            idc_count_list.append({'name': idc, 'value': CMDB_MODELS.Asset.objects.filter(idc__name=idc).count()})

        return {'name_list': idc_list, 'value_list': idc_count_list}

    def get_businessAjax_count(self,):
        get_asset_type = CMDB_MODELS.Asset.device_type_choices
        asset_type_dict = {type_obj[1]: type_obj[0] for type_obj in get_asset_type}
        asset_type_list = list(map(lambda x: x[1], get_asset_type))
        # 用于统计docker实例的个数
        asset_type_list.append('DockerInstance')
        get_business_name = CMDB_MODELS.BusinessUnit.objects.values_list('name')
        business_name_list = [business_obj[0] for business_obj in get_business_name]

        data_count_dic = []
        for asset_type in asset_type_list:
            asset_count_list = []
            for business_name in business_name_list:
                if asset_type == 'DockerInstance':
                    # 额外统计当前业务线包含的docker实例个数
                    dockerInstance_count = CMDB_MODELS.DockerInstance.objects.filter(
                        dockers__app_id__project_id__business_unit__name=business_name).count()
                    asset_count_list.append(dockerInstance_count)
                else:
                    asset_count = CMDB_MODELS.BusinessUnit.objects.filter(name=business_name,asset__device_type_id=asset_type_dict[asset_type]).count()
                    asset_count_list.append(asset_count)

            data_dic = {
                'name': asset_type,
                'type': 'bar',
                'stack': '统计',
                'label': {
                    'normal': {
                        'show': True,
                        'position': 'insideRight'
                    }
                },
                'data': asset_count_list
            }
            data_count_dic.append(data_dic)

        asset_type_list.append('DockerInstance')

        return {'business_list': business_name_list, 'asset_type_list': asset_type_list, 'data_count': data_count_dic}


    def get_chart_ajax(self):
        response = BaseResponse()
        try:

            asset_count = self.get_assetAjax_count()
            idc_count = self.get_idcAjax_count()
            business_count = self.get_businessAjax_count()

            response.asset_count = asset_count
            response.idc_count = idc_count
            response.business_count = business_count

        except Exception as e:
            print(Exception, e)
            response.status = False
            response.message = str(e)
        return response