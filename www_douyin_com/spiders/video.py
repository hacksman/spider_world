#!/usr/bin/env python 
# coding:utf-8

from www_douyin_com.common.utils import URL
from www_douyin_com.config import TOKEN
from www_douyin_com.config import COMMON_COOKIES
from www_douyin_com.config import COMMON_HEADERS
from www_douyin_com.utils.fetch import fetch
from www_douyin_com.utils.gen_base import (gen_device, gen_common_params, gen_real_url)


def aweme_id_video_url(aweme_id):

    query_params = {'aweme_id': aweme_id}
    device_info = gen_device(TOKEN)

    params = {**query_params, **gen_common_params(device_info)}

    url = URL.video_detail_url()

    real_url = gen_real_url(TOKEN, url, params)

    cookies = COMMON_COOKIES
    cookies['install_id'] = str(device_info["install_id"])

    resp_json = fetch(real_url,
                      cookies=cookies,
                      headers=COMMON_HEADERS,
                      timeout=3).json()

    url_list = resp_json.get('aweme_detail', {}).get("video", {}).get("play_addr", {}).get("url_list", [])
    if len(url_list) > 0:
        return url_list[0]
