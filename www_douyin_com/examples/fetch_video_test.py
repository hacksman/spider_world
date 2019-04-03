#!/usr/bin/env python 
# coding:utf-8

from www_douyin_com.common.utils import URL
from www_douyin_com.utils.gen_base import (gen_device, gen_common_params, gen_real_url)
from www_douyin_com.utils.fetch import fetch
from www_douyin_com.config import COMMON_COOKIES
from www_douyin_com.config import COMMON_HEADERS

import json

if __name__ == '__main__':
    token = "关注公众号【鸡仔说】回复【抖音】获取自己的唯一 token 号"
    user_id = "73763378004"
    max_cursor = "0"
    device = gen_device(token)
    common_params = gen_common_params(device)
    query_params = {"count": "20", "user_id": user_id, "max_cursor": max_cursor}
    search_params = {**common_params, **query_params}
    real_url = gen_real_url(token, URL.favorite_url(), search_params)

    cookies = COMMON_COOKIES
    cookies['install_id'] = str(device["install_id"])

    # download video
    resp = fetch(real_url,
                 verify=False,
                 cookies=cookies,
                 headers=COMMON_HEADERS,
                 timeout=3)

    print(json.dumps(resp, ensure_ascii=False))
