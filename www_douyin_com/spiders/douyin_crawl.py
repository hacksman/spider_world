#!/usr/bin/env python 
# coding:utf-8
# @Time :10/5/18 15:48

import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import time
import json
import os
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

    __FAVORITE_PARAMS = {
        "count": "21",
        "user_id": None,
        "max_cursor": 0
    }

    # try times
    __MAX_TIMES_DOWNLOAD_VEDIO = 5

    def __init__(self):
        self.common_params = common_params()

    def __get_token(self):
        return getToken()

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

        for per_person in persons:
            has_more, max_cursor = self.grab_user_video(per_person)
            while has_more:
                has_more, max_cursor = self.grab_user_video(per_person, max_cursor)
            break


        # print(json.dumps(resp.text, ensure_ascii=False))
        # print(resp.text)

    # def spider_user_follows(self, user_id):
    #     total_offset = self.grab_follow_list(user_id)

        # for i in range(1, total_offset):
            # offset

    def grab_user_video(self, user_info, max_cursor=0):
        nickname = user_info.get('nickname')
        unique_id = user_info.get('unique_id')
        uid = user_info.get('uid')
        signature = user_info.get("signature")

        print(nickname, signature, uid, unique_id)

        user_video_params = self.__USER_VIDEO_PARAMS
        user_video_params['user_id'] = uid
        user_video_params['max_cursor'] = max_cursor

        query_params = {**user_video_params, **self.common_params}
        sign = getSign(self.__get_token(), query_params)
        params = {**query_params, **sign}
        resp = requests.get(self.__USER_VIDEO_URL,
                            params=params,
                            verify=False,
                            headers=self.__HEADERS)

        video_infos = resp.json().get("aweme_list")
        has_more = resp.json().get("has_more")
        max_cursor = resp.json().get("max_cursor")

        for per_video in video_infos:
            aweme_id = per_video.get("aweme_id")
            self.download_user_video(aweme_id, nickname)

        return has_more, max_cursor

    def download_user_video(self, aweme_id, nickname):
        video_content = self.download_video(aweme_id)

        if not os.path.exists("../videos/{}".format(nickname)):
            os.makedirs('../videos/{}'.format(nickname))

        with open('../videos/{}/{}.mp4'.format(nickname, aweme_id), 'wb') as f:
            f.write(video_content)


    def grab_favorite_main(self, user_id):
        count = 1
        self.logger.info("当前正在爬取第 👉 {} 👈 页内容...".format(count))
        hasmore, max_cursor = self.grab_favorite(user_id)
        while hasmore:
            count += 1
            self.logger.info("当前正在爬取第 👉 {} 👈 页内容...".format(count))
            hasmore, max_cursor = self.grab_favorite(user_id, max_cursor)


    def grab_favorite(self, user_id, max_cursor=0):
        favorite_params = self.__FAVORITE_PARAMS
        favorite_params['user_id'] = user_id
        favorite_params['max_cursor'] = max_cursor
        query_params = {**favorite_params, **self.common_params}
        sign = getSign(self.__get_token(), query_params)
        params = {**query_params, **sign}
        resp = requests.get(self.__FAVORITE_URL,
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
            self.download_favorite_video(aweme_id, **download_item)
            time.sleep(5)

        return hasmore, max_cursor

    def download_favorite_video(self, aweme_id, **video_infos):
        video_content = self.download_video(aweme_id)
        author_nick_name = video_infos.get("author_nick_name")
        author_uid = video_infos.get("author_uid")
        video_desc = video_infos.get("video_desc")
        video_name = "_".join([author_nick_name, author_uid, video_desc])

        self.logger.info("download_favorite_video 正在下载视频 {} ".format(video_name))

        if not video_content:
            self.logger.warn("你正在下载的视频，由于某种神秘力量的作用，已经凉凉了，请跳过...")
            return

        with open("../videos/{}.mp4".format(video_name), 'wb') as f:
            f.write(video_content)

    def download_video(self, aweme_id, retry_times=0):
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

        # 重试弃用
        # try:
        #     resp_result = resp.json()
        #     if aweme_id == "6603499423932615943":
        #         self.logger.info("download_video 正在下载视频...，此时resp_json={}".format(resp.json()))
        # except:
        #     self.logger.error("download_video 解析json时发生错误，此时resp={}".format(resp.text))
        #     while retry_times <= self.__MAX_TIMES_DOWNLOAD_VEDIO:
        #         retry_times += 1
        #         self.logger.info("正在进行第 {} 次重试爬取...".format(retry_times))
        #         time.sleep(retry_times*5)
        #         content = self.download_video(aweme_id, retry_times)
        #         return content
        #     self.logger.error("download_video 重试了最大次数，但依然无法提取视频...")
        #     return None

        resp_result = resp.json()
        play_addr_raw = resp_result['aweme_detail']['video']['play_addr']['url_list']

        # 重试弃用
        # if not play_addr_raw:
        #     self.logger.warn("download_video 并未提取到视频数据...")
        #     while retry_times <= self.__MAX_TIMES_DOWNLOAD_VEDIO:
        #         retry_times += 1
        #         self.logger.info("正在进行第 {} 次重试爬取...".format(retry_times))
        #         time.sleep(retry_times*5)
        #         content = self.download_video(aweme_id, retry_times)
        #         return content
        #     self.logger.error("download_video 重试了最大次数，但依然无法提取视频...")
        #     return None

        play_addr = play_addr_raw[0]

        content = requests.get(play_addr).content

        return content


if __name__ == '__main__':
    douyin = DouyinCrawl()
    user_id = '00000'
    # douyin.grab_follow_list(user_id, offset=0)
    douyin.grab_favorite_main(user_id)
