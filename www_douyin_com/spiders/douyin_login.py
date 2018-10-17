#!/usr/bin/env python 
# coding:utf-8
# @Time :10/17/18 19:31

from www_douyin_com.common.log_handler import getLogger
from www_douyin_com.common.utils import *

import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import time
import json
import copy
import re
import os
import sys

file_path_now = os.path.abspath(__file__)

sys.path.append('../')
sys.path.append('../../')
sys.path.append('../../../')


class DouyinLogin(object):
    logger = getLogger("DouyinLogin", console_out=True)

    __PHONE_SEND_CODE_URL = "https://lf.snssdk.com/passport/mobile/send_code/v1/"
    __INPUT_CODE_URL = "https://lf.snssdk.com/passport/mobile/sms_login/"

    __HEADERS = {"User-Agent": "Aweme/2.7.0 (iPhone; iOS 11.0; Scale/2.00)"}

    # params
    __CODE_PARAMS = {
        "pass-region": "1",
        "mix_mode": "1",
        "mobile": None,
    }

    __PHONE_SEND_CODE_MESSAGE = {
        "success": "验证码发送成功，请稍等几秒...请输入你的验证码：",
        "failed": "你发送验证码的速度都已经快超过光速了，请停下来活动活动手指吧，回车键结束此次操作..."
    }

    __MAX_TOKEN_VALIDITY = 60 * 50

    def __init__(self):
        self.common_params = common_params()

        self.__token = None

        self.request = requests.Session()

    def login(self, phone):
        # 默认 60 秒尝试一次 发送验证码，不要频繁尝试
        phone_send_code_params = copy.deepcopy(self.__CODE_PARAMS)
        phone_send_code_params['mobile'] = mixString("+86" + phone)
        phone_send_code_params['type'] = "3731"
        query_params = {**phone_send_code_params, **self.common_params}
        sign = getSign(self.__get_token(), query_params)
        params = {**query_params, **sign}
        resp = requests.get(self.__PHONE_SEND_CODE_URL,
                            params=params,
                            verify=False,
                            headers=self.__HEADERS)

        if resp.json().get('message') == "success":
            code = input(self.__PHONE_SEND_CODE_MESSAGE["success"])
            return self.__login_input_code(code, phone)
        else:
            input(self.__PHONE_SEND_CODE_MESSAGE["failed"])
            os._exit(0)

    def __login_input_code(self, code, phone):
        code_params = copy.deepcopy(self.__CODE_PARAMS)
        code_params['mobile'] = mixString("+86" + phone)
        code_params['code'] = mixString(code)
        query_params = {**code_params, **self.common_params}
        sign = getSign(self.__get_token(), query_params)
        params = {**query_params, **sign}
        resp = self.request.get(self.__INPUT_CODE_URL,
                                params=params,
                                verify=False,
                                headers=self.__HEADERS)
        if resp.json().get('message') == "success":
            self.logger.info("登录成功...")
            return self.request

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


if __name__ == '__main__':
    douyin_login = DouyinLogin()
    douyin_login.login('1333')


