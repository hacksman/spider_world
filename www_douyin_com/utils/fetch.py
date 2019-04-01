#!/usr/bin/env python 
# coding:utf-8

import requests
from retrying import retry

from www_douyin_com.config import (DEFALUT_REQ_TIMEOUT, MAX_RETRY_REQ_TIMES, RETRY_RANDON_MAX_WAIT,
                                   RETRY_RANDON_MIN_WAIT)


def need_retry(exception):
    result = isinstance(exception, (requests.ConnectionError, requests.ReadTimeout))
    if result:
        print("Exception", type(exception), "occurred retrying...")
    return result


def fetch(url, **kwargs):

    @retry(stop_max_attempt_number=MAX_RETRY_REQ_TIMES, wait_random_min=RETRY_RANDON_MIN_WAIT,
           wait_random_max=RETRY_RANDON_MAX_WAIT, retry_on_exception=need_retry)
    def _fetch(url, **kwargs):

        kwargs.update({"verify": False})
        kwargs.update({"timeout": kwargs.get("timeout") or DEFALUT_REQ_TIMEOUT})
        response = requests.get(url, **kwargs)
        if response.status_code != 200:
            raise requests.ConnectionError("request status code should be 200! but got {}".format(response.status_code))
        return response.json()

    try:
        result = _fetch(url, **kwargs)
        return result
    except (requests.ConnectionError, requests.ReadTimeout):
        return {}

