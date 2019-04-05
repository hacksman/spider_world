#!/usr/bin/env python 
# coding:utf-8

import requests


def grab_proxy():
    proxy = requests.get("http://your_proxy_service", timeout=10)
    resp = proxy.json()
    if resp.get("status") == "ok":
        return resp["proxy"]
