#!/usr/bin/env python 
# coding:utf-8


def params2str(params):
    query = ""
    for k, v in params.items():
        query += "%s=%s&" % (k, v)
    query = query.strip("&")
    return query

