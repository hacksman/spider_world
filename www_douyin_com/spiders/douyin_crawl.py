#!/usr/bin/env python 
# coding:utf-8
# @Time :10/5/18 15:48
from backports import csv
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
from www_douyin_com.spiders.douyin_login import DouyinLogin


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
    __COMMENT_URL               = "https://aweme.snssdk.com/aweme/v1/comment/list/"
    __MUSIC_URL                 = "https://p3.pstatp.com/obj/"
    # __FOLLOW_USER_URL           = "https://aweme.snssdk.com/aweme/v1/commit/follow/user/"

    # login url
    __LIKE_VIDEO                = "https://aweme.snssdk.com/aweme/v1/commit/item/digg/"

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
        "count": "21",
        # "offset": "0",
        "user_id": None,
        # "max_cursor": str(int(time.time())) + "000",
        "max_cursor": "0",
    }

    # try times

    # common
    __MAX_TOKEN_VALIDITY = 60 * 50

    def __init__(self, phone=None):
        self.common_params = common_params()

        self.__token_last_time = int(time.time())

        self.__token = None

        self.__request = self.__init__session(phone) if phone else None

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

    def __init__session(self, phone):
        if not phone:
            self.logger.info("请输入手机号码以登录账户!!!")
            return
        return DouyinLogin().login_pickle_cookie()

    def grab_user_media(self, user_id, action, content=None):

        if not re.findall('^\d{11,12}$', user_id):
            self.logger.info("请输入正确的用户id， 用户id为11或12位纯数字...")
            return

        count = 1
        self.logger.info("当前正在爬取 user id 为 {} 的第 👉 {} 👈 页内容...".format(user_id ,count))
        hasmore, max_cursor = self.grab_video(user_id, action, content)
        while hasmore:
            count += 1
            self.logger.info("当前正在爬取 user id 为 {} 的第 👉 {} 👈 页内容...".format(user_id, count))
            hasmore, max_cursor = self.grab_video(user_id, action, content, max_cursor)

    def grab_video(self, user_id, action, content, max_cursor=0):
        favorite_params = copy.deepcopy(self.__USER_VIDEO_PARAMS)
        favorite_params['user_id'] = user_id
        favorite_params['max_cursor'] = max_cursor
        query_params = {**favorite_params, **self.common_params}
        sign = getSign(self.__get_token(), query_params)
        params = {**query_params, **sign}

        # 目前支持两种类型爬取，用户喜欢过的，和当前用户所有已发布的视频
        url = self.__FAVORITE_URL if action == "USER_LIKE" else self.__POST_URL
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
        comment_params = copy.deepcopy(self.__COMMENT_LIST_PARAMS)
        comment_params['aweme_id'] = aweme_id
        comment_params['cursor'] = cursor
        query_params = {**comment_params, **self.common_params}
        sign = getSign(self.__get_token(), query_params)
        params = {**query_params, **sign}
        resp = requests.get(self.__COMMENT_URL,
                            params=params,
                            verify=False,
                            headers=self.__HEADERS)
        comment_content = resp.json()

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

            print(upvote_count)

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

        url = self.__MUSIC_URL + music_id

        resp = requests.get(url, headers=self.__HEADERS, verify=False)

        music_content = resp.content

        return music_content

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
        # print(resp_result)
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

    def like_video(self, aweme_id):
        query_params = {**{"pass-region": "1"}, **self.common_params}
        sign = getSign(self.__get_token(), query_params)
        params = {**query_params, **sign}

        form_params = {
            "aweme_id": aweme_id,
            "type": 1
        }

        headers = copy.deepcopy(self.__HEADERS)
        headers["sdk-version"] = '1'
        headers["Accept-Encoding"] = 'br, gzip, deflate'

        print(self.__request.cookies)

        result = self.__request.post(self.__LIKE_VIDEO,
                                     params=params,
                                     data=form_params,
                                     verify=False,
                                     headers=headers)

        print(result.json())

        # if result.json().get("status_code") == "0":
        #     self.logger.info("喜欢成功...")


if __name__ == '__main__':
    douyin = DouyinCrawl("123")

    aweme_id = "6612876887381249287"

    douyin.like_video(aweme_id)
