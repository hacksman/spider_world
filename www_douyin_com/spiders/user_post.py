#!/usr/bin/env python 
# coding:utf-8

from www_douyin_com.common.utils import URL
from www_douyin_com.utils.gen_base import (gen_device, gen_common_params, gen_real_url)
from www_douyin_com.utils.fetch import fetch
from www_douyin_com.config import TOKEN
from www_douyin_com.config import COMMON_COOKIES
from www_douyin_com.config import COMMON_HEADERS
from www_douyin_com.utils.transform import data_to_video

import json
import time
import random


def post(user_id):

    device = gen_device(TOKEN)
    common_params = gen_common_params(device)

    count = 0

    max_cursor = 0

    while True:

        query_params = {"count": 21 if not count else count, "user_id": user_id, "max_cursor": max_cursor}
        search_params = {**common_params, **query_params}
        real_url = gen_real_url(TOKEN, URL.favorite_url(), search_params)

        cookies = COMMON_COOKIES
        cookies['install_id'] = str(device["install_id"])

        # download video
        resp = fetch(real_url,
                     verify=False,
                     cookies=cookies,
                     headers=COMMON_HEADERS,
                     timeout=3).json()

        if resp.get("has_more") != 1:
            print("%s post video spider done!" % user_id)
            break

        print(json.dumps(resp, ensure_ascii=False))

        results = []
        for video_info in resp.get("aweme_list"):
            results.append(data_to_video(video_info))

        yield resp

        max_cursor = resp.get("max_cursor")
        count = 12
        # time.sleep(5)


if __name__ == '__main__':
    count = 0
    for i in post("73763378004"):
        pass
        # count += 1
        # if count > 2:
        #     break

