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
        "device_id":        str(device_info['device_id']),
        "openudid":         str(device_info['openudid']),
        "iid":              str(device_info['install_id']),
    }
    params = {**item, **APPINFO}
    return params


def gen_real_url(token, raw_url, query):
    if isinstance(query, dict):
        query = params2str(query)
    url = raw_url + "?" + query
    resp = fetch(URL.api_sign(token), json={"url": url}, method="post")
    if not resp:
        print("你的当日 token 次数已经用完，请明天再来尝试吧...")
        raise BaseException("you have run out of token.Please try tomorrow")
    resp_json = resp.json()
    real_url = resp_json['url']
    return real_url
