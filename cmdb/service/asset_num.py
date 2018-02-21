__author__ = 'Aaron'

import string
import random
import django

from cmdb import models as cmdb_models


def check_asset_num(new_asset):
    try:
        cmdb_models.Asset.objects.get(asset_num=new_asset)
        return True
    except:
        return False


def asset_num_builder():
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    while True:
        get_new_asset = ''.join(random.sample((letters + string.digits), 8))
        if check_asset_num(get_new_asset):
            continue
        else:
            return get_new_asset