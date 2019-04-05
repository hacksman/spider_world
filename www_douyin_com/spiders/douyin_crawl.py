#!/usr/bin/env python 
# coding:utf-8
# @Time :10/5/18 15:48
import csv
import io

import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import time
import json
import copy
import re
import os
import sys

sys.path.append('../')
sys.path.append('../../')
sys.path.append('../../../')

file_path_now = os.path.abspath(__file__)

from www_douyin_com.common.utils import *
from www_douyin_com.common.log_handler import getLogger

from www_douyin_com.common.urls import URL
from www_douyin_com.utils.fetch import fetch
from www_douyin_com.config import TOKEN


class DouyinCrawl(object):
    logger = getLogger("DouyinCrawl", console_out=True)

    # headers
    __HEADERS = {"User-Agent": "okhttp/3.10.0.1"}

    # params
    __FOLLOW_LIST_PARAMS = {
        "count": "20",
        "offset": "0",
        "user_id": None,
        "source_type": "2",
        "max_time": int(time.time()),
    }

    __COMMENT_LIST_PARAMS = {
        "count": "20",
        "cursor": "0",
        "comment_style": '2',
        "aweme_id": None,
        "digged_cid": "",
    }

    __USER_VIDEO_PARAMS = {
        "count": "20",
        # "offset": "0",
        "user_id": None,
        # "max_cursor": str(int(time.time())) + "000",
        "max_cursor": "0",
    }

    __COOKIES = {
            'ttreq': '1$f58a422877af68a234141b2dc94eda292d8cd901',
            'sid_guard': '190e1d75900416b7eb62c639d7fe653a%7C1548671527%7C5184000%7CFri%2C+29-Mar-2019+10%3A32%3A07+GMT',
            'uid_tt': '51289fc385905048dbc45575efead7d5',
            'sid_tt': '190e1d75900416b7eb62c639d7fe653a',
            'sessionid': '190e1d75900416b7eb62c639d7fe653a',
            'odin_tt': "d44fbf1baf710b502070386558b48c94250edc24497a85f029c3cbef046cf706d27692be6295813ef3c6ca20dfa2a405d2d4a0d169224c3f65a1b55e18d33bf7",
        }

    # try times

    # common
    __MAX_TOKEN_VALIDITY = 60 * 50

    def __init__(self, token):

        self.__device_last_time = int(time.time())

        self.token = token

        self.__device = None

        self.common_params = None

        self.__update_device_common_params()

    def __update_device_common_params(self):

        current_time = int(time.time())

        if not self.__device:
            self.__device = get_device(self.token)
            self.common_params = common_params(self.__device)
            print(self.__device)
            self.__device_last_time = current_time
            return

        if current_time - self.__device_last_time > self.__MAX_TOKEN_VALIDITY:
            self.logger.info("__device 在有效期内已过，重新获取...")
            self.__device = get_device(self.token)
            self.common_params = common_params(self.__device)
            self.__device_last_time = current_time

    def grab_user_media(self, user_id, action, content=None):
        count = 1
        self.logger.info("当前正在爬取 user id 为 {} 的第 👉 {} 👈 页内容...".format(user_id ,count))
        hasmore, max_cursor = self.grab_video(user_id, action, content)
        while hasmore:
            count += 1
            self.logger.info("当前正在爬取 user id 为 {} 的第 👉 {} 👈 页内容...".format(user_id, count))
            hasmore, max_cursor = self.grab_video(user_id, action, content, max_cursor)

    def grab_video(self, user_id, action, content, max_cursor=0):

        url = URL.favorite_url() if action == "USER_LIKE" else URL.post_url()

        favorite_params = copy.deepcopy(self.__USER_VIDEO_PARAMS)
        favorite_params['user_id'] = user_id
        favorite_params['max_cursor'] = max_cursor
        query_params = {**favorite_params, **self.common_params}
        real_url = gen_url(self.token, url, query_params)
        # 目前支持两种类型爬取，用户喜欢过的，和当前用户所有已发布的视频
        cookies = self.__COOKIES
        cookies['install_id'] = str(self.__device["install_id"])

        resp = requests.get(real_url,
                            verify=False,
                            cookies=cookies,
                            headers={"User-Agent": "okhttp/3.10.0.1"},
                            timeout=3)

        favorite_info = json.loads(resp.content.decode("utf-8"))

        hasmore = favorite_info.get('has_more')
        max_cursor = favorite_info.get('max_cursor')
        video_infos = favorite_info.get('aweme_list')

        for per_video in video_infos:
            author_nick_name = per_video['author'].get("nickname")
            author_uid = per_video['author'].get('uid')
            video_desc = per_video.get('desc')
            music_id = per_video['music']['play_url'].get('uri') if content == "-m" else None
            download_item = {
                "author_nick_name": author_nick_name,
                "video_desc": video_desc,
                "author_uid": author_uid,
                "music_id": music_id
            }
            aweme_id = per_video.get("aweme_id")
            self.download_user_video(aweme_id, **download_item)
            time.sleep(5)

        return hasmore, max_cursor

    def grab_comment_main(self, aweme_id, upvote_bound=1):
        has_more = self.__grab_comment(aweme_id, upvote_bound)
        cursor = -20
        while True:
            cursor += 20
            if has_more == -2:
                self.logger.info("已经到达采集设定的最低点赞数，停止采集...")
                break
            if has_more == 0:
                self.logger.info("没有更多的评论内容，停止采集...")
                break
            has_more = self.__grab_comment(aweme_id, cursor, upvote_bound)

    def __grab_comment(self, aweme_id, cursor, upvote_bound=10):
        url = URL.comment_url()
        comment_params = copy.deepcopy(self.__COMMENT_LIST_PARAMS)
        comment_params['aweme_id'] = aweme_id
        comment_params['cursor'] = cursor
        params = {**comment_params, **self.common_params}
        real_url = gen_url(self.token, url, params)

        cookies = self.__COOKIES
        cookies['install_id'] = str(self.__device["install_id"])

        resp = requests.get(real_url,
                            verify=False,
                            cookies=cookies,
                            headers=self.__HEADERS)

        comment_content = json.loads(resp.content.decode("utf-8"))

        comments = comment_content.get("comments")

        for per_comment in comments:
            is_reply = per_comment.get("reply_comment")
            if is_reply:
                upvote_count = is_reply[0].get("digg_count")
                comment_info = {
                    "text": is_reply[0].get("text"),
                    "upvote_count": upvote_count,
                    "nick_name": is_reply[0]['user'].get("nickname"),
                    "user_id": is_reply[0]['user'].get("uid"),

                }
            else:
                upvote_count = per_comment.get("digg_count")
                comment_info = {
                    "text": per_comment.get("text"),
                    "upvote_count": upvote_count,
                    "nick_name": per_comment['user'].get("nickname"),
                    "user_id": per_comment['user'].get("uid"),
                }

            if int(upvote_count) < upvote_bound:
                return -2

            self.download_comment(aweme_id, **comment_info)

        # print(text,upvote_count,nick_name,user_id)

        hasmore = int(comment_content.get("hasmore"))

        return hasmore

    def download_user_video(self, aweme_id, **video_infos):

        video_content = self.download_video(aweme_id)
        music_id = video_infos.get("music_id")
        music_content = self.download_music(music_id)
        author_nick_name = video_infos.get("author_nick_name")
        author_uid = video_infos.get("author_uid")
        video_desc = video_infos.get("video_desc")
        video_name = "_".join([author_nick_name, author_uid, video_desc])

        music_log_info = "和音频" if music_content else ""
        self.logger.info("download_favorite_video 正在下载视频{} {} ".format(music_log_info, video_name))

        if not video_content:
            self.logger.warn("你正在下载的视频，由于某种神秘力量的作用，已经凉凉了，请跳过...")
            return
        file_path_grandfather = "/".join(file_path_now.split("/")[:-2])

        if not os.path.exists("{}/videos/{}".format(file_path_grandfather, author_nick_name)):
            os.makedirs("{}/videos/{}".format(file_path_grandfather, author_nick_name))

        with open("{}/videos/{}/{}.mp4".format(file_path_grandfather, author_nick_name, video_name), 'wb') as f:
            f.write(video_content)

        # 若存在音乐内容，则进行下载
        if music_content:
            with open("{}/videos/{}/{}.mp3".format(file_path_grandfather, author_nick_name, video_name), 'wb') as f:
                f.write(music_content)

    def download_music(self, music_id):

        if not music_id:
            return

        url = URL.music_url(music_id)

        resp = requests.get(url, headers=self.__HEADERS, verify=False)

        music_content = resp.content

        return music_content

    def download_video(self, aweme_id):

        query_params = self.common_params
        query_params['aweme_id'] = aweme_id

        params = {**query_params, **self.common_params}

        url = URL.video_detail_url()

        real_url = gen_url(self.token, url, params)

        post_data = {
            "aweme_id": aweme_id
        }

        cookies = self.__COOKIES
        cookies['install_id'] = str(self.__device["install_id"])

        resp = fetch(real_url,
                     data=post_data,
                     cookies=cookies,
                     headers=self.__HEADERS,
                     timeout=3).json()

        try:
            play_addr_raw = resp['aweme_detail']['video']['play_addr']['url_list']
            play_addr = play_addr_raw[0]
            print(play_addr)
            content = fetch(play_addr).content
        except:
            self.logger.warning("提取视频信息失败...")
            content = None

        return content

    def download_one_video(self, aweme_id):
        author_nick_name = "单视频下载专用目录"
        video_name = aweme_id
        file_path_grandfather = "/".join(file_path_now.split("/")[:-2])
        if not os.path.exists("{}/videos/{}".format(file_path_grandfather, author_nick_name)):
            os.makedirs("{}/videos/{}".format(file_path_grandfather, author_nick_name))
        video_content = self.download_video(aweme_id)
        if video_content:
            with open("{}/videos/{}/{}.mp4".format(file_path_grandfather, author_nick_name, video_name), 'wb') as f:
                f.write(video_content)

    def download_comment(self, aweme_id, **comment_info):
        comment_sort = [0, 0, 0, 0]
        print(comment_info)
        for k, v in comment_info.items():
            if k == "user_id":
                comment_sort[0] = v
            elif k == "nick_name":
                comment_sort[1] = v
            elif k == "upvote_count":
                comment_sort[2] = v
            else:
                comment_sort[3] = v
        with io.open("{}.csv".format(aweme_id), "a+", encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(comment_sort)


if __name__ == '__main__':

    token = "关注公众号【鸡仔说】回复【抖音】获取自己的唯一 token 号"

    douyin = DouyinCrawl(TOKEN)

    aweme_id = "6675585689419091212"

    user_id = "73763378004"

    # douyin.grab_user_media(user_id, "USER_POST")
    # douyin.grab_comment_main(aweme_id)
    douyin.download_one_video(aweme_id)
