#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, sys
import docker
import django
import platform
#from conf import settings

if platform.system() == 'Linux':
    sys.path.append('/app/project/JointerServer')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "JointerServer.settings")
django.setup()

from cmdb import models as CMDB_MODELS


class DockerHandler(object):
    def __init__(self):
        self.host_port = 2375

    def __docker_api_conn(self, host_ip):
        try:
            print(host_ip)
            client = docker.DockerClient(base_url='tcp://%s:%s' % (host_ip, self.host_port), version='1.24')
            return client
        except:
            return False

    def get_docker_hosts(self):
        filter_data = CMDB_MODELS.Asset.objects.filter(device_type_id=2, device_status_id=1)
        return filter_data

    def fetch_docker_container(self, host_ip):
        docker_set = self.__docker_api_conn(host_ip)
        return docker_set.containers.list()

    def set_container(self):
        list_from_db = list(self.host_obj.docker.values_list('name'))

        list_from_new = []
        for obj in self.contains_new_list:
            list_from_new.append((obj['name'], ))

        old_set = set(list_from_db)
        new_set = set(list_from_new)

        container_need_create = new_set - old_set
        container_need_delete = old_set - new_set

        return {"container_need_create": container_need_create, "container_need_delete": container_need_delete}

    def __container_create(self, container_list):
        for obj in container_list:
            try:
                obj['asset_id'] = self.host_obj.id
                print('---going to create %s' %obj)
                data_insert = CMDB_MODELS.DockerInstance(**obj)
                data_insert.save()
            except Exception as e:
                print(Exception, e)

    def __container_delete(self, container_list):
        if container_list:
            print('---going to delete %s' % container_list)
            data = CMDB_MODELS.DockerInstance.objects.filter(asset_id=self.host_obj.id, name__in=container_list)
            CMDB_MODELS.DockerInstance.objects.filter(asset_id=self.host_obj.id, name__in=container_list).delete()

    def __container_create_or_delete(self, contains_set):
        need_create = filter(lambda x: (x['name'], ) in contains_set['container_need_create'], self.contains_new_list)
        need_delete = map(lambda x: x[0], contains_set['container_need_delete'])

        self.__container_create(list(need_create))
        self.__container_delete(list(need_delete))

    def contains_handle(self, contains_list):
        self.contains_new_list = []
        for contains_obj in contains_list:
            obj_idc = {}
            obj_idc['obj_id'] = contains_obj.id[0:12]
            obj_idc['name'] = contains_obj.name

            attrs_json = contains_obj.attrs

            try:
                obj_idc['cpu'] = int(attrs_json['HostConfig']['CpuCount'] / 1000 / 1000 /1000)   # format to GB
            except:
                obj_idc['cpu'] = None

            try:
                obj_idc['mem'] = int(attrs_json['HostConfig']['Memory'] / 1000 / 1000 /1000)   # format to GB
            except:
                obj_idc['mem'] = None

            try:
                obj_idc['disk'] = int(int(attrs_json['GraphDriver']['Data']['DeviceSize'])  / 1000 / 1000 /1000)   # format to GB
            except:
                obj_idc['disk'] = None

            try:
                port_list = []
                port_map_list = []
                for container_port, host_port_list in attrs_json['HostConfig']['PortBindings'].items():
                    if host_port_list != None:
                        host_port = host_port_list[0]['HostPort']
                        port_list.append(host_port)
                    else:
                        host_port = None

                    port_map_list.append('%s ---> %s' % (container_port, host_port))

                obj_idc['port'] = ', '.join(port_list)
                obj_idc['port_map'] = ', '.join(port_map_list)
            except:
                obj_idc['port'] = None
                obj_idc['port_map'] = None

            # use for cpu memory usage.
            # stats_json = contains_obj.stats(stream=False)

            self.contains_new_list.append(obj_idc)

        self.__container_create_or_delete(self.set_container())


    def handle(self):
        host_list = self.get_docker_hosts()
        for host_obj in host_list:
            self.host_obj = host_obj
            self.contains_handle(self.fetch_docker_container(host_obj.server.ipaddress))


if __name__ == "__main__":
    docker_api = DockerHandler()
    docker_api.handle()
