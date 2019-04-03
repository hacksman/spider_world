#!/usr/bin/env python 
# coding:utf-8

from www_douyin_com.utils.fetch import fetch
from www_douyin_com.common.urls import URL
from www_douyin_com.config import APPINFO
from www_douyin_com.utils.tools import params2str


def gen_device(token):
    resp = fetch(URL.api_device(token), timeout=10).json()
    return resp


def gen_common_params(device_info):
    item = {
        "new_user":         str(device_info['new_user']),
        "device_id":        str(device_info['device_id']),
        "openudid":         str(device_info['openudid']),
        "iid":              str(device_info['install_id']),
        "android_id":       str(device_info['android_id']),
    }
    params = {**item, **APPINFO}
    return params


def gen_real_url(token, raw_url, query):
    if isinstance(query, dict):
        query = params2str(query)
    url = raw_url + "?" + query
    resp = fetch(URL.api_sign(token), json={"url": url}, method="post").json()
    real_url = resp['url']
    return real_url
