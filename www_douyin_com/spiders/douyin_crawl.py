#!/usr/bin/env python 
# coding:utf-8
# @Time :10/5/18 15:48

import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import time
import json
import re
import os
import sys

sys.path.append('../')
sys.path.append('../../')
sys.path.append('../../../')

file_path_now = os.path.abspath(__file__)

from www_douyin_com.common.utils import *
from www_douyin_com.common.log_handler import getLogger


class DouyinCrawl(object):
    logger = getLogger("DouyinCrawl", console_out=True)

    # headers
    __HEADERS = {"User-Agent": "Aweme/2.7.0 (iPhone; iOS 11.0; Scale/2.00)"}
    # __HEADERS = {"User-Agent": "Aweme/2.8.0 (iPhone; iOS 12.0; Scale/2.00)"}

    # urls
    __FOLLOW_URL                = "https://aweme.snssdk.com/aweme/v1/user/following/list/"
    __USER_VIDEO_URL            = "https://aweme.snssdk.com/aweme/v1/aweme/post/"
    __VIDEO_DETAIL_URL          = "https://aweme.snssdk.com/aweme/v1/aweme/detail/"
    __FAVORITE_URL              = "https://aweme.snssdk.com/aweme/v1/aweme/favorite/"
    __POST_URL                  = "https://aweme.snssdk.com/aweme/v1/aweme/post/"
    # __FOLLOW_USER_URL           = "https://aweme.snssdk.com/aweme/v1/commit/follow/user/"

    # params
    __FOLLOW_LIST_PARAMS = {
        "count": "20",
        "offset": "0",
        "user_id": None,
        "source_type": "2",
        "max_time": int(time.time()),
    }

    __USER_VIDEO_PARAMS = {
        "count": "21",
        # "offset": "0",
        "user_id": None,
        # "max_cursor": str(int(time.time())) + "000",
        "max_cursor": "0",
    }

    # try times

    # common
    __MAX_TOKEN_VALIDITY = 60 * 50

    def __init__(self):
        self.common_params = common_params()

        self.__token_last_time = int(time.time())

        self.__token = None

    def __get_token(self):
        current_time = int(time.time())

        # 第一次获取token
        if not self.__token:
            self.__token_last_time = current_time
            self.__token = getToken()
            return self.__token

        # token有效期已过
        if current_time - self.__token_last_time > self.__MAX_TOKEN_VALIDITY:
            self.logger.info("__token 在有效期内已过，重新获取...")
            self.__token = getToken()
            self.__token_last_time = current_time
            return self.__token

        return self.__token

    def __get_device(self):
        return getDevice()

    def __generate_sign(self, token, params):
        sign = getSign(token, params)
        return sign

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

        # for per_person in persons:
        #     has_more, max_cursor = self.grab_user_video(per_person)
        #     while has_more:
        #         has_more, max_cursor = self.grab_user_video(per_person, max_cursor)
        #     break

    def grab_video_main(self, user_id, user_type):
        count = 1
        self.logger.info("当前正在爬取 user id 为 {} 的第 👉 {} 👈 页内容...".format(user_id ,count))
        hasmore, max_cursor = self.grab_video(user_id, user_type)
        while hasmore:
            count += 1
            self.logger.info("当前正在爬取 user id 为 {} 的第 👉 {} 👈 页内容...".format(user_id, count))
            hasmore, max_cursor = self.grab_video(user_id, user_type, max_cursor)

    def grab_video(self, user_id, user_type, max_cursor=0):
        favorite_params = self.__USER_VIDEO_PARAMS
        favorite_params['user_id'] = user_id
        favorite_params['max_cursor'] = max_cursor
        query_params = {**favorite_params, **self.common_params}
        sign = getSign(self.__get_token(), query_params)
        params = {**query_params, **sign}

        # 目前支持两种类型爬取，用户喜欢过的，和当前用户所有已发布的视频
        url = self.__FAVORITE_URL if user_type == "MY_LOVE" else self.__POST_URL
        resp = requests.get(url,
                            params=params,
                            verify=False,
                            headers=self.__HEADERS)

        favorite_info = resp.json()

        hasmore = favorite_info.get('has_more')
        max_cursor = favorite_info.get('max_cursor')
        video_infos = favorite_info.get('aweme_list')

        for per_video in video_infos:
            author_nick_name = per_video['author'].get("nickname")
            author_uid = per_video['author'].get('uid')
            video_desc = per_video.get('desc')
            download_item = {
                "author_nick_name": author_nick_name,
                "video_desc": video_desc,
                "author_uid": author_uid,
            }
            aweme_id = per_video.get("aweme_id")
            self.download_user_video(aweme_id, **download_item)
            time.sleep(5)

        return hasmore, max_cursor

    def download_user_video(self, aweme_id, **video_infos):
        video_content = self.download_video(aweme_id)
        author_nick_name = video_infos.get("author_nick_name")
        author_uid = video_infos.get("author_uid")
        video_desc = video_infos.get("video_desc")
        video_name = "_".join([author_nick_name, author_uid, video_desc])

        self.logger.info("download_favorite_video 正在下载视频 {} ".format(video_name))

        if not video_content:
            self.logger.warn("你正在下载的视频，由于某种神秘力量的作用，已经凉凉了，请跳过...")
            return
        file_path_grandfather = "/".join(file_path_now.split("/")[:-2])

        if not os.path.exists("{}/videos/{}".format(file_path_grandfather, author_nick_name)):
            os.makedirs("{}/videos/{}".format(file_path_grandfather, author_nick_name))

        with open("{}/videos/{}/{}.mp4".format(file_path_grandfather, author_nick_name, video_name), 'wb') as f:
            f.write(video_content)

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
        resp_result = resp.json()
        play_addr_raw = resp_result['aweme_detail']['video']['play_addr']['url_list']
        play_addr = play_addr_raw[0]
        content = requests.get(play_addr).content
        return content

    def download_one_video(self, aweme_id):
        if not re.findall('^\d{19}$', aweme_id):
            self.logger.error("download_one_video 收到错误的视频id，校验后再尝试")
            self.logger.error("正确的视频id是19位纯数字")
            return
        author_nick_name = "单视频下载专用目录"
        video_name = aweme_id
        file_path_grandfather = "/".join(file_path_now.split("/")[:-2])
        if not os.path.exists("{}/videos/{}".format(file_path_grandfather, author_nick_name)):
            os.makedirs("{}/videos/{}".format(file_path_grandfather, author_nick_name))
        video_content = self.download_video(aweme_id)
        with open("{}/videos/{}/{}.mp4".format(file_path_grandfather, author_nick_name, video_name), 'wb') as f:
            f.write(video_content)


if __name__ == '__main__':
    douyin = DouyinCrawl()
    input = input("请输入用户的id（11位纯数字）：")
    user_id = '98524853984'
    if not re.findall('^\d{11}$', input):
        print("请输入正确的用户id， 用户id为11位纯数字")
    else:
        douyin.grab_video(input, "USER_POST")
