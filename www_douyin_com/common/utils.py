#!/usr/bin/env python 
# coding:utf-8
# @Time :10/6/18 16:31

import requests

API = "https://api.appsign.vip:2688"
APPINFO = {
    "version_code": "2.7.0",
    "app_version": "2.7.0",
    "channel": "App%20Stroe",
    "app_name": "aweme",
    "build_number": "27014",
    "aid": "1128",
}

# APPINFO = {
#     "version_code": "2.8.0",
#     "app_version": "2.8.0",
#     "channel": "App Store",
#     "app_name": "aweme",
#     "build_number": "28007",
#     "aid": "1128",
# }

header = {
    "User-Agent": "Aweme/2.7.0 (iPhone; iOS 12.0; Scale/2.00)"
}

# 获取Token       有效期60分钟
def getToken():
    #resp = requests.get(API + "/token/douyin").json()
    resp = requests.get(API + "/token/douyin/version/2.7.0").json()
    token = resp['token']
    # print("Token: " + token)
    return token

# 获取新的设备信息  有效期60分钟永久
def getDevice():
    #resp = requests.get(API + "/douyin/device/new").json()
    resp = requests.get(API + "/douyin/device/new/version/2.7.0").json()
    # resp = requests.get(API + "/douyin/device/new/version/").json()
    device_info = resp['data']
    # print("设备信息: " + str(device_info))
    return device_info

# 拼装参数
def params2str(params):
    query = ""
    for k, v in params.items():
        query += "%s=%s&" % (k, v)
    query = query.strip("&")
    # print("Sign str: " + query)
    return query

# 使用拼装参数签名
def getSign(token, query):
    if isinstance(query, dict):
        query = params2str(query)
    resp = requests.post(API + "/sign", json={"token": token, "query": query}).json()
    # print("签名返回: " + str(resp))
    sign = resp['data']
    return sign

# 混淆手机号码和密码
def mixString(pwd):
    password = ""
    for i in range(len(pwd)):
        password += hex(ord(pwd[i]) ^ 5)[-2:]
    return password


def common_params():
    device_info = getDevice()
    item = {
        "iid":              device_info['iid'],
        "idfa":             device_info['idfa'],
        "vid":              device_info['vid'],
        "device_id":        device_info['device_id'],
        "openudid":         device_info['openudid'],
        "device_type":      device_info['device_type'],
        "os_version":       device_info['os_version'],
        "os_api":           device_info['os_api'],
        "screen_width":     device_info['screen_width'],
        "device_platform":  device_info['device_platform'],
        "version_code":     APPINFO['version_code'],
        "channel":          APPINFO['channel'],
        "app_name":         APPINFO['app_name'],
        "build_number":     APPINFO['build_number'],
        "app_version":      APPINFO['app_version'],
        "aid":              APPINFO['aid'],
        "ac":               "WIFI",
    }
    return item


# check douyin id
import re
import functools
def check_id(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if not re.findall('^\d{10,13}$', args[0]):
            self.logger.info("请输入正确的用户id， 用户id为10,11,12或13位纯数字...")
            raise Exception
        return func(self, *args, **kwargs)
    return wrapper

