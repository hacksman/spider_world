#!/usr/bin/env python 
# coding:utf-8
# @Time :10/6/18 16:31

import requests
from www_douyin_com.common.urls import URL

APPINFO = {
    "version_code": "290",
    "app_version": "2.9.0",
    "version_name": "2.9.0",
    "device_platform": "android",
    "ssmix": "a",
    "device_type": "ONEPLUS+A5000",
    "device_brand": "OnePlus",
    "language": "zh",
    "os_api": "28",
    "os_version": "9",
    "manifest_version_code": "290",
    "resolution": "1080*1920",
    "dpi": "420",
    "update_version_code": "2902",
    "_rticket": "1548672388498",
    "channel": "wandoujia_zhiwei",
    "app_name": "aweme",
    "build_number": "27014",
    "aid": "1128",
    "ac": "WIFI",
}

header = {
    "User-Agent": "Aweme/2.7.0 (iPhone; iOS 12.0; Scale/2.00)"
}


# 获取新的设备信息  有效期60分钟永久
def get_device(token):

    device_info = requests.get(URL.api_device(token), timeout=10)

    return device_info.json()

# 拼装参数
def params2str(params):
    query = ""
    for k, v in params.items():
        query += "%s=%s&" % (k, v)
    query = query.strip("&")
    # print("Sign str: " + query)
    return query

# 使用拼装参数签名
def gen_url(token, raw_url, query):
    if isinstance(query, dict):
        query = params2str(query)
    url = raw_url + "?" + query
    resp = requests.post(URL.api_sign(token), json={"url": url}).json()
    real_url = resp['url']
    return real_url

# 混淆手机号码和密码
def mixString(pwd):
    password = ""
    for i in range(len(pwd)):
        password += hex(ord(pwd[i]) ^ 5)[-2:]
    return password


def common_params(device_info):
    item = {
        "new_user":         str(device_info['new_user']),
        "device_id":        str(device_info['device_id']),
        "openudid":         str(device_info['openudid']),
        "iid":              str(device_info['install_id']),
        "android_id":       str(device_info['android_id']),
    }
    params = {**item, **APPINFO}
    return params


# check douyin id
# import re
# import functools
# def check_id(func):
#     @functools.wraps(func)
#     def wrapper(self, *args, **kwargs):
#         if not re.findall('^\d{10,13}$', args[0]):
#             self.logger.info("请输入正确的用户id， 用户id为10,11,12或13位纯数字...")
#             raise Exception
#         return func(self, *args, **kwargs)
#     return wrapper

