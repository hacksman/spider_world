#!/usr/bin/env python 
# coding:utf-8

TOKEN = "关注公众号【鸡仔说】回复【抖音】获取自己的唯一 token 号"

DEFALUT_REQ_TIMEOUT = 5
MAX_RETRY_REQ_TIMES = 3
RETRY_RANDON_MIN_WAIT = 1000  # ms
RETRY_RANDON_MAX_WAIT = 5000  # ms

COMMON_HEADERS = {"User-Agent": "okhttp/3.10.0.1"}

APPINFO = {
    "version_code": "290",
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
    "aid": "1128",
    "ac": "wifi",
}

COMMON_COOKIES = {
    'ttreq': '1$f58a422877af68a234141b2dc94eda292d8cd901',
    'sid_guard': '190e1d75900416b7eb62c639d7fe653a%7C1548671527%7C5184000%7CFri%2C+29-Mar-2019+10%3A32%3A07+GMT',
    'uid_tt': '51289fc385905048dbc45575efead7d5',
    'sid_tt': '190e1d75900416b7eb62c639d7fe653a',
    'sessionid': '190e1d75900416b7eb62c639d7fe653a',
    'odin_tt': "d44fbf1baf710b502070386558b48c94250edc24497a85f029c3cbef046cf706d27692be6295813ef3c6ca20dfa2a405d2d4a0d169224c3f65a1b55e18d33bf7"
}


