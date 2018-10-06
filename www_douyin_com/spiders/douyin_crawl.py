#!/usr/bin/env python 
# coding:utf-8
# @Time :10/5/18 15:48

import requests
import time
import json

from www_douyin_com.common.utils import *


class DouyinCrawl(object):

    # headers
    __HEADERS = {"User-Agent": "Aweme/2.7.0 (iPhone; iOS 11.0; Scale/2.00)"}
    # __HEADERS = {"User-Agent": "Aweme/2.8.0 (iPhone; iOS 12.0; Scale/2.00)"}

    # urls
    __FOLLOW_URL                = "https://aweme.snssdk.com/aweme/v1/user/following/list/"
    __USER_VIDEO_URL            = "https://aweme.snssdk.com/aweme/v1/aweme/post/"
    __VIDEO_DETAIL_URL          = "https://aweme.snssdk.com/aweme/v1/aweme/detail/"

    # common params
    __FOLLOW_LIST_PARAMS = {
        "count": "20",
        "offset": "0",
        "user_id": None,
        "source_type": "2",
        "max_time": int(time.time()),
    }

    __USER_VIDEO_PARAMS = {
        "count": "12",
        # "offset": "0",
        "user_id": None,
        "max_cursor": str(int(time.time())) + "000",
    }

    def __init__(self):
        self.common_params = common_params()

    def __get_token(self):
        return getToken()

    def __get_device(self):
        return getDevice()

    def __generate_sign(self, token, params):
        sign = getSign(token, params)
        return sign

    def spider_video(self, url):
        resp = requests.get(url)
        print(resp.status_code)
        print(resp.text)

    def grab_follow_list(self, user_id, offset=0):
        follow_params = self.__FOLLOW_LIST_PARAMS
        follow_params['user_id'] = user_id
        follow_params['offset'] = offset
        query_params = {**follow_params, **self.common_params}
        sign = getSign(self.__get_token(), query_params)
        params = {**query_params, **sign}
        resp = requests.get(self.__FOLLOW_URL,
                            params=params,
                            verify=False,
                            headers=self.__HEADERS)

        # 获取所有偏置数
        # total_offset_page = json.loads(resp.text).get("total") // 20


        # 提取每个人的视频
        persons = resp.json().get('followings')

        for per_person in persons:
            self.grab_user_video(per_person)
            break


        # print(json.dumps(resp.text, ensure_ascii=False))
        # print(resp.text)

    # def spider_user_follows(self, user_id):
    #     total_offset = self.grab_follow_list(user_id)

        # for i in range(1, total_offset):
            # offset

    def grab_user_video(self, user_info):
        nickname = user_info.get('nickname')
        unique_id = user_info.get('unique_id')
        uid = user_info.get('uid')
        signature = user_info.get("signature")

        print(nickname, signature, uid, unique_id)

        user_video_params = self.__USER_VIDEO_PARAMS
        user_video_params['user_id'] = uid

        query_params = {**user_video_params, **self.common_params}
        sign = getSign(self.__get_token(), query_params)
        params = {**query_params, **sign}
        resp = requests.get(self.__USER_VIDEO_URL,
                            params=params,
                            verify=False,
                            headers=self.__HEADERS)

        video_infos = resp.json().get("aweme_list")

        for per_video in video_infos:
            aweme_id = per_video.get("aweme_id")
            self.download_video(aweme_id)

    def download_video(self, aweme_id):
        query_params = self.common_params
        query_params['aweme_id'] = aweme_id

        sign = getSign(self.__get_token(), query_params)
        params = {**query_params, **sign}

        post_data = {
            "aweme_id": aweme_id
        }

        resp = requests.get(self.__VIDEO_DETAIL_URL,
                            params=params,
                            data=post_data,
                            verify=False,
                            headers=self.__HEADERS)

        play_addr = resp.json()['aweme_detail']['video']['play_addr']['url_list'][0]

        content = requests.get(play_addr).content

        with open('../videos/{}.mp4'.format(aweme_id), 'wb') as f:
            f.write(content)


if __name__ == '__main__':
    douyin = DouyinCrawl()
    user_id = '000000'
    douyin.grab_follow_list(user_id, offset=0)
