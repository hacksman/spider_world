#!/usr/bin/env python 
# coding:utf-8
# @Time :1/1/19 16:52

import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

sys.path.append("..")
sys.path.append("../..")
sys.path.append("../../..")

import click
import random
import datetime
import requests
import time
import json

from common.logger import AppLogger

from common.mongo import MongDb
from configs.mongo_config import LocalMongoConfig


logger = AppLogger('yizhoucp.log').get_logger()


class YizhoucpCrawl(object):
    __START_URL = "https://api.myrightone.com/api/feed/moment-list"
    __LIKE_PID_URL = "https://api.myrightone.com/api/feed/like"

    __CRACK_SIGN_URL = "http://wx.zxiaoji.com/cp"

    __HOST = "api.myrightone.com"

    def __init__(self, secrite_key, token, user_id, check_code, log):
        self.log = log
        self.secrite_key = secrite_key
        self.user_id = user_id
        self.token = token
        self.check_code = check_code
        self.request = self.__init_reqeust()
        self.cp_mongo = MongDb(LocalMongoConfig.HOST,
                               LocalMongoConfig.PORT,
                               LocalMongoConfig.DB,
                               LocalMongoConfig.USER,
                               LocalMongoConfig.PASSWD,
                               log=self.log)

        self.cp_table = "yizhou_cp"

    def __init_reqeust(self):
        headers = {
            "Host": self.__HOST,
            "App-Id": self.token.split("_")[0],
            "Platform": "ios",
            "Token": self.token,
            "User-Agent": "Right-iOS/3.33.2 (com.myrightone.datecha; build:224; iOS 12.1.2) Alamofire/4.8.0",
            "Accept": "*/*",
            "Accept-Encoding": "gzip;q=1.0, compress;q=0.5",
            "Accept-Language": "zh-Hans-CN;q=1.0, en-CN;q=0.9",
        }
        self.request = requests.Session()
        self.request.headers = headers
        return self.request

    def __get_sign(self, params):
        req = requests.get(self.__CRACK_SIGN_URL, params={"secret_key": self.secrite_key,
                                                          "check_code": self.check_code,
                                                          "params": json.dumps(params)})
        req_json = req.json()
        if req_json.get("status") != 1:
            self.log.error("提取sign发生错误，错误原因是：")
            self.log.error(req_json.get("data"))
            return None
        return req_json.get("data")

    def get_moment_list(self):
        self.log.info("开始采集动态页")
        params = {
            "num": 20,
            "start": 0,
            "timestamp": int(time.time()),
            "type": "recommend",
            "user_id": self.user_id,
            "last_object_id": "",
        }

        sign = self.__get_sign(params)
        if not sign:
            return
        params["sign"] = sign
        resp = self.request.get(self.__START_URL, params=params, verify=False)
        resp_json = resp.json()
        return resp_json

    def like_sex(self, post_data, sex=2, exclude_cp=True):
        """
        :param fid: 文章id
        :param sex: 性别
        :return:
        """

        is_cp = post_data.get('left_user', None)
        if exclude_cp and is_cp:
            self.log.info("过滤掉cp组")
            return False
        category = post_data.get("category")
        if category == "topic":
            self.log.info("过滤掉话题..")
            return False

        fid = post_data.get("fid")
        nick_name = post_data["user"].get("nickname")
        post_text = post_data["payload"].get("text")

        mongo_exists = self.__update_like_mongo(fid, nick_name, post_text)
        if mongo_exists == -1:
            self.log.info("之前已对这条数据点过赞了，跳过...")
            return False

        raw_sex = post_data["user"].get('sex')

        if raw_sex == sex:
            fid_params = {
                "cancel": "0",
                "fid": fid,
                "timestamp": "0",
                "user_id": self.user_id,
            }
            sign = self.__get_sign(fid_params)
            fid_params["sign"] = sign
            resp = self.request.get(self.__LIKE_PID_URL, params=fid_params, verify=False)
            resp_json = resp.json()
            if resp_json.get("message") == "success":
                nick_name = post_data["user"].get("nickname")
                post_text = post_data["payload"].get("text")
                self.log.info("给用户({})发布的【{}】点赞成功".format(nick_name, post_text))
                return True

    def start(self, *args, **kwargs):
        count = 0
        like_count = 0
        while True:
            count += 1
            moment_data = self.get_moment_list()
            like_count_batch = 0
            for per_post in moment_data["data"]["list"]:
                like_succeed = self.like_sex(per_post)
                if like_succeed:
                    like_count_batch += 1
                    like_count += 1
                time.sleep(random.randint(1, 2))
                if like_count % 100 == 0:
                    self.log.info("当前已经对 {} 位小姐姐点过赞了...".format(like_count))
            self.log.info("当前已经遍历了第 {} 次动态".format(count))
            time.sleep(random.randint(5*like_count_batch, 7*like_count_batch))
            now = datetime.datetime.now()
            if now.hour in range(2, 6):
                time.sleep(random.randint(3600, 4000))

    def __update_like_mongo(self, fid, nick_name, post_text):
        exist_data = self.cp_mongo.find_one(self.cp_table, {"_id": fid})
        if exist_data:
            self.log.info(">>>找到相同的数据啦...")
            count = exist_data['count']
            count += 1
            exist_data.update({"count": count})
            self.cp_mongo.insert_batch_data(self.cp_table, [exist_data])
            return -1
        new_data = {
            "_id": fid,
            "nick_name": nick_name,
            "post_text": post_text,
            "count": 1
        }
        self.cp_mongo.insert_batch_data(self.cp_table, [new_data], insert=True)
        return 1


@click.command()
@click.option('--secrite_key',
              type=str,
              help=u'secrite_key')
@click.option('--token',
              type=str,
              help=u'token')
@click.option('--user_id',
              type=str,
              help=u'用户id')
@click.option('--check_code',
              type=str,
              help=u'check_code')
def main(secrite_key, token, user_id, check_code):
    try:
        YizhoucpCrawl(secrite_key,
                      token,
                      user_id,
                      check_code,
                      log=logger).start()

    except Exception as e:
        logger.error("发生异常退出: ")
        logger.exception(e)


if __name__ == '__main__':
    main()