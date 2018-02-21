# _*_coding:utf-8_*_

import json
import hashlib
from django.core.exceptions import ObjectDoesNotExist
from cmdb import models as CMDB_MODELS
from django.utils import timezone
from cmdb.service import asset_num


class Asset(object):
    def __init__(self, request):
        self.request = request
        request_client = get_client_ip(self.request)
        self.mandatory_fields = ['sn', 'asset_id', 'asset_type']  # must contains 'sn' , 'asset_id' and 'asset_type'
        self.field_sets = {
            'asset': ['manufactory'],
            'server': ['model', 'cpu_count', 'cpu_core_count', 'cpu_model', 'os_type', 'os_distribution', 'os_release'],
            'networkdevice': []
        }
        self.response = {
            'error': [],
            'info': [],
            'warning': []
        }

    def response_msg(self, msg_type, key, msg):
        if msg_type in self.response:
            self.response[msg_type].append({key: msg})
        else:
            raise ValueError

    def mandatory_check(self, data, check_from_asset=False, check_from_approval=False, only_check_filed=False):
        for field in self.mandatory_fields:
            if field not in data:
                self.response_msg('error', 'MandatoryCheckFailed',
                                  "The field [%s] is mandatory and not provided in your reporting data" % field)
                return False

        if only_check_filed:
            return True

        try:
            # 检查该资产是否包含有效sn 号，没有sn 的数据不予以处理
            if not data['sn']:
                self.response_msg('error', 'SN value error',
                                  "The field [sn] is mandatory and not provided in your reporting data")
                return False

            if check_from_asset:
                self.asset_obj = CMDB_MODELS.Asset.objects.get(sn=data['sn'])
            elif check_from_approval:
                self.asset_obj = CMDB_MODELS.NewAssetApprovalZone.objects.get(sn=data['sn'])
            else:
                self.asset_obj = CMDB_MODELS.Asset.objects.get(asset_num=data['asset_id'])
            return True

        except ObjectDoesNotExist as e:
            self.response_msg('error', 'AssetDataInvalid',
                              "Cannot find asset object in DB by using asset id [%s] and SN [%s] " % (
                              data['asset_id'], data['sn']))
            self.waiting_approval = True
            return False

    def get_asset_id_by_sn(self):
        '''When the client first time reports it's data to Server,it doesn't know it's asset id yet,so it will come to the server asks for the asset it first,then report the data again  '''
        data = self.request.POST.get("asset_data")
        response = {}
        if data:
            try:
                data = json.loads(data)
                # the asset is already exist in DB, just return it's asset id to client
                if self.mandatory_check(data, only_check_md5=True):
                    response = {
                        'needs_aproval': 'This asset has already report to server, Please waiting the admin confirm.'}
                else:
                    if hasattr(self, 'waiting_approval'):
                        response = {
                            'needs_aproval': "this is a new asset,needs IT admin's approval to create the new asset id."}
                        self.save_new_asset_to_approval_zone()
                        print(response)
                    else:
                        response = self.response
            except ValueError as e:
                self.response_msg('error', 'AssetDataInvalid', str(e))
                response = self.response
        else:
            self.response_msg('error', 'AssetDataInvalid', "The reported asset data is not valid or provided")
            response = self.response

        return response

    def check_asset_from_approval_zone(self):
        data = self.request.POST.get("asset_data")
        if data:
            try:
                data = json.loads(data)

                # 暂时不开放sn检测，因为sn不唯一，容易造成数据错乱，如果资产已经存在，手动关联资产编号
                if self.mandatory_check(data, check_from_asset=True):
                    return {"asset_id": self.asset_obj.asset_num}
                if self.mandatory_check(data, check_from_approval=True):
                    if self.asset_obj.asset_resume_num:
                        # 如果资产SN 发生变化，手动重置这个字段
                        return {"asset_id": self.asset_obj.asset_resume_num}
                    else:
                        # the asset is already exist in aporoval zone, waiting administrator to confirm.
                        response = {
                            'needs_aproval': 'This asset has already report to server, Please waiting the admin confirm.'}
                else:
                    if hasattr(self, 'waiting_approval'):
                        response = {
                            'needs_aproval': "this is a new asset,needs IT admin's approval to create the new asset id."}
                        self.clean_data = data
                        self.save_new_asset_to_approval_zone()
                    else:
                        response = self.response
            except ValueError as e:
                self.response_msg('error', 'AssetDataInvalid', str(e))
                response = self.response
        else:
            self.response_msg('error', 'AssetDataInvalid', "The reported asset data is not valid or provided")
            response = self.response
        return response

    def get_available_ip_from_nic(self):
        exclude_list = [None, '', '127.0.0.1']
        for nic_object in self.clean_data.get('nic'):
            if nic_object.get('ipaddress') not in exclude_list:
                return nic_object.get('ipaddress')

        return None

    def create_new_asset_md5(self):
        # Use asset sn and nic list create unique md5. Avoid duplicate data to add

        md5_str = self.clean_data.get('sn')
        for nic_obj in self.clean_data.get('nic'):
            md5_str += nic_obj.get('macaddress') + str(nic_obj.get('ipaddress'))
        md5_component = hashlib.md5()
        md5_component.update(md5_str.encode('utf-8'))
        asset_md5 = md5_component.hexdigest()
        return asset_md5

    def save_new_asset_to_approval_zone(self):
        '''When find out it is a new asset, will save the data into approval zone to waiting for IT admin's approvals'''
        asset_sn = self.clean_data.get('sn')
        asset_already_in_approval_zone = CMDB_MODELS.NewAssetApprovalZone.objects.get_or_create(
            ipaddress=self.clean_data.get('ipaddress'),
            sn=asset_sn,
            data=json.dumps(self.clean_data),
            manufactory=self.clean_data.get('manufactory'),
            model=self.clean_data.get('model'),
            ram_size=self.clean_data.get('ram_size'),
            cpu_model=self.clean_data.get('cpu_model'),
            cpu_count=self.clean_data.get('cpu_count'),
            cpu_core_count=self.clean_data.get('cpu_core_count'),
            os_release=self.clean_data.get('os_release'),
            os_type=self.clean_data.get('os_type'),
            )
        return True

    def data_is_valid(self):
        data = self.request.POST.get("asset_data")
        if data:
            try:
                data = json.loads(data)
                self.mandatory_check(data)
                self.clean_data = data
                if not self.response['error']:
                    return True
            except ValueError as e:
                self.response_msg('error', 'AssetDataInvalid', str(e))
        else:
            self.response_msg('error', 'AssetDataInvalid', "The reported asset data is not valid or provided")

    def __is_new_asset(self):
        if not hasattr(self.asset_obj, self.clean_data['asset_type']):  # new asset
            return True
        else:
            return False

    def data_inject(self):
        '''save data into DB,the data_is_valid() must returns True before call this function'''
        if self.__is_new_asset():
            print('\033[32;1m---new asset,going to create----\033[0m')
            self.create_asset()
        else:  # asset already already exist , just update it
            print('\033[33;1m---asset already exist ,going to update----\033[0m')

            self.update_asset()

    def data_is_valid_without_id(self):
        '''when there's no asset id in reporting data ,goes through this function fisrt'''
        data = self.request.POST.get("asset_data")
        if data:
            try:
                # push asset id into reporting data before doing the mandatory check
                if self.mandatory_check(data, only_check_filed=True):
                    self.asset_obj = CMDB_MODELS.Asset.objects.create(sn=data['sn'])
                else:
                    return False

                if self.asset_obj.asset_num:
                    return False
                else:
                    new_asset_num = asset_num.asset_num_builder()
                    self.asset_obj.asset_num = new_asset_num
                    self.asset_obj.save()
                    self.clean_data = data

                if not self.response['error']:
                    return True
            except ValueError as e:
                print(ValueError, e)
                self.response_msg('error', 'AssetDataInvalid', str(e))
        else:
            self.response_msg('error', 'AssetDataInvalid', "The reported asset data is not valid or provided")

    def reformat_components(self, identify_field, data_set):
        '''This function is used as workround for some components's data structor is big dict ,yet
        the standard structor is list,e.g:
        standard: [{
            "slot": "1I:1:1",
            "capacity": 300,
            "sn": "",
            "model": "",
            "enclosure": "0",
            "iface_type": "SAS"
        },
        {
            "slot": "1I:1:2",
            "capacity": 300,
            "sn": "",
            "model": "",
            "enclosure": "0",
            "iface_type": "SAS"
        }]
        but for some components such as ram:
        {"PROC 2 DIMM 1": {
            "model": "<OUT OF SPEC>",
            "capacity": 0,
            "sn": "Not Specified",
            "manufactory": "UNKNOWN"
        },}

        it uses key as identified field, the key is actually equals slot field in db model field, this unstandard
        data source should be dprecated in the future, now I will just reformat it as workround
        '''
        for k, data in data_set.items():
            data[identify_field] = k

    def __verify_field(self, data_set, field_key, data_type, required=True):
        field_val = data_set.get(field_key)
        if field_val:
            try:
                data_set[field_key] = data_type(field_val)
            except ValueError as e:
                self.response_msg('error', 'InvalidField',
                                  "The field [%s]'s data type is invalid, the correct data type should be [%s] " % (
                                  field_key, data_type))

        elif required == True:
            pass
            # self.response_msg('error','LackOfField', "The field [%s] has no value provided in your reporting data [%s]" % (field_key,data_set) )

    def create_asset(self):
        '''
        invoke asset create function according to it's asset type
        :return:
        '''
        func = getattr(self, '_create_%s' % self.clean_data['asset_type'])
        create_obj = func()

    def update_asset(self):
        func = getattr(self, '_update_%s' % self.clean_data['asset_type'])
        create_obj = func()

    def _update_server(self):
        # nic = self.__update_asset_component(data_source=self.clean_data['nic'],
        #                                     fk='nic_set',
        #                                     update_fields = ['name','sn','model','macaddress','ipaddress','netmask','bonding'],
        #                                     identify_field = 'macaddress'
        #                                     )
        disk = self.__update_asset_component(data_source=self.clean_data['physical_disk_driver'],
                                             fk='disk_set',
                                             update_fields=['slot', 'sn', 'model', 'manufactory', 'capacity',
                                                            'iface_type'],
                                             identify_field='slot'
                                             )
        ram = self.__update_asset_component(data_source=self.clean_data['ram'],
                                            fk='ram_set',
                                            update_fields=['slot', 'sn', 'model', 'capacity'],
                                            identify_field='slot'
                                            )
        # cpu = self.__update_cpu_component()
        # manufactory = self.__update_manufactory_component()

        server = self.__update_server_component()

        # self.__update_client_version()

    def _create_server(self):
        self.__create_server_info()
        # self.__create_or_update_manufactory()
        # self.__create_cpu_component()
        self.__create_disk_component()
        # self.__create_nic_component()
        self.__create_ram_component()
        # self.__check_idc_component()

        log_msg = "Asset [<a href='/admin/assets/asset/%s/' target='_blank'>%s</a>] has been created!" % (
        self.asset_obj.id, self.asset_obj)
        self.response_msg('info', 'NewAssetOnline', log_msg)

    def __check_idc_component(self):
        obj_ip = self.get_available_ip_from_nic()
        idc_name = idc_check_handler(obj_ip)
        if idc_name:
            idc_obj = CMDB_MODELS.IDC.objects.get(name=idc_name)
            self.asset_obj.idc = idc_obj
            self.asset_obj.save()

    def __create_server_info(self, ignore_errs=False):
        try:
            self.__verify_field(self.clean_data, 'model', str)
            # no processing when there's no error happend
            if not len(self.response['error']) or ignore_errs == True:
                data_set = {
                    'asset_id': self.asset_obj.id,
                    'hostname': self.clean_data.get('hostname'),
                    'model': self.clean_data.get('model'),
                    'Memory': self.clean_data.get('Memory'),
                    'DeviceSize': self.clean_data.get('DeviceSize'),
                    'CpuUsage': self.clean_data.get('CpuUsage'),
                    'MemUsage': self.clean_data.get('MemUsage'),
                    'DiskUsage': self.clean_data.get('DiskUsage'),
                    'LoadInfo': self.clean_data.get('LoadInfo'),
                    'configuration': self.clean_data.get('configuration'),
                    'os_type': self.clean_data.get('os_type'),
                    'os_release': self.clean_data.get('os_release'),
                    'ipaddress': self.clean_data.get('ipaddress'),
                }

                obj = CMDB_MODELS.Server(**data_set)
                obj.save()
                self.obj = obj
                return obj
        except Exception as e:
            print('error', 'ObjectCreationException', 'Object [server] %s' % str(e))
            self.response_msg('error', 'ObjectCreationException', 'Object [server] %s' % str(e))

    def __create_or_update_manufactory(self, ignore_errs=False):
        try:
            self.__verify_field(self.clean_data, 'manufactory', str)
            manufactory = self.clean_data.get('manufactory')
            # no processing when there's no error happend
            if not len(self.response['error']) or ignore_errs == True:
                obj_exist = CMDB_MODELS.Manufactory.objects.filter(manufactory=manufactory)
                if obj_exist:
                    obj = obj_exist[0]
                else:  # create a new one
                    obj = CMDB_MODELS.Manufactory(manufactory=manufactory)
                    obj.save()
                self.asset_obj.manufactory = obj
                self.asset_obj.save()
        except Exception as e:
            self.response_msg('error', 'ObjectCreationException', 'Object [manufactory] %s' % str(e))

    def __create_cpu_component(self, ignore_errs=False):
        try:
            self.__verify_field(self.clean_data, 'model', str)
            self.__verify_field(self.clean_data, 'cpu_count', int)
            self.__verify_field(self.clean_data, 'cpu_core_count', int)
            # no processing when there's no error happend
            if not len(self.response['error']) or ignore_errs == True:
                data_set = {
                    'asset_id': self.asset_obj.id,
                    'cpu_model': self.clean_data.get('cpu_model'),
                    'cpu_count': self.clean_data.get('cpu_count'),
                    'cpu_core_count': self.clean_data.get('cpu_core_count'),
                }

                obj = CMDB_MODELS.CPU(**data_set)
                obj.save()
                log_msg = "Asset[%s] --> has added new [cpu] component with data [%s]" % (self.asset_obj, data_set)
                self.response_msg('info', 'NewComponentAdded', log_msg)
                return obj
        except Exception as e:
            pass
            # self.response_msg('error','ObjectCreationException','Object [cpu] %s' % str(e) )

    def __create_disk_component(self):
        disk_info = self.clean_data.get('physical_disk_driver')
        if disk_info:
            for disk_item in disk_info:
                try:
                    self.__verify_field(disk_item, 'slot', str, required=False)
                    self.__verify_field(disk_item, 'capacity', float, required=False)
                    self.__verify_field(disk_item, 'iface_type', str, required=False)
                    self.__verify_field(disk_item, 'model', str, required=False)
                    # no processing when there's no error happend
                    if not len(self.response['error']):
                        data_set = {
                            'asset_id': self.asset_obj.id,
                            'sn': disk_item.get('sn'),
                            'slot': disk_item.get('slot'),
                            'capacity': disk_item.get('capacity'),
                            'model': disk_item.get('model'),
                            'iface_type': disk_item.get('iface_type'),
                            'manufactory': disk_item.get('manufactory'),
                        }

                        obj = CMDB_MODELS.Disk(**data_set)
                        obj.save()

                except Exception as e:
                    print(Exception, e)
                    self.response_msg('error', 'ObjectCreationException', 'Object [disk] %s' % str(e))
        else:
            # self.response_msg('error','LackOfData','Disk info is not provied in your reporting data' )
            pass

    def __create_nic_component(self):
        nic_info = self.clean_data.get('nic')
        if nic_info:
            for nic_item in nic_info:
                try:
                    self.__verify_field(nic_item, 'macaddress', str)
                    # no processing when there's no error happend
                    print(self.response['error'])
                    if not len(self.response['error']):
                        data_set = {
                            'asset_id': self.asset_obj.id,
                            'name': nic_item.get('name'),
                            'sn': nic_item.get('sn'),
                            'macaddress': nic_item.get('macaddress'),
                            'ipaddress': nic_item.get('ipaddress'),
                            'bonding': nic_item.get('bonding'),
                            'model': nic_item.get('model'),
                            'netmask': nic_item.get('netmask'),
                        }

                        obj = CMDB_MODELS.NIC(**data_set)
                        obj.save()

                except Exception as e:
                    print(Exception, e)
                    self.response_msg('error', 'ObjectCreationException', 'Object [nic] %s' % str(e))
        else:
            self.response_msg('error', 'LackOfData', 'NIC info is not provied in your reporting data')

    def __create_ram_component(self):
        ram_info = self.clean_data.get('ram')
        if ram_info:
            for ram_item in ram_info:
                try:
                    self.__verify_field(ram_item, 'capacity', int, required=False)
                    # no processing when there's no error happend
                    if not len(self.response['error']):
                        data_set = {
                            'asset_id': self.asset_obj.id,
                            'slot': ram_item.get("slot"),
                            'sn': ram_item.get('sn'),
                            'capacity': ram_item.get('capacity'),
                            'model': ram_item.get('model'),
                        }

                        obj = CMDB_MODELS.RAM(**data_set)
                        obj.save()

                except Exception as e:
                    print(Exception, e)
                    self.response_msg('error', 'ObjectCreationException', 'Object [ram] %s' % str(e))
        else:
            # self.response_msg('error','LackOfData','RAM info is not provied in your reporting data' )
            pass

    def __update_server_component(self):
        update_fields = ['model', 'os_type', 'os_release', 'hostname', 'CpuUsage', 'MemUsage', 'DiskUsage',
                         'configuration', 'Memory', 'DeviceSize', 'LoadInfo', 'ipaddress', 'cpu_count', 'cpu_model', 'cpu_core_count']
        if hasattr(self.asset_obj, 'server'):
            self.__compare_componet(model_obj=self.asset_obj.server,
                                    fields_from_db=update_fields,
                                    data_source=self.clean_data)
        else:
            self.__create_server_info(ignore_errs=True)

    def __update_manufactory_component(self):
        self.__create_or_update_manufactory(ignore_errs=True)

    def __update_client_version(self):
        update_fields = ['client_version']
        self.__compare_componet(model_obj=self.asset_obj,
                                fields_from_db=update_fields,
                                data_source=self.clean_data)

    def __update_cpu_component(self):
        update_fields = ['cpu_model', 'cpu_count', 'cpu_core_count']
        if hasattr(self.asset_obj, 'cpu'):
            self.__compare_componet(model_obj=self.asset_obj.cpu,
                                    fields_from_db=update_fields,
                                    data_source=self.clean_data)
        else:
            self.__create_cpu_component(ignore_errs=True)

    def __update_asset_component(self, data_source, fk, update_fields, identify_field=None):
        '''
        data_source: the data source of this component from reporting data
        fk: which key to use to find the connection between main Asset obj and each asset component
        update_fields: what fields in DB will be compared and updated
        identify_field: use this field to identify each component of an Asset , if set to None, means only use asset id to identify
         '''
        try:
            component_obj = getattr(self.asset_obj, fk)
            if hasattr(component_obj, 'select_related'):  # this component is reverse m2m relation with Asset model
                objects_from_db = component_obj.select_related()
                for obj in objects_from_db:
                    # use this key_field_data to find the relative data source from reporting data
                    key_field_data = getattr(obj, identify_field)
                    if type(data_source) is list:
                        for source_data_item in data_source:
                            key_field_data_from_source_data = source_data_item.get(identify_field)
                            if key_field_data_from_source_data:
                                if key_field_data == key_field_data_from_source_data:  # find the matched source data for this component,then should compare each field in this component to see if there's any changes since last update
                                    self.__compare_componet(model_obj=obj, fields_from_db=update_fields,
                                                            data_source=source_data_item)
                                    break  # must break ast last ,then if the loop is finished , logic will goes for ..else part,then you will know that no source data is matched for by using this key_field_data, that means , this item is lacked from source data, it makes sense when the hardware info got changed. e.g: one of the RAM is broken, sb takes it away,then this data will not be reported in reporting data
                            else:  # key field data from source data cannot be none
                                self.response_msg('warning', 'AssetUpdateWarning',
                                                  "Asset component [%s]'s key field [%s] is not provided in reporting data " % (
                                                  fk, identify_field))
                        else:  # couldn't find any matches, the asset component must be broken or changed manually
                            print(
                                '\033[33;1mError:cannot find any matches in source data by using key field val [%s],component data is missing in reporting data!\033[0m' % (
                                key_field_data))
                            self.response_msg("error", "AssetUpdateWarning",
                                              "Cannot find any matches in source data by using key field val [%s],component data is missing in reporting data!" % (
                                              key_field_data))
                    elif type(data_source) is dict:
                        for key, source_data_item in data_source.items():
                            key_field_data_from_source_data = source_data_item.get(identify_field)
                            if key_field_data_from_source_data:
                                if key_field_data == key_field_data_from_source_data:  # find the matched source data for this component,then should compare each field in this component to see if there's any changes since last update
                                    self.__compare_componet(model_obj=obj, fields_from_db=update_fields,
                                                            data_source=source_data_item)
                                    break  # must break ast last ,then if the loop is finished , logic will goes for ..else part,then you will know that no source data is matched for by using this key_field_data, that means , this item is lacked from source data, it makes sense when the hardware info got changed. e.g: one of the RAM is broken, sb takes it away,then this data will not be reported in reporting data
                            else:  # key field data from source data cannot be none
                                self.response_msg('warning', 'AssetUpdateWarning',
                                                  "Asset component [%s]'s key field [%s] is not provided in reporting data " % (
                                                  fk, identify_field))

                        else:  # couldn't find any matches, the asset component must be broken or changed manually
                            print(
                                '\033[33;1mWarning:cannot find any matches in source data by using key field val [%s],component data is missing in reporting data!\033[0m' % (
                                key_field_data))
                    else:
                        print('\033[31;1mMust be sth wrong,logic should goes to here at all.\033[0m')
                # compare all the components from DB with the data source from reporting data
                self.__filter_add_or_deleted_components(model_obj_name=component_obj.model._meta.object_name,
                                                        data_from_db=objects_from_db, data_source=data_source,
                                                        identify_field=identify_field)

            else:  # this component is reverse fk relation with Asset model
                pass
        except ValueError as e:
            print('\033[41;1m%s\033[0m' % str(e))

    def __filter_add_or_deleted_components(self, model_obj_name, data_from_db, data_source, identify_field):
        '''This function is filter out all  component data in db but missing in reporting data, and all the data in reporting data but not in DB'''
        print(data_from_db, data_source, identify_field)
        data_source_key_list = []  # save all the idenified keys from client data,e.g: [macaddress1,macaddress2]
        if type(data_source) is list:
            for data in data_source:
                data_source_key_list.append(data.get(identify_field))
        elif type(data_source) is dict:
            for key, data in data_source.items():
                if data.get(identify_field):
                    data_source_key_list.append(data.get(identify_field))
                else:  # workround for some component uses key as identified field e.g: ram
                    data_source_key_list.append(key)
        print('-->identify field [%s] from db  :', data_source_key_list)
        print('-->identify[%s] from data source:', [getattr(obj, identify_field) for obj in data_from_db])

        data_source_key_list = set(data_source_key_list)
        data_identify_val_from_db = set([getattr(obj, identify_field) for obj in data_from_db])
        data_only_in_db = data_identify_val_from_db - data_source_key_list  # delete all this from db
        data_only_in_data_source = data_source_key_list - data_identify_val_from_db  # add into db
        print('\033[31;1mdata_only_in_db:\033[0m', data_only_in_db)
        print('\033[31;1mdata_only_in_data source:\033[0m', data_only_in_data_source)
        self.__delete_components(all_components=data_from_db, delete_list=data_only_in_db,
                                 identify_field=identify_field)
        if data_only_in_data_source:
            self.__add_components(model_obj_name=model_obj_name, all_components=data_source,
                                  add_list=data_only_in_data_source, identify_field=identify_field)

    def __add_components(self, model_obj_name, all_components, add_list, identify_field):
        model_class = getattr(CMDB_MODELS, model_obj_name)
        will_be_creating_list = []
        print('--add component list:', add_list)
        if type(all_components) is list:
            for data in all_components:
                if data[identify_field] in add_list:
                    # print data
                    will_be_creating_list.append(data)
        elif type(all_components) is dict:
            for k, data in all_components.items():
                # workround for some components uses key as identified field ,e.g ram
                if data.get(identify_field):
                    if data[identify_field] in add_list:
                        # print k,data
                        will_be_creating_list.append(data)
                else:  # if the identified field cannot be found from data set,then try to compare the dict key
                    if k in add_list:
                        data[
                            identify_field] = k  # add this key into dict , because this dict will be used to create new component item in DB
                        will_be_creating_list.append(data)

        # creating components
        try:
            for component in will_be_creating_list:
                data_set = {}
                for field in model_class.auto_create_fields:
                    data_set[field] = component.get(field)
                data_set['asset_id'] = self.asset_obj.id
                obj = model_class(**data_set)
                obj.save()
                print('\033[32;1mCreated component with data:\033[0m', data_set)
                log_msg = "Asset[%s] --> component[%s] has justed added a new item [%s]" % (
                self.asset_obj, model_obj_name, data_set)
                self.response_msg('info', 'NewComponentAdded', log_msg)
                log_handler(self.asset_obj, 'NewComponentAdded', self.request.user, log_msg, model_obj_name)

        except Exception as e:
            print("\033[31;1m %s \033[0m" % e)
            log_msg = "Asset[%s] --> component[%s] has error: %s" % (self.asset_obj, model_obj_name, str(e))
            self.response_msg('error', "AddingComponentException", log_msg)

    def __delete_components(self, all_components, delete_list, identify_field):
        '''All the objects in delete list will be deleted from DB'''
        deleting_obj_list = []
        print('--deleting components', delete_list, identify_field)
        for obj in all_components:
            val = getattr(obj, identify_field)
            if val in delete_list:
                deleting_obj_list.append(obj)

        for i in deleting_obj_list:
            log_msg = "Asset[%s] --> component[%s] --> is lacking from reporting source data, assume it has been removed or replaced,will also delete it from DB" % (
            self.asset_obj, i)
            self.response_msg('info', 'HardwareChanges', log_msg)
            log_handler(self.asset_obj, 'HardwareChanges', self.request.user, log_msg, i)
            i.delete()

    def __compare_componet(self, model_obj, fields_from_db, data_source):
        print('---going to compare:[%s]' % model_obj, fields_from_db)
        print('---source data:', data_source)
        for field in fields_from_db:
            val_from_db = getattr(model_obj, field)
            val_from_data_source = data_source.get(field)
            if val_from_data_source:
                print(val_from_data_source)
                # if type(val_from_db) is unicode:val_from_data_source = unicode(val_from_data_source)#no unicode in py3
                # if type(val_from_db) in (int,long):val_from_data_source = int(val_from_data_source) #no long in py3
                if type(val_from_db) in (int,):
                    val_from_data_source = int(val_from_data_source)
                elif type(val_from_db) is float:
                    val_from_data_source = float(val_from_data_source)
                elif type(val_from_db) is str:
                    val_from_data_source = str(val_from_data_source).strip()
                if val_from_db == val_from_data_source:  # this field haven't changed since last update
                    pass
                    print('\033[32;1m val_from_db[%s]  == val_from_data_source[%s]\033[0m' % (
                    val_from_db, val_from_data_source))
                else:
                    print('\033[34;1m val_from_db[%s]  != val_from_data_source[%s]\033[0m' % (
                    val_from_db, val_from_data_source), type(val_from_db), type(val_from_data_source), field)
                    db_field = model_obj._meta.get_field(field)
                    db_field.save_form_data(model_obj, val_from_data_source)
                    model_obj.update_date = timezone.now()
                    model_obj.save()
                    log_msg = "Asset[%s] --> component[%s] --> field[%s] has changed from [%s] to [%s]" % (
                    self.asset_obj, model_obj, field, val_from_db, val_from_data_source)
                    self.response_msg('info', 'FieldChanged', log_msg)
                    log_handler(self.asset_obj, 'FieldChanged', self.request.user, log_msg, model_obj)
            else:
                self.response_msg('warning', 'AssetUpdateWarning',
                                  "Asset component [%s]'s field [%s] is not provided in reporting data " % (
                                  model_obj, field))

        model_obj.save()


def log_handler(asset_obj, event_name, user, detail, component=None):
    ''' (1, u'硬件变更'),
        (2, u'新增配件'),
        (3, u'设备下线'),
        (4, u'设备上线'),
        (5, u'定期维护'),
        (6, u'资源发现'),'''

    '''log_catelog = {
        1: ['FieldChanged', 'HardwareChanges'],
        2: ['NewComponentAdded'],
        3: ['AssetOffLine'],
        4: ['AssetOnLine'],
        5: ['ScheduledMaintenance'],
        6: ['AssetScanFound'],
    }
    if not user:
        #user = models.UserProfile.objects.filter(is_admin=True).last()
        user = 'Aaron'

    event_type = None
    for k,v in log_catelog.items():
        if event_name in v:
            event_type = k
            break

    log_obj = CMDB_MODELS.EventLog(
        name =event_name,
        event_type = event_type,
        asset_id = asset_obj.id,
        component = component,
        detail = detail,
        options = user
    )

    log_obj.save()'''
    pass


def idc_check_handler(ipaddress):
    valid_idc_to_network = {'TechZone': '192.168.10',
                            'HongKong': '10.167.11',
                            'GDC': '10.168.11'}

    for idc, network in valid_idc_to_network.items():
        if network in ipaddress:
            return idc

    return None


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
