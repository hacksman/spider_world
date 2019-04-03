#!/usr/bin/env python 
# coding:utf-8

import datetime
from copy import deepcopy


class Base:

    def json(self):
        d = deepcopy(self.__dict__)
        for k, v in d.items():
            if not v:
                continue
            from www_douyin_com.structures import Video
            if isinstance(v, Video):
                d[k] = v.json()
            if isinstance(v, datetime.datetime):
                d[k] = str(v)
        return d
