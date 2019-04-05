#!/usr/bin/env python 
# coding:utf-8


def params2str(params):
    query = ""
    for k, v in params.items():
        query += "%s=%s&" % (k, v)
    query = query.strip("&")
    return query


def get_video_url(array):
    if isinstance(array, list) and len(array) > 0:
        return array[-1]
